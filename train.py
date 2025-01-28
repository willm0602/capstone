from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd
from models import TestCase

def train():
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

    # Define features (X) and target (y)
    x = df.drop(columns=['lung_cancer'])
    y = df['lung_cancer']

    # Split the dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(x_train, y_train)

    # Make predictions and evaluate the model
    y_pred = model.predict(x_test)
    print('Accuracy:', accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
