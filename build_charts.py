
from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from matplotlib import pyplot as plt
from typing import List
from models import TestCase
import pandas as pd

def make_pie_chart(
    title: str,
    labels: List[str],
    vals: List[float],
    path: str
):
    """Generates a piechart saved to a file"""
    plt.pie(vals, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.savefig(path)
    plt.close()

def make_gender_pie_chart():
    """Creates the pie-chart to show whether or not gender affects possibility of lung cancer"""
    make_comparison_chart(
        'is_male',
        'Male',
        'Female',
        'male_cancer.png',
        'female_cancer.png'
    )

def make_lung_cancer_chart() -> None:
    people_with_cancer = 0
    people_without_cancer = 0
    for test_case in TestCase.query.all():
        test_case: TestCase
        if test_case.lung_cancer:
            people_with_cancer+=1
        else:
            people_without_cancer+=1
    make_pie_chart(
        'People With Lung Cancer',
        ['With Cancer', 'Without Cancer'],
        [people_with_cancer, people_without_cancer],
        './static/img/cancer.png'
    )

def make_comparison_chart(
    field_name,
    true_label,
    false_label,
    true_file_name,
    false_file_name
):
    people_with_field_with_cancer = 0
    people_without_field_with_cancer = 0
    people_with_field_without_cancer = 0
    people_without_field_without_cancer = 0

    for tc in TestCase.query.all():
        tc: TestCase
        val = getattr(tc, field_name, None)
        if val is None:
            raise ValueError(f'Missing field {field_name} on TestCase')
        if val:
            if tc.lung_cancer:
                people_without_field_with_cancer+=1
            else:
                people_without_field_without_cancer+=1
        else:
            if tc.lung_cancer:
                people_with_field_with_cancer+=1
            else:
                people_with_field_without_cancer+=1

    make_pie_chart(
        true_label,
        ['With Cancer', 'Without Cancer'],
        [people_with_field_with_cancer, people_with_field_without_cancer],
        f'./static/img/{true_file_name}'
    )

    make_pie_chart(
        false_label,
        ['With Cancer', 'Without Cancer'],
        [people_without_field_with_cancer, people_without_field_without_cancer],
        f'./static/img/{false_file_name}'
    )

def make_smoking_charts() -> None:
    make_comparison_chart(
        'smoking',
        'Smokes',
        'Doesn\'t Smoke',
        'smokers.png',
        'nonsmokers.png'
    )

def make_yellow_fingers_charts() -> None:
    make_comparison_chart(
        'yellow_fingers',
        'Has Yellow Fingers',
        'Don\'t Have Yellow Fingers',
        'yellowfingers.png',
        'normalfingers.png'
    )

def make_anxiety_charts() -> None:
    make_comparison_chart(
        'anxiety',
        'Has Anxiety',
        'Doesn\'t Have Anxiety',
        'anxiety.png',
        'no_anxiety.png'
    )

def make_chronic_disease_charts() -> None:
    make_comparison_chart(
        'chronic_disease',
        'Has Chronic Disease',
        'Doesn\'t Have Chronic Disease',
        'chronic.png',
        'not_chronic.png'
    )

def make_fatigue_charts() -> None:
    make_comparison_chart(
        'fatigue',
        'Has Fatigue',
        'Doesn\'t Have Fatigue',
        'fatigue.png',
        'no_fatigue.png'
    )

def make_allergy_charts() -> None:
    make_comparison_chart(
        'allergy',
        'Has Allergies',
        'Doesn\'t Have Allergies',
        'allergies.png',
        'no_allergies.png'
    )

def make_wheezing_charts() -> None:
    make_comparison_chart(
        'wheezing',
        'Wheezing',
        'Not Wheezing',
        'wheezing.png',
        'no_wheezing.png'
    )

def make_drinking_charts() -> None:
    make_comparison_chart(
        'alcohol_consuming',
        'Drinks Alcohol',
        'Doesn\'t Drink',
        'drinks.png',
        'sober.png'
    )

def make_coughing_charts() -> None:
    make_comparison_chart(
        'coughing',
        'Coughing',
        'Not Coughing',
        'coughing.png',
        'not_coughing.png'
    )

def make_shortness_of_breath_charts() -> None:
    make_comparison_chart(
        'shortness_of_breath',
        'Shortness of Breath',
        'Normal Breathing',
        'shortness_of_breath.png',
        'normal_breathing.png'
    )

def make_swallowing_difficulty_charts() -> None:
    make_comparison_chart(
        'swallowing_difficulty',
        'Has Trouble Swallowing',
        'Swallows Fine',
        'swallow_issues.png',
        'swallows_fine.png'
    )

def make_chest_pain_charts() -> None:
    make_comparison_chart(
        'chest_pain',
        'Has Chest Pains',
        'Doesn\'t Have Chest Pains',
        'chest_pains.png',
        'no_chest_pains.png'
    )

def make_age_charts() -> None:
    with_cancer = [0 for _ in range(12)]
    without_cancer = [0 for _ in range(12)]
    for tc in TestCase.query.all():
        tc: TestCase
        age_range = tc.age // 10 if tc.age <= 120 else 11
        if tc.lung_cancer:
            with_cancer[age_range]+=1
        else:
            without_cancer[age_range]+=1
    age_ranges = [f'{10*i} - {11*i-1}' for i in range(12)]
    data = {
        'Age Ranges': age_ranges,
        'With Cancer': with_cancer,
        'Without Cancer': without_cancer
    }

    df = pd.DataFrame(data)
    df.set_index('Age Ranges', inplace=True)
    ax = df.plot(kind='bar', figsize=(8,6), color=['skyblue', 'orange'])
    plt.title('Ages vs Cancer', fontsize=16)
    plt.xlabel('Ages', fontsize=12)
    plt.ylabel('# of People w/ Cancer', fontsize=12)
    plt.legend(title='Cancer Status')
    plt.tight_layout()
    plt.savefig('./static/img/ages.png')
    plt.close()

def build_charts(db: SQLAlchemy) -> None:
    make_lung_cancer_chart()
    make_gender_pie_chart()
    make_smoking_charts()
    make_yellow_fingers_charts()
    make_anxiety_charts()
    make_chronic_disease_charts()
    make_fatigue_charts()
    make_allergy_charts()
    make_wheezing_charts()
    make_drinking_charts()
    make_coughing_charts()
    make_shortness_of_breath_charts()
    make_swallowing_difficulty_charts()
    make_chest_pain_charts()
    make_age_charts()