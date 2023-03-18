from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import func

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    scientist=db.relationship('Scientist', back_populates='missions')
    planet=db.relationship('Planet', back_populates='missions')

    @validates('name')
    def validate_name(self,key,value):
        if not value:
            raise ValueError('Must have a name')
        return value

    @validates('scientist_id')
    def validate_scientist(self,key,value):
        if not value:
            raise ValueError('Must have a scientist')
        if Mission.query.filter_by(scientist_id=value, planet_id=self.planet_id).first():
            raise ValueError('Scientist already joined this mission')
        return value

    @validates('planet_id')
    def validate_planet(self,key,value):
        if not value:
            raise ValueError('Must have a planet')
        return value

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    field_of_study = db.Column(db.String)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    missions = db.relationship('Mission',back_populates='scientist')
    planets = association_proxy('missions', 'planet')

    @validates('name')
    def validate_name(self,key,value):
        if not value:
            raise ValueError('Must have a name')
        return value
    @validates('field_of_study')
    def validate_field_of_study(self,key,value):
        if not value:
            raise ValueError('Must have a field of study')
        return value


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    missions = db.relationship('Mission', back_populates='planet')
    scientists = association_proxy('missions', 'scientist')