import configparser
import datetime
import json
import os
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm

import requests
from flask import Flask, url_for, request, render_template
from flask import flash, redirect, make_response, session
from flask_login import LoginManager, login_user
from werkzeug.utils import secure_filename

from forms.loginform import LoginForm
from mailform import MailForm

current_directory = os.path.dirname(__file__)  # путь к корню сервера
UPLOAD_FOLDER = f'{current_directory}/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)  # привязали менеджер авторизации к приложению

app.config['SECRET_KEY'] = 'too_short_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

config = configparser.ConfigParser()  # объект для обращения к ini


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['text'] = 'Этот текст отобразится на главной странице'
    param['title'] = 'Главная'
    return render_template('index.html', **param)
    # return """
    # <a href="/index">Главная</a> | <a href="/contacts">Контакты</a> | <a href="/img/1">Картинка 1</a>
    # | <a href="/img/2">Картинка 2</a>
    # """


@login_manager.user_loader
def user_loader(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/session_test')
def session_test():
    visit_count = session.get('visit_count', 0)
    session['visit_count'] = visit_count + 1
    # session.pop('visit_count', None) # если надо программно уничтожить сессию
    return make_response(f'Вы посетили данную страницу {visit_count} раз.')


@app.route('/cookie_test')
def cookie_test():
    visit_count = int(request.cookies.get('visit_count', 0))
    if visit_count:
        res = make_response(f'Вы посетили данную страницу {visit_count + 1} раз')
        res.set_cookie('visit_count', str(visit_count + 1), max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response('За последние два года вы посетили данную страницу впервые.')
        res.set_cookie('visit_count', '1', max_age=60 * 60 * 24 * 365 * 2)
        # res.set_cookie('visit_count', '1', max_age=0) # удаляем cookies
    return res


@app.route('/news')
def news():
    with open("news.json", "rt", encoding="utf-8") as f:
        news_list = json.loads(f.read())
    print(news_list)
    return render_template('news.html', news=news_list, title='Новости')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'GET':
        return render_template('weather.html', title='Погода', form=None)
    elif request.method == 'POST':
        # читаем
        config.read('settings.ini')
        city = request.form['city']
        if len(city) < 2:
            flash('Город не введен или введён не полностью')
            return redirect(request.url)
        key = config['Weather']['key']

        res = requests.get('http://api.openweathermap.org/data/2.5/find',
                           params={'q': city,
                                   'type': 'like',
                                   'units': 'metric',
                                   'APPID': key})
        data = res.json()
        if len(data['list']) == 0:
            flash('Город введён неверно!')
            return redirect(request.url)
        temp = data['list'][0]['main']

        params = {}  # пустой словарь для передачи параметров в render weather.html
        params['temper'] = temp['temp']
        params['feel'] = temp['feels_like']
        params['press'] = temp['pressure']
        params['humid'] = temp['humidity']

        return render_template('weather.html',
                               title=f'Погода в городе {city}',
                               form=request.form, params=params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message=f'Пользователь с E-mail {form.email.data} уже есть')
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')  # request.url, либо на нужную страницу
        return render_template('login.html', title='Ошибка авторизации',
                               message='Неправильная пара: логин - пароль!',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# 1. Добавить требуемый пункт в меню
# 2. Создать .html-файл для расширения шаблона
# 3. Отрендерить, создав соответствующий декоратор
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = MailForm()
    params = {}
    if form.validate_on_submit():
        name = form.username.data  # получили имя с формы
        params['name'] = name  # добавили ключ и значение к словарю params
        phone = form.phone.data
        params['phone'] = phone
        email = form.email.data
        params['email'] = email
        message = form.message.data
        params['message'] = message
        params['page'] = request.url

        text = f"""
        Пользователь {name} оставил Вам сообщение:
        {message}
        Его телефон: {phone},
        E-mail: {email},
        Cтраница: {request.url}.
        """
        text_to_user = f"""
        Уважаемый (ая) {name}!
        Ваши данные:
        Телефон: {phone},
        E-mail: {email},
        успешно получены.
        Ваше сообщение:
        {message}
        принято рассмотрению.
        Отправлено со страницы: {request.url}.
        """
        # send_mail(email, 'Ваши данные на сайте', text_to_user)
        # send_mail('mrharut@yandex.ru', 'Запрос с сайта', text)
        return render_template('mailresult.html',
                               title='Ваши данные',
                               params=params)
    return render_template('contacts.html', title='Наши контакты', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html', title='Выбор файла', form=None)
    elif request.method == 'POST':
        if 'file' not in request.files:
            flash('Файл не был прочитан')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Файл не был отправлен')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Загрузка файлов данного типа запрещена!')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html', title='Файл загружен',
                                   form=True)


@app.route('/success')
def success():
    return 'Успех'


@app.route('/pets')
def pets():
    with open('pets.json', 'rt', encoding='utf-8') as f:
        pets_info = json.load(f)
    print(pets_info)
    return render_template('pets.html', pets=pets_info, title='Питомцы')


@app.route('/queue')
def queue():
    return render_template('queue.html', title='Очередь на медосмотр')


@app.route('/odd_even/', defaults={'num': 0})
@app.route('/odd_even/<int:num>')
def odd_even(num):
    return render_template('index.html', num=num, title='Чётное или нечётное')


@app.route('/countdown')
def countdown():
    cl = ['Старт']
    cl += [str(x) for x in reversed(range(11))]
    cl.append('Финиш')
    return '<br>'.join(cl)


@app.route('/about')
def about():
    params = {}
    params['title'] = 'О нас'
    params['text'] = 'Мы перспективная и динамично развивающаяся компания...'
    return render_template('about.html', **params)


@app.route('/blog')
def blog():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private == False)
    return render_template('blog.html', title='Новости', news=news)


# Статический контент (в папке static/...)
# Все изображения - static/images
# Таблицы стилей - static/css
# Шрифты - static/fonts
# Любые файлы для скачивания
# Файлы JS-сценариев - static/js
# Музыка, видео
# для удобства пользуемся url_for
@app.route('/img/', defaults={'num': None})
@app.route('/img/<num>')
def show_img(num):
    """
    :param num: по умолчанию - строка
    <int:num> - целое число
    <float:num> - действительное число
    <path:num> - строка со слешами для URL
    <uuid:num> - идентификатор в 16-м представлении (550e8400-e29b-41d4-a716-446655440000)
    :return: Путь к картинке
    """
    # num += 1
    if num:
        return f"""
        <h1>Python</h1>
        <img src="{url_for('static', filename=f'images/python-{num}.jpg')}"><br>
        <a href='/'>На главную</a>
        """
    else:
        return f"""
                <h1>Здесь ничего нет.</h1>
                <img src="{url_for('static', filename='images/python.png')}"><br>
                <a href='/'>На главную</a>
                """


# http://localhost:5000/two-params/Victor/12
@app.route('/two-params/<username>/<int:number>')
def two_params_func(username, number):
    param = 100 + number
    return f"""
    <h1>Пользователь: {username}</h1>
    <h2>Номер в системе: {param}</h2>
    """


# Методы:
# GET - запрашивает информацию с сервера, не меняя его состояния
# POST - отправляет данные на сервер для обработки
# PUT - заменяет текущие данные на сервере данными запроса
# PATCH - частичная замена данных на сервере
# DELETE - удаляет указанные данные
@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return render_template('form_sample.html', title='Заполните форму', form='None')
    elif request.method == 'POST':
        return render_template('form_sample.html', title='Ваши данные', form=request.form)


# res = cur.execute("""select * from users
#                   where id > 1 and email not like(%1%)""")
# res.fetchall()

if __name__ == '__main__':
    db_session.global_init('db/blogs.db')
    app.run(port=5000, host='127.0.0.1')
