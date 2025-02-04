from typing import List
from flask import Blueprint, request, url_for
from flask import render_template
from flask import current_app

from chart_section import ChartSection

urls = Blueprint('urls', __name__, url_prefix='')
HAS_CANCER_THRESHOLD = 0.6 # score for determining if we want to report that they may have cancer

def static(path: str) -> str:
    """Shortcut for getting static URLs"""
    return url_for('static', filename=path)

@urls.route('/', methods=['GET'])
def index():
    return render_template('index.html', page_name='home')

@urls.route('/info', methods=['GET'])
def info():
    app = current_app
    model = app.config['MODEL']
    accuracy = round(model.overall_accuracy * 100, 2)
    false_negative_rate = model.false_negative_rate
    print('FALSE NEGATIVE RATE IS', false_negative_rate)
    false_negative_rate = round(false_negative_rate * 100, 2)
    return render_template('info.html', page_name='info', accuracy=accuracy, false_negative_rate=false_negative_rate)

@urls.route('/cancer_score')
def cancer_score():
    score = float(request.args.get('score') or '0')
    has_cancer = score > HAS_CANCER_THRESHOLD
    return render_template('cancer_score.html', has_cancer=has_cancer, page_name='home')

@urls.route('/charts', methods=['GET'])
def charts():
    chart_sections: List[ChartSection] = [
        {
            'name': 'Total People with Lung Cancer',
            'charts': [
                static('img/cancer.png'),
            ]
        },
        {
            'name': 'Gender',
            'charts': [
                static('img/male_cancer.png'),
                static('img/female_cancer.png'),
            ]
        },
        {
            'name': 'Smoking',
            'charts': [
                static('img/smokers.png'),
                static('img/nonsmokers.png')
            ]
        },
        {
            'name': 'Yellow Fingers',
            'charts': [
                static('img/yellowfingers.png'),
                static('img/normalfingers.png')
            ]
        },
        {
            'name': 'Anxiety',
            'charts': [
                static('img/anxiety.png'),
                static('img/no_anxiety.png'),
            ]
        },
        {
            'name': 'Chronic Disease',
            'charts': [
                static('img/chronic.png'),
                static('img/not_chronic.png')
            ]
        },
        {
            'name': 'Fatigue',
            'charts': [
                static('img/fatigue.png'),
                static('img/no_fatigue.png'),
            ]
        },
                {
            'name': 'Allergies',
            'charts': [
                static('img/allergies.png'),
                static('img/no_allergies.png'),
            ]
        },
        {
            'name': 'Wheezing',
            'charts': [
                static('img/wheezing.png'),
                static('img/no_wheezing.png'),
            ]
        },
        {
            'name': 'Alcohol Consumption',
            'charts': [
                static('img/drinks.png'),
                static('img/sober.png'),
            ]
        },
        {
            'name': 'Coughing',
            'charts': [
                static('img/coughing.png'),
                static('img/not_coughing.png'),
            ]
        },
        {
            'name': 'Shortness of Breath',
            'charts': [
                static('img/shortness_of_breath.png'),
                static('img/normal_breathing.png'),
            ]
        },
        {
            'name': 'Swallowing Difficulty',
            'charts': [
                static('img/swallows_fine.png'),
                static('img/swallow_issues.png'),
            ]
        },
        {
            'name': 'Chest Pain',
            'charts': [
                static('img/chest_pains.png'),
                static('img/no_chest_pains.png'),
            ]
        },
        {
            'name': 'Ages',
            'charts': [
                static('img/ages.png')
            ]
        }
    ]
    return render_template('charts.html', chart_sections=chart_sections, page_name='charts')
