from typing import List
from flask import Blueprint, request, url_for
from flask import render_template

from chart_section import ChartSection

urls = Blueprint('urls', __name__, url_prefix='')

def static(path: str) -> str:
    """Shortcut for getting static URLs"""
    return url_for('static', filename=path)

@urls.route('/', methods=['GET'])
def index():
    return render_template('index.html', page_name='home')

@urls.route('/cancer_score')
def cancer_score():
    score = float(request.args.get('score') or '0')
    rounded_score = round(score, 4)
    print('rounded score is', rounded_score)
    return render_template('cancer_score.html', has_cancer = (score > 0.5))

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
