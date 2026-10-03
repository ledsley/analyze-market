import pandas as pd

df = pd.read_csv('cars_dataset.csv')

test_rows = pd.DataFrame({'id':[11,12,13],'brand':['Ford','Kia','Focus'],'model':['Fiesta','Cerato','Ford'],'year':[1900,2032,2010],'mileage_km':[12456,111111111,0],'engine_l':[-1.0,0,11.0], 'fuel':['petrol','petrol','electric'],'transmission':['manual','manual','manual'],'city':['Taganrog','Taganrog','Taganrog'],'price_rub':[12345,0,-123]})

df_test = pd.concat([df.head(10),test_rows],ignore_index=True)