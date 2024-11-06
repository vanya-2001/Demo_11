# Create Read(Retrieve) Update Delete
# CRUD
# PEP 249 (connection,  cursor)
import sqlite3

# Подключение (connection)
connection = sqlite3.connect('films_db.sqlite')

# Создаём курсор
cursor = connection.cursor()

# исполнение запроса
result = cursor.execute(
    """
    UPDATE films
    SET duration = 282
    WHERE title = 'Аватар'
    """
)

# подтверждаем все изменения в БД
choice = input('Вы действительно хотите обновить (Y/N):')
if choice == 'Y':
    connection.commit()

# for item in result:
#     print(item)
# закрытие соединения с базой
connection.close()
