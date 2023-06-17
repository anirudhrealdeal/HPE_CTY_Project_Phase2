import json
from dataclasses import dataclass

import requests
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main' # to connect to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)
#only data classes are json serializable
@dataclass
class Product(db.Model):
    id:int
    title: str
    image: str
    id = db.Column(db.Integer, primary_key=True, autoincrement=False) # autoincrement to False because product
    #created in the django this will only and this app will only catch the event from rabbitMQ and it will create the product
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id: int
    user_id: int
    product_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id','product_id', name = 'user_product_unique')

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())
@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://host.docker.internal:8001/api/user')
    json = req.json()
    try:
        productUser = ProductUser(user_id=json['id'],product_id=id)
        db.session.add(productUser)
        db.session.commit()
        # event
        publish('product_liked', id)

    except:
        # error will happen if the user tries to like the picture again
        abort(400, 'You already liked this product')

    return jsonify({
        'message':'success'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
