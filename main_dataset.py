import pandas as pd
from pathlib import Path
from validation import validate_data

base_dir = Path(__file__).resolve().parent

cars_dataset = base_dir / 'cars_dataset.csv'

df = pd.read_csv(cars_dataset)

clear_df = validate_data(df)