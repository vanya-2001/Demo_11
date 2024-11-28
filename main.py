# Монолитная архитектура (Monolithic Style)
import configparser
import datetime
import json
import os

from data import db_session
from data.sess_admin import Sess
from data.users import User
from data.news import News
from forms.user import RegisterForm
from forms.add_news import NewsForm
from api_folder import news_api, our_resources, user_resources

import requests
from flask import Flask, url_for, request, render_template, abort, jsonify
from flask import flash, redirect, make_response, session
from flask_restful import Api
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import current_user
from werkzeug.utils import secure_filename

from forms.loginform import LoginForm
from mailform import MailForm

MS1 = 'http://127.0.0.1:5000/api/v2/news'

current_directory = os.path.dirname(__file__)  # путь к корню сервера
UPLOAD_FOLDER = f'{current_directory}/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)  # , template_folder='my_tmp'
api = Api(app)  # регистрация нашего микросервиса
login_manager = LoginManager()
login_manager.init_app(app)  # привязали менеджер авторизации к приложению

app.config['SECRET_KEY'] = 'Holy guacamole! You should check in on some of those fields below'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

config = configparser.ConfigParser()  # объект для обращения к ini


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# обработка ошибки сервера 401
# Пользователь не авторизован
# для просмотра данной страницы
@app.errorhandler(401)
def http_401_handler(error):
    return render_template('error401.html', title='Требуется аутентификация')


# обработка ошибки сервера 400
@app.errorhandler(400)
def http_400_handler(_):
    return make_response(jsonify({'error': 'Ошибка 400'}), 400)


# обработка ошибки сервера 404
# Страница не найдена
@app.errorhandler(404)
def http_404_handler(error):
    return make_response(jsonify({'error': 'Новость не найдена'}), 404)


# def http_404_handler(error):
#     return render_template('error404.html', title='Контент не найден')

@login_manager.user_loader
def user_loader(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/')
@app.route('/index')
def index():
    param = {}
    param['text'] = 'Этот текст отобразится на главной странице'
    param['title'] = 'Флагман Консалтинг'
    return render_template('index.html', **param)
    # return """
    # <a href="/index">Главная</a> | <a href="/contacts">Контакты</a> | <a href="/img/1">Картинка 1</a>
    # | <a href="/img/2">Картинка 2</a>
    # """


@app.route('/admin')
@login_required
def admin():
    return render_template('admin/index.html', title="Панель администрирования")


@app.route('/adminuser')
@login_required
def users():
    users = requests.get('http://127.0.0.1:5000/api/v2/users').json()
    if users.get('error', None) or users.get('message', None):
        return redirect('/')
    return render_template('admin/users.html', title="Пользователи сайта",
                           users=users['users'])


@app.route('/admin/user_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def user_delete(id):
    if not current_user.is_admin():
        return redirect('/')
    res = requests.delete(f'http://127.0.0.1:5000/api/v2/user/{id}').json()
    temp = res.get('error', None)
    if temp:
        return render_template('admin/users.html', title=temp)
    return redirect('/adminuser')


@app.route('/session_test')
def session_test():
    visit_count = session.get('visit_count', 0)
    session['visit_count'] = visit_count + 1
    # visit_count % 3 - 0, 1, 2
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


# тестируем наш Api
@app.route('/apitest')
def api_test():
    res = requests.get(MS1).json()
    return render_template('apitest.html', title='Тестируем наш первый API', news=res['news'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')  # request.url, либо на нужную страницу
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
    if current_user.is_authenticated:
        return redirect('/')  # request.url, либо на нужную страницу
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if user.is_admin():
                sess_make = Sess(
                    title='admin',
                    content='super_long_admin_key'
                )
                db_sess.add(sess_make)
                db_sess.commit()
            return redirect('/')  # request.url, либо на нужную страницу
        return render_template('login.html', title='Ошибка авторизации',
                               message='Неправильная пара: логин - пароль!',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    db_sess = db_session.create_session()
    sess = db_sess.query(Sess).filter(Sess.title == 'admin').first()
    if sess:
        db_sess.delete(sess)
        db_sess.commit()
    return redirect('/')


# добавление новости
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/blog')
    return render_template('add_news.html', title='Добавить отзыв о тренинге',
                           form=form)


# редактирование новости
@app.route('/blog/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
            form.submit.data = 'Отредактировать'
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/blog')
        else:
            abort(404)
    return render_template('add_news.html', title='Отредактировать отзыв',
                           form=form)


# удаление новости
@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/blog')


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
@login_required
def success():
    return 'Успешно'



@app.route('/about')
def about():
    params = {}
    params['title'] = 'Команда экспертов'
    params['text'] = 'Мы перспективная и динамично развивающаяся компания...'
    return render_template('about.html', **params)


@app.route('/blog')
def blog():
    # if current_user.is_admin():
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




# Методы:
# GET - запрашивает информацию с сервера, не меняя его состояния
# POST - отправляет данные на сервер для обработки
# PUT - заменяет текущие данные на сервере данными запроса
# PATCH - частичная замена данных на сервере
# DELETE - удаляет указанные данные

# res = cur.execute("""select * from users
#                   where id > 1 and email not like(%1%)""")
# res.fetchall()

if __name__ == '__main__':
    db_session.global_init('db/blogs.db')
    # прописываем blueprint в основное приложение
    app.register_blueprint(news_api.blueprint)
    # прописываем доступ к отдельной новости по RESTful API v2
    api.add_resource(our_resources.NewsResource, '/api/v2/news/<int:news_id>')
    # прописываем доступ ко всем новостям по RESTful API v2
    api.add_resource(our_resources.NewsResourceList, '/api/v2/news')
    # прописываем доступ к отдельному пользователю по RESTful API v2
    api.add_resource(user_resources.UserResource, '/api/v2/user/<int:user_id>')
    # прописываем доступ ко всем пользователям по RESTful API v2
    api.add_resource(user_resources.UsersResourceList, '/api/v2/users')
    app.run(port=5000, host='127.0.0.1')
