from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

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
    def post(self):
        data = request.get_json()
        try:
            scientist = Scientist(
                name=data['name'],
                field_of_study=data['field_of_study'],
                avatar=data['avatar']
            )
            db.session.add(scientist)
            db.session.commit()
        except Exception as e:
            message = {
                "errors": [e.__str__()]
            }
            return make_response(
                message,
                422
            )
        response = make_response(
            scientist.to_dict(),
            201
        )
        return make_response
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
api.add_resource(ScientistById, '/scientists/<int:id>')

class Planets(Resource):
    pass
api.add_resource(Planets,'/planets')

class Missions(Resource):
    pass
api.add_resource(Missions,'/missions')


if __name__ == '__main__':
    app.run(port=5000)
