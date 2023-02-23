from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
from flasgger import Swagger
from flasgger.utils import swag_from
from marshmallow import Schema, fields, validate
from datetime import datetime

password = urllib.parse.quote_plus("1234567")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:' + \
    password + '@localhost:3307/full_stack'
db = SQLAlchemy(app)
Swagger(app)


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


# with app.app_context():
#     db.create_all()


@app.route('/alugueis', methods=['GET'])
def get_alugueis():
    aluguel = Aluguel.query.all()
    return jsonify([c.serialize() for c in aluguel])


@app.route('/alugueis/<int:id>', methods=['GET'])
def get_aluguel(id):
    aluguel = Aluguel.query.get(id)
    if aluguel:
        return jsonify(aluguel.serialize())
    else:
        return jsonify({'erro': 'Aluguel não encontrado'}), 404


@app.route('/alugueis', methods=['POST'])
def create_aluguel():
    data = request.get_json()
    aluguel = Aluguel(cpf_locatario=data['cpf_locatario'], id_carro=data['id_carro'],
                      timestamp=data['timestamp'])
    db.session.add(aluguel)
    db.session.commit()
    return jsonify({'aluguel': aluguel.serialize(), 'message': 'Aluguel Incluido'}), 201


@app.route('/alugueis/<int:id>', methods=['PUT'])
def update_aluguel(id):
    data = request.get_json()
    aluguel = Aluguel.query.get(id)
    if aluguel:
        aluguel.cpf_locatario = data['cpf_locatario']
        aluguel.id_carro = data['id_carro']
        aluguel.timestamp = data['timestamp']
        db.session.commit()
        return jsonify({'aluguel': aluguel.serialize(), 'message': 'Aluguel Editado'})
    else:
        return jsonify({'erro': 'Aluguel não encontrado'}), 404


@app.route('/alugueis/<int:id>', methods=['DELETE'])
def delete_aluguel(id):
    aluguel = Aluguel.query.get(id)
    if aluguel:
        Aluguel.query.filter_by(id=id).delete()
        db.session.commit()
        return jsonify({'message': 'Aluguel Excluido'}), 201
    else:
        return jsonify({'erro': 'Aluguel não encontrado'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=3001)
