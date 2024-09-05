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

    
# Seção de listagem,criação,excluir e atualizar da tabela de servidores
@app.route('/servidores', methods=['GET'])
def listar_servidores():
    """
    Lista todos os servidores
    ---
    responses:
      200:
        description: Lista de servidores
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              cargo:
                type: string
              data_admissao:
                type: string
                format: date
              email:
                type: string
              telefone:
                type: string
    """
    servidores = Servidor.query.all()
    return jsonify([{
        'id': s.id,
        'nome': s.nome,
        'cargo': s.cargo,
        'data_admissao': s.data_admissao,
        'email': s.email,
        'telefone': s.telefone
    } for s in servidores])

@app.route('/servidores', methods=['POST'])
def criar_servidor():
    """
    Cria um novo servidor
    ---
    parameters:
      - name: servidor
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            cargo:
              type: string
            data_admissao:
              type: string
              format: date
            email:
              type: string
            telefone:
              type: string
    responses:
      201:
        description: Servidor criado com sucesso
    """
    dados = request.get_json()
    novo_servidor = Servidor(
        nome=dados['nome'],
        cargo=dados.get('cargo'),
        data_admissao=dados.get('data_admissao'),
        email=dados.get('email'),
        telefone=dados.get('telefone')
    )
    db.session.add(novo_servidor)
    db.session.commit()
    return jsonify({'message': 'Servidor criado com sucesso!'}), 201

@app.route('/servidores/<int:id>', methods=['PUT'])
def atualizar_servidor(id):
    """
    Atualiza um servidor existente
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: servidor
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            cargo:
              type: string
            data_admissao:
              type: string
              format: date
            email:
              type: string
            telefone:
              type: string
    responses:
      200:
        description: Servidor atualizado com sucesso
    """
    servidor = Servidor.query.get_or_404(id)
    dados = request.get_json()
    servidor.nome = dados.get('nome', servidor.nome)
    servidor.cargo = dados.get('cargo', servidor.cargo)
    servidor.data_admissao = dados.get('data_admissao', servidor.data_admissao)
    servidor.email = dados.get('email', servidor.email)
    servidor.telefone = dados.get('telefone', servidor.telefone)
    db.session.commit()
    return jsonify({'message': 'Servidor atualizado com sucesso!'})

@app.route('/servidores/<int:id>', methods=['DELETE'])
def deletar_servidor(id):
    """
    Deleta um servidor
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Servidor deletado com sucesso
    """
    servidor = Servidor.query.get_or_404(id)
    db.session.delete(servidor)
    db.session.commit()
    return jsonify({'message': 'Servidor deletado com sucesso!'})