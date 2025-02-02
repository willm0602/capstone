from flask_sqlalchemy import SQLAlchemy
from numpy import ndarray
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd
from models import LungCancerDetectionModel, TestCase

DEFAULT_RANDOM_STATE = 35

def get_false_negative_rate(matrix: ndarray):
    """Takes in a confusion matrix and outputs the false negative rate"""
    false_negatives = matrix[1][0]
    total_cases = matrix[0][0] + matrix[0][1] + matrix[1][0] + matrix[1][1]
    return false_negatives / total_cases

def train(db, random_state: int = DEFAULT_RANDOM_STATE):
    """Trains a model to predict lung cancer using test cases in the database"""
    # Retrieve all test cases from the database
    testcases = TestCase.query.all()

    # Extract data into a dictionary directly
    data = {
        'gender': [tc.is_male for tc in testcases],
        'age': [tc.age for tc in testcases],
        'smoking': [tc.smoking for tc in testcases],
        'yellow_fingers': [tc.yellow_fingers for tc in testcases],
        'anxiety': [tc.anxiety for tc in testcases],
        'chronic_disease': [tc.chronic_disease for tc in testcases],
        'fatigue': [tc.fatigue for tc in testcases],
        'allergy': [tc.allergy for tc in testcases],
        'wheezing': [tc.wheezing for tc in testcases],
        'alcohol_consuming': [tc.alcohol_consuming for tc in testcases],
        'coughing': [tc.coughing for tc in testcases],
        'shortness_of_breath': [tc.shortness_of_breath for tc in testcases],
        'swallowing_difficulty': [tc.swallowing_difficulty for tc in testcases],
        'chest_pain': [tc.chest_pain for tc in testcases],
        'lung_cancer': [tc.lung_cancer for tc in testcases]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)
    x = df.drop(columns=['lung_cancer'])
    y = df['lung_cancer']

    # Split the dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=random_state
    )

    # Train a logistic regression model
    model = LogisticRegression(solver='lbfgs', max_iter=10000)
    model.fit(x_train, y_train)

    # Make predictions and evaluate the model
    y_pred = model.predict(x_test)
    overall_accuracy = accuracy_score(y_test, y_pred)
    model_confusion_matrix = confusion_matrix(y_test, y_pred)
    
    # https://stackoverflow.com/questions/31324218/scikit-learn-how-to-obtain-true-positive-true-negative-false-positive-and-fal
    false_negative_rate = get_false_negative_rate(model_confusion_matrix)
    dbmodel = LungCancerDetectionModel(
        model=model,
        false_negative_rate=false_negative_rate,
        overall_accuracy=overall_accuracy
    )
    db.session.add(dbmodel)
    db.session.commit()
    return dbmodel