# Projeto API DPU com Python
Neste projeto utilizei os componentes e bibliotecas:
-Flasgger e Swagger UI - Para Gerenciar as rotas da API.
-Flask - Para gerenciar rotas e responder a requisições HTTP.
-Flask-SQLAlchemy - Para auxiliar no gerenciamento do banco de dados.


## Instalação

Para instalar o projeto, siga esses passos:

### Processos necessários

```bash
#Clone o repositório para sua máquina local usando o comando:

git clone <URL do seu repositório>
cd Projeto_Python

#Instale as Dependências

pip install flask flask-sqlalchemy flasgger 

#Após isso inicie MySQL e crie um banco de dados chamado dpu_db e modificando o :
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senhadoDB@localhost/dpu_db'

#Execute o seguinte comando para garantir que as tabelas sejam criadas:
python app.py

#Inicie o servidor Flask para rodar a aplicação:
flask run

#Acesse a documentação da API que foi Gerada pelo Swagger:
http://127.0.0.1:5000/apidocs










