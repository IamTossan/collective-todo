from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flask'

db = SQLAlchemy(app)

from collective_todo.routes.auth import *
from collective_todo.routes.user import *
from collective_todo.routes.todo import *

