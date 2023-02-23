from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
from flasgger import Swagger
from flasgger.utils import swag_from
from marshmallow import Schema, fields, validate
from datetime import datetime

password = urllib.parse.quote_plus("Pa@1234567")
print(password)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:' + \
    password + '@localhost/projeto_fullstack'
# 'mysql://root:password@host:port/database'
db = SQLAlchemy(app)
Swagger(app)


class Aluguel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf_locatario = db.Column(db.String(80), db.ForeignKey(
        'pessoa.cpf'), nullable=False)
    id_carro = db.Column(db.Integer, db.ForeignKey(
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


class Carro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    placa = db.Column(db.String(80), nullable=False)
    alugueis = db.relationship('Aluguel', backref='carro')

    def __repr__(self):
        return '<Carro %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'marca': self.marca,
            'modelo': self.modelo,
            'ano': self.ano,
            'placa': self.placa
        }


class CarroSchema(Schema):
    id = fields.Int(dump_only=True)
    marca = fields.Str(required=True, validate=validate.Length(max=80))
    modelo = fields.Str(required=True, validate=validate.Length(max=80))
    ano = fields.Int(
        required=True, validate=validate.Range(min=1900, max=2100))
    placa = fields.Str(
        required=True, validate=validate.Regexp(r'^[A-Z]{3}-\d{4}$'))


# with app.app_context():
#     db.create_all()


@app.route('/carros', methods=['GET'])
@swag_from('swagger_docs\\carro\\get_carros.yml')
def get_carros():
    carros = Carro.query.all()
    return jsonify([c.serialize() for c in carros])


@app.route('/carros/<int:id>', methods=['GET'])
@swag_from('swagger_docs\\carro\\get_carro.yml')
def get_carro(id):
    carro = Carro.query.get(id)
    if carro:
        return jsonify(carro.serialize())
    else:
        return jsonify({'erro': 'Carro não encontrado'}), 404


@app.route('/carros', methods=['POST'])
@swag_from('swagger_docs\\carro\\create_carro.yml')
def create_carro():
    data = request.get_json()
    carro = Carro(marca=data['marca'], modelo=data['modelo'],
                  ano=data['ano'], placa=data['placa'])
    db.session.add(carro)
    db.session.commit()
    return jsonify({'carro': carro.serialize(), 'message': 'Carro Incluido'}), 201


@app.route('/carros/<int:id>', methods=['PUT'])
@swag_from('swagger_docs\\carro\\update_carro.yml')
def update_carro(id):
    data = request.get_json()
    carro = Carro.query.get(id)
    if carro:
        carro.marca = data['marca']
        carro.modelo = data['modelo']
        carro.ano = data['ano']
        carro.placa = data['placa']
        db.session.commit()
        return jsonify({'carro': carro.serialize(), 'message': 'Carro Editado'})
    else:
        return jsonify({'erro': 'Carro não encontrado'}), 404


@app.route('/carros/<int:id>', methods=['DELETE'])
@swag_from('swagger_docs\\carro\\delete_carro.yml')
def delete_carro(id):
    carro = Carro.query.get(id)
    if carro:
        Carro.query.filter_by(id=id).delete()
        db.session.commit()
        return jsonify({'message': 'Carro Excluido'}), 201
    else:
        return jsonify({'erro': 'Carro não encontrado'}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
