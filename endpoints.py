from fastapi import FastAPI
from fastapi import HTTPException
from datetime import date

from analyzer import df, df_mini

from ds import df_test,df_test_nans

from fucntions import convert_to_api_all #convert_to_api_cars

from stats import convert_to_api_stat,convert_to_api_brands_stats

def register_endpoints(app: FastAPI):
    
    @app.get('/')
    
    async def root():
        return {'message': 'Car Market Analyzer API'}
    
    @app.get('/cars')
    
    async def get_cars(brand: str | None = None, fuel: str | None = None, year_min: int | None = None, year_max: int | None = None):
        current_year = date.today().year
        
        if year_max is not None:
            if year_max < 1920 or year_max > current_year:
                raise HTTPException(status_code=400, detail=f'Некорректное ограничение максимального года: {year_max}') 
            
        if year_min is not None:
            if year_min > current_year or year_min < 1920:
                raise HTTPException(status_code=400,detail=f'Некорректное ограничение минимального года: {year_min}')
            
        if (year_min is not None) and (year_max is not None):
            if year_min > year_max:
                raise HTTPException(status_code=400, detail='Минимальный год не может быть больше максимального года')
            
        r = convert_to_api_all(df_mini,brand,fuel,year_min,year_max)
        if r:
            return r
        
        else: raise HTTPException(status_code=404, detail='Неправильно передан фильтр или такое знеачение отсутвует')

    @app.get('/stats')
    
    async def get_stats():
        return convert_to_api_stat(df_test_nans)
    
    @app.get('/stats/brands')
    
    async def get_stats_brand():
        return convert_to_api_brands_stats(df_mini,'')
    
    @app.get('/stats/brands/{brand}')
    
    async def get_stats_brand_choose(brand: str):
        r = convert_to_api_brands_stats(df_mini,brand)
        if r:
            return r
        else:
            raise HTTPException(status_code=404, detail='Неправильное название бренда или данный броенд отсутсвует')