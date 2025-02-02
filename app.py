from typing import List
from models import db
from flask import Flask
from load_testcases_from_csv import load_testcases_from_csv
from views import urls
from api import api

SQLITE_PATH = 'sqlite:///./db.db'
TOLERABLE_ACCURACY = 0.9
TOLERABLE_FALSE_NEGATIVES = 0.05

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
        from models import TestCase
        from models import LungCancerDetectionModel
        def model_is_not_acceptable(model: None | LungCancerDetectionModel):
            if model is None:
                return True
            if model.overall_accuracy < TOLERABLE_ACCURACY:
                return True
            if model.false_negative_rate > TOLERABLE_FALSE_NEGATIVES:
                return True
            return False

        # generate an acceptable model to be used
        models = LungCancerDetectionModel.query.all()
        model = models[-1] if len(models) > 0 else None
        random_state = 1
        while model_is_not_acceptable(model):
            model = train(db, random_state)
            random_state+=1
        app.config['MODEL'] = model

    return app

app.register_blueprint(urls)
app.register_blueprint(api)

if __name__ == '__main__':
    app = setup_app()
    app.run(debug=True)