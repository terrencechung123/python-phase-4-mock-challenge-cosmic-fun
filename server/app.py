from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse

from models import db, Scientist, Planet, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Scientists(Resource):
    def get(self):
        scientists = Scientist.query.all()
        scientists_dict_list = [scientist.to_dict() for scientist in scientists]
        response = make_response(
            scientists_dict_list,
            200
        )
        return response
    def post(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({
                "error": "Scientist not found"
            }, 404)
        data = request.get_json()
        for attr in data:
            setattr(scientist, attr, data[attr])
        try:
            db.session.commit()
        except:
            return make_response({
                "errors": ["validation errors"]
            }, 400)
        response = make_response(scientist.to_dict(), 202)
        return response
api.add_resource(Scientists,'/scientists')

class ScientistById(Resource):
    def get(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({
                "error": "Scientist not found"
            }, 404)
        response = make_response(
            scientist.to_dict(rules=('planets',)),
            200
        )
        return response

    def patch(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({
                "error": "Scientist not found"
            }, 404)
        data = request.get_json()
        if not data:
            return make_response({
                "error": "No data provided"
            }, 400)
        errors = []
        if 'name' in data:
            scientist.name = data['name']
        if 'field_of_study' in data:
            scientist.field_of_study = data['field_of_study']
        if 'avatar' in data:
            scientist.avatar = data['avatar']
        # Validate the updated scientist
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            errors.append(str(e))
        if errors:
            return make_response({
                "errors": errors
            }, 400)
        response = make_response(scientist.to_dict(), 202)
        return response

    def delete(self, id):
        scientist = Scientist.query.get(id)
        if not scientist:
            return {'error': f'Scientist with id {id} not found'}, 404
        missions = Mission.query.filter_by(scientist_id=id).all()
        for mission in missions:
            db.session.delete(mission)
        db.session.delete(scientist)
        db.session.commit()
        return jsonify({}), 204
api.add_resource(ScientistById, '/scientists/<int:id>')

class Planets(Resource):
    def get(self):
        planets = Planet.query.all()
        planets_dict_list = [planet.to_dict() for planet in planets]
        response = make_response(
            planets_dict_list,
            200
        )
        return response
api.add_resource(Planets,'/planets')

class Missions(Resource):
    def post(self):
        data = request.get_json()
        try:
            mission = Mission(
                name = data['name'],
                scientist_id = data['scientist_id'],
                planet_id = data['planet_id']
            )
            db.session.add(mission)
            db.session.commit()
        except Exception as e:
            response_dict = {
                "errors": [e.__str__()]
            }
            return make_response(
                response_dict,
                422
            )
        response = make_response(
            mission.planet.to_dict(),
            201
        )
        return response
api.add_resource(Missions, '/missions')

if __name__ == '__main__':
    app.run(port=5000)
