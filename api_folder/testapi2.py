from requests import get, post, delete

# тест REST API v2 на get
print(get('http://127.0.0.1:5000/api/v2/news').json())
print(get('http://127.0.0.1:5000/api/v2/news/3').json())
res = get('http://127.0.0.1:5000/api/v2/news/1').json()
if res.get('error', None):  # метод словаря get
    print(res['error'])
else:
    print(res['news']['content'])
    print(res['news']['user_id'])
# res = get('http://127.0.0.1:5000/api/news/1').json()
# print(res['news']['content'])

# тест REST API на post
print(post('http://127.0.0.1:5000/api/v2/news', json={}).json())
print(post('http://127.0.0.1:5000/api/v2/news',
           json={'title': 'Заголовок'}).json())
print(post('http://127.0.0.1:5000/api/v2/news',
           json={'title': 'Заголовок через API #5',
                 'content': 'Текст новости',
                 'user_id': 1,
                 'is_private': False
                 }).json())

# тест REST API v2 на delete
print(delete('http://127.0.0.1:5000/api/v2/news/6').json())
# запись с id=6 только что была удалена
print(delete('http://127.0.0.1:5000/api/v2/news/6').json())
