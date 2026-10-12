import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent

cars_wrong_number_column = base_dir / 'cars_all_wrong_number_column.csv'

cars_wrong_category_column = base_dir / 'cars_all_wrong_category_column.csv'

cars_wrong_combinations = base_dir / 'cars_wrong_combinations.csv'

cars_nans = base_dir / 'cars_nans.csv'

cars_wrong_number_column_expected = base_dir / 'cars_all_wrong_number_column_expected.csv'

cars_wrong_category_column_expected = base_dir / 'cars_all_wrong_category_column_expected.csv'

cars_wrong_combinations_expected = base_dir / 'cars_wrong_combinations_expected.csv'

cars_nans_expected = base_dir / 'cars_nans_expected.csv'

df_test_num = pd.read_csv(cars_wrong_number_column)

df_test_cat = pd.read_csv(cars_wrong_category_column)

df_test_comb = pd.read_csv(cars_wrong_combinations)

df_test_nans = pd.read_csv(cars_nans)

num_expected = pd.read_csv(cars_wrong_number_column_expected)

cat_expected = pd.read_csv(cars_wrong_category_column_expected)

comb_expected = pd.read_csv(cars_wrong_combinations_expected)

nans_expected = pd.read_csv(cars_nans_expected)