import pandas as pd
   
def calculate_stat(d):
    stat = d.agg(
        count = ('price_rub','count'),
        price_min = ('price_rub', 'min'),
        price_max = ('price_rub', 'max'),
        price_mean = ('price_rub', 'mean'),
        price_median = ('price_rub','median'),
        mileage_mean = ('mileage_km', 'mean'),
        year_mean = ('year','mean')
    ).round(0)
    
    return stat

def brand_stats(d):
    brands = d.groupby('brand')
    
    brand_s = calculate_stat(brands)
        
    return brand_s

def calculate_price_by_year(d):
    years = d.groupby('year').agg(mean_price = ('price_rub','mean')).round(0)
    
    return years

def range_mileage(d):
    ranges = pd.cut(d['mileage_km'],bins = range(0,1000001,100000)).value_counts(sort = False)
    
    return ranges

def stat_cat(d,column_name):
    stat = d[column_name].value_counts()
    
    return stat

def convert_to_api_stat(d):
    res = calculate_stat(d)

    v = dict()
    for idx,row in res.iterrows():
        v[idx] = row.dropna().item()
        
    return v

def convert_to_api_brands_stats(d,brand_name:str):
    res = brand_stats(d)
    idxs = set(res.index.tolist())
    if not brand_name:
        vals = dict()
        for idx,row in res.iterrows():
            vals[idx] = row.to_dict()
            
        return vals
    
    elif brand_name in idxs:
        vals = dict()
        vals[brand_name] = res.loc[brand_name].to_dict()

        return vals