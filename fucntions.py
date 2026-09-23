import pandas as pd

from analyzer import df

from ds import df_test

from datetime import date

values = pd.read_csv('allowed_values.csv')

numeric_columns = {'year','price_rub','engine_l','mileage_km'}

categorial_columns = {'city','brand','model','fuel','transmission'}

def check_column_datatype(column):
    if column.name in numeric_columns:isnumeric_data(column)
    elif column.name in categorial_columns: iscategorial_data(column)
    else: print(f'Неверная колнка: {column.name}')

wrong_numeric_datatype = set()

wrong_categorial_datatype = set()

def isnumeric_data(column):
    if not pd.api.types.is_numeric_dtype(column):
        print(f'неправльный тип данных: {column.dtypes}')
        wrong_numeric_datatype.add(column.name)
    else: print('success') 
    
def iscategorial_data(column):
    if not pd.api.types.is_string_dtype(column):
        print(f'неправльный тип данных: {column.dtypes}')
        wrong_categorial_datatype.add(column.name)
    else: print('success')
    

def check_data(column):
    if column.name in numeric_columns:
        check_numeric_data(column)
        
def check_numeric_data(column):
    if column.name == 'year':
        if any(x <= 1920 or x > date.today().year for x in column):
            #return column.loc[column <=1920 or column > date.today().year].index.tolist()
            print(f'Некорректынй год авто: {column.loc[(column <=1920) | (column > date.today().year)].index.tolist()}')
    elif column.name == 'engine_l':
        if any(x <=0 or x >10.0 for x in column):
            #return column.loc[column <=0 or column >10].index.tolist()
            print(f'Некорректный объем двигателя: {column.loc[(column <=0) | (column > 10.0)].index.tolist()}')
    elif column.name == 'mileage_km':
        if any(x <=0 or x > 1000000 for x in column):
            #return column.loc[column <= 0 or column > 1000000].index.tolist()
            print(f'Некорректный пробег: {column.loc[(column <= 0) | (column > 1000000)].index.tolist()}')
    elif column.name == 'price_rub':
        if any(x <=0 for x in column):
            #return column.loc[column <= 0].index.tolist()
            print(f'Некорреткная цена: {column.loc[column <= 0].index.tolist()}')

def check_categorial_data(column):
    s = set(values['value'].loc[values['column'] == column.name])
    if any(x not in s for x in column):
        l = set(column)
        wrong_v = []
        for x in l:
            if x not in s:
                wrong_v.append(x)     
        print(f'Неккореткное значение: {wrong_v}')
        
check_categorial_data(df_test['brand'])