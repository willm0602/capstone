from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class DBBase(DeclarativeBase):
    pass

DB = SQLAlchemy(model_class=DBBase)
SQLITE_PATH = 'sqlite:///db.db'

def setup_app(app: Flask) -> Flask:
    """Initializes the connection for the app to the database

    Parameters
    -----------
    app: Flask
        the Flask application we are connecting to the database
    """
    DB.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_PATH
    return app
