from requests import get, post, delete

# тест REST API на get
print(get('http://127.0.0.1:5000/api/news').json())
print(get('http://127.0.0.1:5000/api/news/3').json())
res = get('http://127.0.0.1:5000/api/news/').json()
if res.get('error', None):  # метод словаря get
    print(res['error'])
else:
    print(res['news']['content'])
# res = get('http://127.0.0.1:5000/api/news/1').json()
# print(res['news']['content'])

# тест REST API на post
print(post('http://127.0.0.1:5000/api/news', json={}).json())
print(post('http://127.0.0.1:5000/api/news',
           json={'title': 'Заголовок'}).json())
print(post('http://127.0.0.1:5000/api/news',
           json={'title': 'Заголовок через API',
                 'content': 'Текст новости',
                 'user_id': 1,
                 'is_private': False
                 }).json())

# тест REST API на delete
print(delete('http://127.0.0.1:5000/api/news/5').json())
# запись с id=4 только что была удалена
print(delete('http://127.0.0.1:5000/api/news/5').json())