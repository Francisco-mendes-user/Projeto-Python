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


# Seção de listagem,criação,excluir e atualizar da tabela de aposentados
@app.route('/aposentados', methods=['GET'])
def listar_aposentados():
    """
    Lista todos os aposentados
    ---
    responses:
      200:
        description: Lista de aposentados
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
              data_aposentadoria:
                type: string
                format: date
              email:
                type: string
              telefone:
                type: string
    """
    aposentados = Aposentado.query.all()
    return jsonify([{
        'id': a.id,
        'nome': a.nome,
        'cargo': a.cargo,
        'data_aposentadoria': a.data_aposentadoria,
        'email': a.email,
        'telefone': a.telefone
    } for a in aposentados])

@app.route('/aposentados', methods=['POST'])
def criar_aposentado():
    """
    Cria um novo aposentado
    ---
    parameters:
      - name: aposentado
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            cargo:
              type: string
            data_aposentadoria:
              type: string
              format: date
            email:
              type: string
            telefone:
              type: string
    responses:
      201:
        description: Aposentado criado com sucesso
    """
    dados = request.get_json()
    novo_aposentado = Aposentado(
        nome=dados['nome'],
        cargo=dados.get('cargo'),
        data_aposentadoria=dados.get('data_aposentadoria'),
        email=dados.get('email'),
        telefone=dados.get('telefone')
    )
    db.session.add(novo_aposentado)
    db.session.commit()
    return jsonify({'message': 'Aposentado criado com sucesso!'}), 201

@app.route('/aposentados/<int:id>', methods=['PUT'])
def atualizar_aposentado(id):
    """
    Atualiza um aposentado existente
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: aposentado
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            cargo:
              type: string
            data_aposentadoria:
              type: string
              format: date
            email:
              type: string
            telefone:
              type: string
    responses:
      200:
        description: Aposentado atualizado com sucesso
    """
    aposentado = Aposentado.query.get_or_404(id)
    dados = request.get_json()
    aposentado.nome = dados.get('nome', aposentado.nome)
    aposentado.cargo = dados.get('cargo', aposentado.cargo)
    aposentado.data_aposentadoria = dados.get('data_aposentadoria', aposentado.data_aposentadoria)
    aposentado.email = dados.get('email', aposentado.email)
    aposentado.telefone = dados.get('telefone', aposentado.telefone)
    db.session.commit()
    return jsonify({'message': 'Aposentado atualizado com sucesso!'})

@app.route('/aposentados/<int:id>', methods=['DELETE'])
def deletar_aposentado(id):
    """
    Deleta um aposentado
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Aposentado deletado com sucesso
    """
    aposentado = Aposentado.query.get_or_404(id)
    db.session.delete(aposentado)
    db.session.commit()
    return jsonify({'message': 'Aposentado deletado com sucesso!'})


# Seção de listagem,criação,excluir e atualizar da tabela de beneficiarios
@app.route('/beneficiarios', methods=['GET'])
def listar_beneficiarios():
    """
    Lista todos os beneficiários
    ---
    responses:
      200:
        description: Lista de beneficiários
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              cpf:
                type: string
              data_nascimento:
                type: string
                format: date
              email:
                type: string
              telefone:
                type: string
    """
    beneficiarios = Beneficiario.query.all()
    return jsonify([{
        'id': b.id,
        'nome': b.nome,
        'cpf': b.cpf,
        'data_nascimento': b.data_nascimento,
        'email': b.email,
        'telefone': b.telefone
    } for b in beneficiarios])

@app.route('/beneficiarios', methods=['POST'])
def criar_beneficiario():
    """
    Cria um novo beneficiário
    ---
    parameters:
      - name: beneficiario
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            cpf:
              type: string
            data_nascimento:
              type: string
              format: date
            email:
              type: string
            telefone:
              type: string
    responses:
      201:
        description: Beneficiário criado com sucesso
    """
    dados = request.get_json()
    novo_beneficiario = Beneficiario(
        nome=dados['nome'],
        cpf=dados.get('cpf'),
        data_nascimento=dados.get('data_nascimento'),
        email=dados.get('email'),
        telefone=dados.get('telefone')
    )
    db.session.add(novo_beneficiario)
    db.session.commit()
    return jsonify({'message': 'Beneficiário criado com sucesso!'}), 201

@app.route('/beneficiarios/<int:id>', methods=['PUT'])
def atualizar_beneficiario(id):
    """
    Atualiza um beneficiário existente
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: beneficiario
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            cpf:
              type: string
            data_nascimento:
              type: string
              format: date
            email:
              type: string
            telefone:
              type: string
    responses:
      200:
        description: Beneficiário atualizado com sucesso
    """
    beneficiario = Beneficiario.query.get_or_404(id)
    dados = request.get_json()
    beneficiario.nome = dados.get('nome', beneficiario.nome)
    beneficiario.cpf = dados.get('cpf', beneficiario.cpf)
    beneficiario.data_nascimento = dados.get('data_nascimento', beneficiario.data_nascimento)
    beneficiario.email = dados.get('email', beneficiario.email)
    beneficiario.telefone = dados.get('telefone', beneficiario.telefone)
    db.session.commit()
    return jsonify({'message': 'Beneficiário atualizado com sucesso!'})

@app.route('/beneficiarios/<int:id>', methods=['DELETE'])
def deletar_beneficiario(id):
    """
    Deleta um beneficiário
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Beneficiário deletado com sucesso
    """
    beneficiario = Beneficiario.query.get_or_404(id)
    db.session.delete(beneficiario)
    db.session.commit()
    return jsonify({'message': 'Beneficiário deletado com sucesso!'})