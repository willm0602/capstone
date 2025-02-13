import csv
FILE_NAME = './data.csv'

def parse_gender(row: dict) -> bool:
    """returns if the individuals sex is male or female"""
    gender = row.get('GENDER')
    if gender is None or gender not in 'MF':
        raise ValueError(f'Input gender {gender} from the dataset must be M or F')
    return gender == 'M'

def parse_1_2(row: dict, field_name: str) -> bool:
    """Some of the data from the dataset is represented as 1
    for false and 2 for true

    Parameters
    ----------------
    row: dictionary
        dictionary representing individuals
    field_name: str
        field in the row that we are parsing
    """
    field_name = field_name.strip()
    val = row.get(field_name)
    if val == '1':
        return False
    if val == '2':
        return True
    raise ValueError(f'Trying to read {field_name} of row: {val} is not 1 or 2')

def parse_yes_no(row, field_name):
    """Returns if the value of a row is 'yes' or 'no'

    Parameters
    ----------------
    row: dictionary
        dictionary representing individuals
    field_name: str
        field in the row that we are parsing
    """
    field_name = field_name.strip()
    val = row.get(field_name)
    if val == 'YES':
        return False
    if val == 'NO':
        return True
    raise ValueError(f'Trying to read {field_name} of row: {val} is not YES or NO')

def load_testcases_from_csv(db):
    from models import TestCase

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            test_case_data = {
                'is_male': parse_gender(row),
                'age': row['AGE'],
                'smoking': parse_1_2(row, 'SMOKING'),
                'yellow_fingers': parse_1_2(row, 'YELLOW_FINGERS'),
                'anxiety': parse_1_2(row, 'ANXIETY'),
                'peer_pressure': parse_1_2(row, 'PEER_PRESSURE'),
                'chronic_disease': parse_1_2(row, 'CHRONIC DISEASE'),
                'fatigue': parse_1_2(row, 'FATIGUE'),
                'allergy': parse_1_2(row, 'ALLERGY'),
                'wheezing': parse_1_2(row, 'WHEEZING'),
                'alcohol_consuming': parse_1_2(row, 'ALCOHOL CONSUMING'),
                'coughing': parse_1_2(row, 'COUGHING'),
                'shortness_of_breath': parse_1_2(row, 'SMOKING'),
                'swallowing_difficulty': parse_1_2(row, 'SMOKING'),
                'chest_pain': parse_1_2(row, 'SMOKING'),
                'lung_cancer': parse_yes_no(row, 'LUNG_CANCER')
            }
            test_case = TestCase(**test_case_data)
            db.session.add(test_case)

        db.session.commit()
