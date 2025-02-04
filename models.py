from typing import List
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class DBBase(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=DBBase)
SQLITE_PATH = 'sqlite:///./db.db'

class TestCase(db.Model):
    """Represents one case of an individual that may or may
    or may not have lung cancer."""

    id = db.Column(db.Integer, primary_key=True)
    is_male = db.Column(db.Boolean, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    smoking = db.Column(db.Boolean, nullable=False)
    yellow_fingers = db.Column(db.Boolean, nullable=False)
    anxiety = db.Column(db.Boolean, nullable=False)
    peer_pressure = db.Column(db.Boolean, nullable=False)
    chronic_disease = db.Column(db.Boolean, nullable=False)
    fatigue = db.Column(db.Boolean, nullable=False)
    allergy = db.Column(db.Boolean, nullable=False)
    wheezing = db.Column(db.Boolean, nullable=False)
    alcohol_consuming = db.Column(db.Boolean, nullable=False)
    coughing = db.Column(db.Boolean, nullable=False)
    shortness_of_breath = db.Column(db.Boolean, nullable=False)
    swallowing_difficulty = db.Column(db.Boolean, nullable=False)
    chest_pain = db.Column(db.Boolean, nullable=False)
    lung_cancer = db.Column(db.Boolean, nullable=False)

class LungCancerDetectionModel(db.Model):
    """Represents a model that can be used to determine
    if an individual has lung cancer or not"""
    id = db.Column(db.Integer, primary_key=True)
    overall_accuracy= db.Column(db.Float, nullable=False)
    false_negative_rate = db.Column(db.Float, nullable=False)
    # https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.PickleType
    model = db.Column(db.PickleType, nullable=False)

def connect_to_db(app: Flask) -> Flask:
    """Initializes the connection for the app to the database

    Parameters
    -----------
    app: Flask
        the Flask application we are connecting to the database
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_PATH
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
