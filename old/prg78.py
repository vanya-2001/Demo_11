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
    SELECT title FROM films
    WHERE genre=(
    SELECT id FROM genres
    WHERE title=?)
    """, ('фантастика',)
).fetchall()

for item in result:
    print(item)
# закрытие соединения с базой
connection.close()
