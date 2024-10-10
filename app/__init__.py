from sqlalchemy.schema import CreateTable
from app.backend.db import Base, engine
from app.models.user_2 import User
from app.models.task_2 import Task


Base.metadata.create_all(bind=engine)  # Печать SQL-запросов для создания таблиц
print(CreateTable(User.__table__).compile(engine))
print(CreateTable(Task.__table__).compile(engine))

