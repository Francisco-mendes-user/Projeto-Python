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


    
# Seção de listagem,criação,excluir e atualizar da tabela de pessoas
@app.route('/pessoas', methods=['GET'])
def listar_pessoas():
    """
    Lista todas as pessoas
    ---
    responses:
      200:
        description: Lista de pessoas
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
    pessoas = Pessoa.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'cpf': p.cpf,
        'data_nascimento': p.data_nascimento,
        'email': p.email,
        'telefone': p.telefone
    } for p in pessoas])

@app.route('/pessoas', methods=['POST'])
def criar_pessoa():
    """
    Cria uma nova pessoa
    ---
    parameters:
      - name: pessoa
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
        description: Pessoa criada com sucesso
    """
    dados = request.get_json()
    nova_pessoa = Pessoa(
        nome=dados['nome'],
        cpf=dados.get('cpf'),
        data_nascimento=dados.get('data_nascimento'),
        email=dados.get('email'),
        telefone=dados.get('telefone')
    )
    db.session.add(nova_pessoa)
    db.session.commit()
    return jsonify({'message': 'Pessoa criada com sucesso!'}), 201

@app.route('/pessoas/<int:id>', methods=['PUT'])
def atualizar_pessoa(id):
    """
    Atualiza uma pessoa existente
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: pessoa
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
        description: Pessoa atualizada com sucesso
    """
    pessoa = Pessoa.query.get_or_404(id)
    dados = request.get_json()
    pessoa.nome = dados.get('nome', pessoa.nome)
    pessoa.cpf = dados.get('cpf', pessoa.cpf)
    pessoa.data_nascimento = dados.get('data_nascimento', pessoa.data_nascimento)
    pessoa.email = dados.get('email', pessoa.email)
    pessoa.telefone = dados.get('telefone', pessoa.telefone)
    db.session.commit()
    return jsonify({'message': 'Pessoa atualizada com sucesso!'})

@app.route('/pessoas/<int:id>', methods=['DELETE'])
def deletar_pessoa(id):
    """
    Deleta uma pessoa
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Pessoa deletada com sucesso
    """
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    return jsonify({'message': 'Pessoa deletada com sucesso!'})

    
# Seção de listagem,criação,excluir e atualizar da tabela de Tipo de pessoas
@app.route('/tipos_de_pessoas', methods=['GET'])
def listar_tipos_de_pessoas():
    """
    Lista todos os tipos de pessoas
    ---
    responses:
      200:
        description: Lista de tipos de pessoas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              tipo:
                type: string
    """
    tipos_de_pessoas = TipoPessoa.query.all()
    return jsonify([{
        'id': t.id,
        'tipo': t.tipo
    } for t in tipos_de_pessoas])

@app.route('/tipos_de_pessoas', methods=['POST'])
def criar_tipo_pessoa():
    """
    Cria um novo tipo de pessoa
    ---
    parameters:
      - name: tipo_pessoa
        in: body
        required: true
        schema:
          type: object
          properties:
            tipo:
              type: string
    responses:
      201:
        description: Tipo de pessoa criado com sucesso
    """
    dados = request.get_json()
    novo_tipo_pessoa = TipoPessoa(tipo=dados['tipo'])
    db.session.add(novo_tipo_pessoa)
    db.session.commit()
    return jsonify({'message': 'Tipo de pessoa criado com sucesso!'}), 201

@app.route('/tipos_de_pessoas/<int:id>', methods=['PUT'])
def atualizar_tipo_pessoa(id):
    """
    Atualiza um tipo de pessoa existente
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: tipo_pessoa
        in: body
        required: true
        schema:
          type: object
          properties:
            tipo:
              type: string
    responses:
      200:
        description: Tipo de pessoa atualizado com sucesso
    """
    tipo_pessoa = TipoPessoa.query.get_or_404(id)
    dados = request.get_json()
    tipo_pessoa.tipo = dados.get('tipo', tipo_pessoa.tipo)
    db.session.commit()
    return jsonify({'message': 'Tipo de pessoa atualizado com sucesso!'})

@app.route('/tipos_de_pessoas/<int:id>', methods=['DELETE'])
def deletar_tipo_pessoa(id):
    """
    Deleta um tipo de pessoa
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tipo de pessoa deletado com sucesso
    """
    tipo_pessoa = TipoPessoa.query.get_or_404(id)
    db.session.delete(tipo_pessoa)
    db.session.commit()
    return jsonify({'message': 'Tipo de pessoa deletado com sucesso!'})


    
# Seção de listagem,criação,excluir e atualizar da tabela de pessoa tipo
@app.route('/pessoa_tipo', methods=['GET'])
def listar_pessoa_tipo():
    """
    Lista todos os relacionamentos entre pessoas e tipos
    ---
    responses:
      200:
        description: Lista de relacionamentos entre pessoas e tipos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              pessoa_id:
                type: integer
              tipo_id:
                type: integer
              data_inicio:
                type: string
                format: date
              data_fim:
                type: string
                format: date
    """
    pessoa_tipos = PessoaTipo.query.all()
    return jsonify([{
        'id': pt.id,
        'pessoa_id': pt.pessoa_id,
        'tipo_id': pt.tipo_id,
        'data_inicio': pt.data_inicio,
        'data_fim': pt.data_fim
    } for pt in pessoa_tipos])

@app.route('/pessoa_tipo', methods=['POST'])
def criar_pessoa_tipo():
    """
    Cria um novo relacionamento entre pessoa e tipo
    ---
    parameters:
      - name: pessoa_tipo
        in: body
        required: true
        schema:
          type: object
          properties:
            pessoa_id:
              type: integer
            tipo_id:
              type: integer
            data_inicio:
              type: string
              format: date
            data_fim:
              type: string
              format: date
    responses:
      201:
        description: Relacionamento entre pessoa e tipo criado com sucesso
    """
    dados = request.get_json()
    novo_pessoa_tipo = PessoaTipo(
        pessoa_id=dados['pessoa_id'],
        tipo_id=dados['tipo_id'],
        data_inicio=dados.get('data_inicio'),
        data_fim=dados.get('data_fim')
    )
    db.session.add(novo_pessoa_tipo)
    db.session.commit()
    return jsonify({'message': 'Relacionamento entre pessoa e tipo criado com sucesso!'}), 201

@app.route('/pessoa_tipo/<int:id>', methods=['PUT'])
def atualizar_pessoa_tipo(id):
    """
    Atualiza um relacionamento entre pessoa e tipo existente
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: pessoa_tipo
        in: body
        required: true
        schema:
          type: object
          properties:
            pessoa_id:
              type: integer
            tipo_id:
              type: integer
            data_inicio:
              type: string
              format: date
            data_fim:
              type: string
              format: date
    responses:
      200:
        description: Relacionamento entre pessoa e tipo atualizado com sucesso
    """
    pessoa_tipo = PessoaTipo.query.get_or_404(id)
    dados = request.get_json()
    pessoa_tipo.pessoa_id = dados.get('pessoa_id', pessoa_tipo.pessoa_id)
    pessoa_tipo.tipo_id = dados.get('tipo_id', pessoa_tipo.tipo_id)
    pessoa_tipo.data_inicio = dados.get('data_inicio', pessoa_tipo.data_inicio)
    pessoa_tipo.data_fim = dados.get('data_fim', pessoa_tipo.data_fim)
    db.session.commit()
    return jsonify({'message': 'Relacionamento entre pessoa e tipo atualizado com sucesso!'})

@app.route('/pessoa_tipo/<int:id>', methods=['DELETE'])
def deletar_pessoa_tipo(id):
    """
    Deleta um relacionamento entre pessoa e tipo
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Relacionamento entre pessoa e tipo deletado com sucesso
    """
    pessoa_tipo = PessoaTipo.query.get_or_404(id)
    db.session.delete(pessoa_tipo)
    db.session.commit()
    return jsonify({'message': 'Relacionamento entre pessoa e tipo deletado com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
