# pip install psycopg2
import psycopg2

connection = psycopg2.connect(user="postgres", password="123",
                              host="127.0.0.1", port="5432",
                              database='lib')

cursor = connection.cursor()

result = cursor.execute("""select * from author""")

connection.close()