#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)


# Index route
class Index(Resource):
    def get(self):
        return {"message": "Welcome to the Plant Store API"}, 200


api.add_resource(Index, '/')


# All plants
class Plants(Resource):
    def get(self):
        plants = [p.to_dict() for p in Plant.query.all()]
        return plants, 200

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
            is_in_stock=data.get('is_in_stock', True)
        )
        db.session.add(new_plant)
        db.session.commit()
        return new_plant.to_dict(), 201


api.add_resource(Plants, '/plants')


# Single plant
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        return plant.to_dict(), 200

    def patch(self, id):
        plant = Plant.query.get_or_404(id)
        data = request.get_json()
        for key, value in data.items():
            setattr(plant, key, value)
        db.session.commit()
        return plant.to_dict(), 200

    def delete(self, id):
        plant = Plant.query.get_or_404(id)
        db.session.delete(plant)
        db.session.commit()
        return '', 204


api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
