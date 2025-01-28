from typing import List
from models import db
from flask import Flask
from load_testcases_from_csv import load_testcases_from_csv
from views import urls

SQLITE_PATH = 'sqlite:///./db.db'
app = Flask(__name__)

def get_test_cases() -> List:
    """Return all the input data"""
    from models import TestCase
    test_cases = TestCase.query.all()
    return test_cases

def bootstrap_data():
    """Loads data into our database from the CSV if it hasn't been loaded yet"""
    test_cases = get_test_cases()
    if not test_cases:
        load_testcases_from_csv(db)

def setup_app() -> Flask:
    """Constructs the flask application and does any pre-processing before the application is running"""

    # sets up the database
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_PATH
    db.init_app(app)
    with app.app_context():
        db.create_all()
        bootstrap_data()

        # create charts
        from build_charts import build_charts
        build_charts(db)

        # train model
        from train import train
        train()

    return app

app.register_blueprint(urls)

if __name__ == '__main__':
    app = setup_app()
    app.run(debug=True)