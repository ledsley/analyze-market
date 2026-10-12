import joblib
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent

model_file = base_dir / 'lr_model.joblib'

def convert_from_api(d):
    d = pd.json_normalize(d)

    return d

model = joblib.load(model_file)

def get_predict(car_data):
    prediction = model.predict(car_data)
    
    return prediction.item()