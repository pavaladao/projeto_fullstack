from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
from flasgger.utils import swag_from
from datetime import datetime


password = urllib.parse.quote_plus("1234567")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:' + \
    password + '@localhost:3307/full_stack'
db = SQLAlchemy(app)


class Aluguel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf_locatario = db.Column(db.String(80), db.ForeignKey(
        'pessoa.cpf'), nullable=False)
    id_carro = db.Column(db.String(80), db.ForeignKey(
        'carro.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Aluguel %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'cpf_locatario': self.cpf_locatario,
            'id_carro': self.id_carro,
            'timestamp': self.timestamp.isoformat()
        }


class Pessoa(db.Model):
    cpf = db.Column(db.String(80), primary_key=True, autoincrement=False)
    nome = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    alugueis = db.relationship('Aluguel', backref='pessoa')

    def __repr__(self):
        return '<Pessoa %r>' % self.nome

    def serialize(self):
        return {
            'cpf': self.cpf,
            'nome': self.nome,
            'idade': self.idade,
        }


# with app.app_context():
#     db.drop_all()
#     # db.create_all()


@app.route('/pessoas', methods=['GET'])
@swag_from('swagger_docs\\pessoa\\pessoas.yml')
def get_pessoas():

    pessoas = Pessoa.query.all()
    return jsonify([c.serialize() for c in pessoas])


@app.route('/pessoas/<int:cpf>', methods=['GET'])
@swag_from('swagger_docs\\pessoa\\pessoa.yml')
def get_pessoa(cpf):

    pessoa = Pessoa.query.get(cpf)

    if pessoa:
        return jsonify(pessoa.serialize()), 200
    else:
        return jsonify({'erro': 'Pessoa não encontrada'}), 404


@app.route('/pessoas', methods=['POST'])
@swag_from('swagger_docs\\pessoa\\create_pessoa.yml')
def create_pessoa():

    data = request.get_json()
    pessoa = Pessoa(cpf=data['cpf'], nome=data['nome'], idade=data['idade'])
    db.session.add(pessoa)
    db.session.commit()
    return jsonify({'pessoa': pessoa.serialize(), 'message': 'Pessoa Criada'}), 201


@app.route('/pessoas/<int:cpf>', methods=['PUT'])
@swag_from('swagger_docs\\pessoa\\update_pessoa.yml')
def update_pessoa(cpf):

    data = request.get_json()
    pessoa = Pessoa.query.get(cpf)

    if pessoa:
        pessoa.nome = data['nome']
        pessoa.idade = data['idade']
        db.session.commit()
        return jsonify({'pessoa': pessoa.serialize(), 'message': 'Pessoa Editada'}), 201
    else:
        return jsonify({'erro': 'Pessoa não encontrada'}), 404


@app.route('/pessoas/<int:cpf>', methods=['DELETE'])
@swag_from('swagger_docs\\pessoa\\delete_pessoa.yml')
def delete_pessoa(cpf):

    pessoa = Pessoa.query.get(cpf)

    if pessoa:
        Pessoa.query.filter_by(cpf=cpf).delete()
        db.session.commit()
        return jsonify({'message': 'Pessoa Excluída'}), 201
    else:
        return jsonify({'erro': 'Pessoa não encontrada'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=3000)
