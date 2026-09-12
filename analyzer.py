import pandas as pd

df = pd.read_csv('cars_dataset.csv')

#print(df)

print(df.shape) #размер таблицы(фалйа) в виде строка*столбцы
col_n = list(df.columns)
print(col_n) #названия столбцов
print(df.isna().sum()) #пропущенные значения
for i in col_n:
    if df[i].isna().sum() != 0 :
        if df[i].dtypes == 'str':
            df[i] = df[i].fillna('Unknown')
        else: df[i] = df[i].fillna(0)


print(df.dtypes) #типы данных столбцов
for i in col_n:
    print(df[i].unique())

print(df.head(3)) #несколько первых строк