from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Импортируем пакет Migrate для работы с миграциями
from flask_migrate import Migrate

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

# Подключаем базу данных к приложению
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../carsharing.sqlite"

# Отключаем вывод технических сообщений
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Создаем саму базу данных - объект db
db = SQLAlchemy(app)


# Создаем объект для работы с миграциями
migrate = Migrate(app, db)


from app import views
from app import models