from flask import current_app, redirect, render_template, url_for
from flask import Blueprint
from flask import request
from sklearn.linear_model import LogisticRegression
import pandas as pd

api = urls = Blueprint('api', __name__, url_prefix='/api')

def clean_form_data(obj: dict):
    cleaned_dict = {}
    for key, val in obj.items():
        if val == '0':
            val = False
        elif val == '1':
            val = True
        cleaned_dict[key] = val
    return cleaned_dict

@api.route('/analyze', methods=['POST'])
def evaluate():
    data = request.args
    data = clean_form_data(data)
    from models import LungCancerDetectionModel
    app = current_app
    model: LungCancerDetectionModel = app.config['MODEL']
    regression_model: LogisticRegression = model.model
    df = pd.DataFrame(data, index=[0])
    columns = regression_model.feature_names_in_
    df = df[columns]
    score = regression_model.predict_proba(df)[:,0][0] * 100
    score = round(score, 2)
    return {'score': score}
