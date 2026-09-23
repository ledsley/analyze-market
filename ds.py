import pandas as pd

df = pd.read_csv('cars_dataset.csv')

test_rows = pd.DataFrame({'id':[11,12,13],'brand':['Ford','Kia','Focus'],'model':['Fiesta','Cerato','Ford'],'year':[1900,2032,2010],'mileage_km':[12456,111111111,0],'engine_l':[-1.0,0,11.0], 'fuel':['petrol','petrol','petrol'],'transmission':['manual','manual','manual'],'city':['Taganrog','Taganrog','Taganrog'],'price_rub':[12345,0,-123]})

df_test = pd.concat([df.head(10),test_rows],ignore_index=True)

#print(df_test)

#print(set(df['brand']))

#B4: год: >1900 <=2026, mileage: >0 <1000000, engine >0 <10.0 , price_rub >0 остальные подумать