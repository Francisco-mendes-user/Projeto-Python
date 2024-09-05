from flask import Flask, jsonify, request
from flasksqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(_name)

Configuração de conexão com o banco MySQL usando Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senhadoDB@localhost/dpu_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
swagger = Swagger(app)


# Definindo os modelos das tabelas
class Servidor(db.Model):
    __tablename__ = 'servidores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(50))
    data_admissao = db.Column(db.Date)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

class Aposentado(db.Model):
    __tablename__ = 'aposentados'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(50))
    data_aposentadoria = db.Column(db.Date)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

class Beneficiario(db.Model):
    __tablename__ = 'beneficiarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11))
    data_nascimento = db.Column(db.Date)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

class Pessoa(db.Model):
    __tablename__ = 'pessoas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True)
    data_nascimento = db.Column(db.Date)
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

class TipoPessoa(db.Model):
    __tablename__ = 'tipos_de_pessoas'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)

class PessoaTipo(db.Model):
    __tablename__ = 'pessoa_tipo'
    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'))
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_de_pessoas.id'))
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)

    pessoa = db.relationship('Pessoa', backref='pessoa_tipos')
    tipo = db.relationship('TipoPessoa', backref='pessoa_tipos')