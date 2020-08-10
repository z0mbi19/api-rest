#import que eu vou usar no projeto
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# Iniciar o app
app =Flask(__name__)
CORS(app)

# Local do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))

# Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Iniciar DB

db = SQLAlchemy(app)

# Iniciar ma

ma = Marshmallow(app)

# Contato Class/Model

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.Integer, unique=True)
    delete = db.Column(db.Boolean)

    def __init__(self, nome, telefone, delete):
        self.nome = nome
        self.telefone = telefone
        self.delete = delete

# Contato Schema

class ContatoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'telefone', 'delete')

# Iniciar schema

contato_schema = ContatoSchema()
contatos_schema = ContatoSchema(many=True)

# Criar um contato

@app.route('/contato', methods=['POST'])
def update_contato():
    nome = request.json['nome']
    telefone = request.json['telefone']
    delete = request.json['delete']

    new_contato = Contato(nome, telefone, delete)

    db.session.add(new_contato)
    db.session.commit()

    return contato_schema.jsonify(new_contato)

# Listar todos os contatos

@app.route('/contato', methods=['GET'])
def get_contatos():
    all_contatos = Contato.query.filter(Contato.delete == False).all()
    result = contatos_schema.dump(all_contatos)
    return jsonify(result)

# Listar um os contatos

@app.route('/contato/<id>', methods=['GET'])
def get_contato(id):
    contato = Contato.query.get(id)
    return contato_schema.jsonify(contato)

# Atualizar um contato

@app.route('/contato/<id>', methods=['PUT'])
def add_contato(id):
    contato = Contato.query.get(id)

    nome = request.json['nome']
    telefone = request.json['telefone']
    delete = request.json['delete']

    contato.nome = nome
    contato.telefone = telefone
    contato.delete = delete

    db.session.commit()

    return contato_schema.jsonify(contato)

# Deletar contato

@app.route('/contato/<id>', methods=['DELETE'])
def delete_contato(id):
    contato = Contato.query.get(id)
    contato.delete = True
    db.session.commit()

    return contato_schema.jsonify(contato)

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)