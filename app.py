from flask import Flask, jsonify, request
from flasksqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(_name)

Configuração de conexão com o banco MySQL usando Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senhadoDB@localhost/dpu_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
swagger = Swagger(app)