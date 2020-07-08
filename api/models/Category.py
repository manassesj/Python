from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    
    def __init__(self, name):
        self.name = name

class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)

def add_category():
    name = request.json['name']
    

    new_category = category(name)

    db.session.add(new_category)
    db.session.commit()

    return category_schema.jsonify(new_category)