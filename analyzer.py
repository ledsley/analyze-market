import pandas as pd

df = pd.read_csv('cars_dataset.csv')

df_mini = df.head(15)

#print(df_mini.loc[df_mini['brand'] == 'sob'].to_dict('records'))
#df_t = df.to_json(orient='table')
#df_mini = df_mini.loc[(df_mini['brand'] == 'Kia')]
#print(df_mini)
#df_mini= df_mini.loc[(df_mini['fuel'] == 'petrol')]

#print(df_mini)


#d = pd.DataFrame()
#cols_to_use = b.columns.difference(a.columns)

#c = pd.merge(a,b[cols_to_use],left_index=True,right_index=True)
#c = pd.merge(d,b[cols_to_use],left_index=True,right_index=True).to_dict('records')
#print(c)

col_n = list(df.columns)

for i in col_n:
    if df[i].isna().sum() != 0 :
        if df[i].dtypes == 'str':
            df[i] = df[i].fillna('Unknown')
        else: df[i] = df[i].fillna(0)