import pandas as pd

from analyzer import df

from ds import df_test

from datetime import date

allowed_cat_values = pd.read_csv('allowed_values.csv')

allowed_combinations = {('brand','model') :set(df['brand'] + df['model']), 
                        ('engine_l','fuel') : set(df['engine_l'].astype(str) + df['fuel']),
                        ('model','year'): set(df['model'] + df['year'].astype(str))}

numeric_columns = {'year','price_rub','engine_l','mileage_km'}

categorial_columns = {'city','brand','model','fuel','transmission'}

def isnumeric_data(column):
    if not pd.api.types.is_numeric_dtype(column):
        return column.name
    
def iscategorial_data(column):
    if not pd.api.types.is_string_dtype(column):
        return column.name

def check_data(column):
    if column.name in numeric_columns:
        return check_numeric_data(column)
    elif column.name in categorial_columns:
        return check_categorial_data(column)
        
def check_numeric_data(column):
    if column.name == 'year':
        if any(x <= 1920 or x > date.today().year for x in column):
            #print(f'Некорректынй год авто: {column.loc[(column <=1920) | (column > date.today().year)].index.tolist()}')
            return {column.name : column.loc[(column <=1920) | (column > date.today().year)].index.tolist()}
        #else: return []
            
    elif column.name == 'engine_l':
        if any(x <=0 or x >10.0 for x in column):
            #print(f'Некорректный объем двигателя: {column.loc[(column <=0) | (column > 10.0)].index.tolist()}')
            return {column.name : column.loc[(column <=0) | (column >10)].index.tolist()}
        #else: return []
            
    elif column.name == 'mileage_km':
        if any(x <=0 or x > 1000000 for x in column):
            #print(f'Некорректный пробег: {column.loc[(column <= 0) | (column > 1000000)].index.tolist()}')
            return {column.name : column.loc[(column <= 0) | (column > 1000000)].index.tolist()}
        #else: return []
            
    elif column.name == 'price_rub':
        if any(x <=0 for x in column):
            #print(f'Некорреткная цена: {column.loc[column <= 0].index.tolist()}')
            return {column.name : column.loc[column <= 0].index.tolist()}
        #else: return []

    return []                

def check_categorial_data(column):
    s = set(allowed_cat_values['value'].loc[allowed_cat_values['column'] == column.name])
    if any(x not in s for x in column):
        wrong_v = {}
        for x in column:
            if x not in s:
                wrong_v.update({column.name :column.loc[column == x].index.item()})     
        return wrong_v
    #else: return []

def check_combinations(c1,c2):
    key_name = (c1.name,c2.name)
    if key_name in allowed_combinations:
        combinations = set(c1.astype(str) + c2.astype(str))
        wrong_combinations = set()
        for n in combinations:
            if n not in allowed_combinations[key_name]:
                wrong_combinations.add(n)
        if not wrong_combinations:
            return {}
        else:
            indexes = []
            for i in range(len(c1)):
                    if str(c1[i])+str(c2[i]) in wrong_combinations:
                        indexes.append(i)
            return indexes
    else: return {}
    
d_test = df_test
#print(d_test)
def validate_data(d):
    d.drop_duplicates(inplace = True)
    
    wrong_categorial_datatype = set()
    wrong_numeric_datatype = set()
    
    for n in d:
        if n == 'id':
            continue
        if n in numeric_columns:
            r = isnumeric_data(d[n])
            if r:
                wrong_numeric_datatype.add(r)
        elif n in categorial_columns:
            r = iscategorial_data(d[n])
            if r:
                wrong_categorial_datatype.add(r)
    
    if wrong_categorial_datatype:
        for x in wrong_categorial_datatype:
            d[x] = d[x].astype('string')
            if d[x].dropna().empty:
                if x == 'brand':
                    d[x] = 'Kia'
                elif x == 'model':
                    d[x] = 'Cerato'
                elif x == 'fuel':
                    d[x] = 'petrol'
                elif x == 'transmission':
                    d[x] = 'manual'
                elif x == 'city':
                    d[x] = 'Moscow'
            d[x] = d[x].fillna(d[x].dropna().mode()[0])
    if wrong_numeric_datatype:
        for x in wrong_numeric_datatype:
            d[x] = pd.to_numeric(d[x],errors='coerce')
            if pd.api.types.is_float_dtype(d[x]):
                a =1
            else: a =0

            if d[x].notnull().any():
                d[x] = d[x].fillna(round(d[x].dropna().mean(),a))
            else:
                if x == 'year':
                    d[x] = d[x].fillna(2000)
                elif x == 'engine_l':
                    d[x] = d[x].fillna(1.6)
                elif x == 'mileage_km':
                    d[x] = d[x].fillna(500000)
                elif x == 'price_rub':
                    d[x] = d[x].fillna(1000000)

    data_replace_indexes = {}
    for n in d:
        if n == 'id':
            continue
        r = check_data(d[n])
        if r:
            data_replace_indexes.update(r)
        
    for k,v in data_replace_indexes.items():
        if k in categorial_columns:
            if d[k].drop(v).empty:
                if k == 'brand':
                    d[k] = 'Kia'
                elif k == 'model':
                    d[k] = 'Cerato'
                elif k == 'fuel':
                    d[k] = 'petrol'
                elif k == 'transmission':
                    d[k] = 'manual'
                elif k == 'city':
                    d[k] = 'Moscow'
            else:
                if isinstance(v,list):
                    for x in v:
                        d.loc[x,k] = d[k].drop(v).mode()[0] 
                else:
                    d.loc[v,k] = d[k].drop(v).mode()[0]
        else:
            if pd.api.types.is_float_dtype(d[k]):
                a = 1
            else: a =0
            
            if d[k].drop(v).empty:
                if k == 'year':
                    d[k] = 2000
                elif k == 'engine_l':
                    d[k] = 1.6
                elif k == 'mileage_km':
                    d[k] = 500000
                elif k == 'price_rub':
                    d[k] = 1000000
            else:
                if isinstance(v,list):
                    for x in v:
                        d.loc[x,k] = round(d[k].drop(v).mean(),a)
                else:d.loc[v,k] = round(d[k].drop(v).mean(),a)
            
        
    data_del_indexes = []
    
    for key in allowed_combinations:
        data_del_indexes.append(check_combinations(d[key[0]],d[key[1]])) 
     
    data_del_indexes = list(set([i for sl in data_del_indexes for i in sl]))
      
    d.drop(data_del_indexes,inplace = True)
         
    return d 
        
validate_data(d_test)

print(d_test)