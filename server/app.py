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
    pass
api.add_resource(Scientists,'/scientists')
class Planets(Resource):
    pass
api.add_resource(Planets,'/planets')
class Missions(Resource):
    pass
api.add_resource(Missions,'/missions')


if __name__ == '__main__':
    app.run(port=5555)
