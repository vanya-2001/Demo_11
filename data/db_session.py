# ORM - Object Relational Mapping - объектно-реляционное отображение
# pip install sqlalchemy
"""
Для отслеживания состояний структуры таблиц БД нам потребуется
pip install alembic
После надо в терминале запустить: alembic init alembic
Далее зайти в созданную директорию alembic, найти файл env.py
Изменения смотрим в ветке webApp13 (/alembic/env.py)
Конфигурируем alembic.ini (см. файл alembic.ini в корне)
Вносим нужные изменения в нашу таблицу БД (в частности столе)
В терминале пишем команду:
alembic revision --autogenerate -m "Добавили столбец в таблицу users"
Чтобы подтвердить добавление используем команду:
alembic upgrade head
Если нужно откатиться до предыдущей версии таблии БД, то:
alembic downgrade head
"""
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл БД при вызове global_init")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f'Мы подключились к БД по адресу: {conn_str}')

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
