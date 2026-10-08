import pandas as pd

from validation import validate_data

df = pd.read_csv('cars_dataset.csv')

df_mini = df.head(15)

df_test_num = pd.read_csv('cars_all_wrong_number_column.csv')

df_test_cat = pd.read_csv('cars_all_wrong_category_column.csv')

df_test_comb = pd.read_csv('cars_wrong_combinations.csv')

df_test_nans = pd.read_csv('cars_nans.csv')

num_expected = pd.read_csv('cars_all_wrong_number_column_expected.csv')

cat_expected = pd.read_csv('cars_all_wrong_category_column_expected.csv')

comb_expected = pd.read_csv('cars_wrong_combinations_expected.csv')

nans_expected = pd.read_csv('cars_nans_expected.csv')

clear_df = validate_data(df)

clear_df_mini = validate_data(df_mini)