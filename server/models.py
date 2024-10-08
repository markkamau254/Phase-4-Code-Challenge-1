# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.orm import validates
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin

# metadata = MetaData(naming_convention={
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
# })

# db = SQLAlchemy(metadata=metadata)


# class Hero(db.Model, SerializerMixin):
#     __tablename__ = 'heroes'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     super_name = db.Column(db.String)

#     # add relationship
#     hero_powers = db.relationship('HeroPower', backref='hero')
#     powers = association_proxy('hero_powers', 'power')

#     # add serialization rules
#     serialize_rules = ('-hero_powers.hero',)

#     def __repr__(self):
#         return f'<Hero {self.id}>' 


# class Power(db.Model, SerializerMixin):
#     __tablename__ = 'powers'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     description = db.Column(db.String)

#     # add relationship
#     hero_powers = db.relationship('HeroPower', backref='power')
#     heroes = association_proxy('hero_powers', 'hero')

#     # add serialization rules
#     serialize_rules = ('-hero_powers.power',)

#     # add validation
#     @validates('description')
#     def validate_description(self, key, description):
#         if len(description) < 20:
#             raise ValueError("Description must be at least 20 characters long.")
#         return description

#     def __repr__(self):
#         return f'<Power {self.id}>'


# class HeroPower(db.Model, SerializerMixin):
#     __tablename__ = 'hero_powers'

#     id = db.Column(db.Integer, primary_key=True)
#     strength = db.Column(db.String, nullable=False)

#     # add relationships
#     hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
#     power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
#     hero = db.relationship('Hero', backref='hero_powers')
#     power = db.relationship('Power', backref='hero_powers')

#     # add serialization rules
#     serialize_rules = ('-hero.hero_powers', '-power.hero_powers',)


#     # add validation
#     @validates('strength')
#     def validate_strength(self, key, strength):
#         if strength not in ['Strong', 'Weak', 'Average']:
#             raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
#         return strength

#     def __repr__(self):
#         return f'<HeroPower {self.id}>'

#######################################################################################################
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Metadata for SQLAlchemy to manage naming conventions for constraints.
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy with the metadata.
db = SQLAlchemy(metadata=metadata)

# Define the Hero model.
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Relationship with HeroPower, used to access associated powers through HeroPower.
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')
    powers = association_proxy('hero_powers', 'power')

    # Serialization rules to avoid recursion.
    serialize_rules = ('-hero_powers.hero',)

    def __repr__(self):
        return f'<Hero {self.id} - {self.name} aka {self.super_name}>'


# Define the Power model.
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # Relationship with HeroPower, used to access associated heroes through HeroPower.
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan')
    heroes = association_proxy('hero_powers', 'hero')

    # Serialization rules to avoid recursion.
    serialize_rules = ('-hero_powers.power',)

    # Validate the description to ensure it has at least 20 characters.
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description

    def __repr__(self):
        return f'<Power {self.id} - {self.name}>'


# Define the HeroPower model, representing the association between Hero and Power.
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)

    # Foreign keys to link to Hero and Power.
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # Serialization rules to avoid recursion.
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers',)

    # Validate the strength to ensure it is 'Strong', 'Weak', or 'Average'.
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id} - {self.hero.name} with {self.power.name} at {self.strength} strength>'
