from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///taskmanager.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Печать SQL-запросов для создания таблиц
from sqlalchemy.schema import CreateTable


def print_sql_queries():
    print(CreateTable(User.__table__).compile(engine))
    print(CreateTable(Task.__table__).compile(engine))


# Импорт функций в другие модули
from app.models.user_2 import User
from app.models.task_2 import Task