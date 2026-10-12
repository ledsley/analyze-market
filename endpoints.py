from fastapi import FastAPI, Request
from pydantic import BaseModel,field_validator, FiniteFloat
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import date
import re

from main_dataframe import clear_df

from validation import convert_to_api_all

from stats import convert_to_api_stat,convert_to_api_brands_stats

from model_lr import convert_from_api,get_predict

class predcit_data(BaseModel):
    
    brand: str
    
    @field_validator('brand')
    def capitalize_brand(cls,value:str):
        if not value.split():
            raise ValueError('Некорректное название бренда')
        else:
            value = ' '.join(value.split())
            return value.title()

    model: str
    
    @field_validator('model')
    def capitalize_model(cls,value:str):
        if not value.split():
            raise ValueError('Некорректное название модели')
        else:
            value = ' '.join(value.split())
            return value.title()
    
    year: int
    
    @field_validator('year')
    def validate_year(cls,value:int):
        current_year = date.today().year
        if value <2008:
            raise ValueError('Год не может быть меньше 2008')
        if value > current_year:
            raise ValueError('Год не может быть больше текущего года')
        return value
    
    mileage_km: int
    
    @field_validator('mileage_km')
    def validate_mileage(cls, value:int):
        if value <= 0:
            raise ValueError('Пробег не может быть отрицательным или равным 0')
        if value >1000000:
            raise ValueError('Пробег не может быть больше миллиона')
        return value
            
    engine_l: FiniteFloat
    
    @field_validator('engine_l')
    def validate_engine(cls,value:float):
        if value <= 0:
            raise ValueError('Объем двигателя не может быть отрицательным или равным 0')
        if value >10.0:
            raise ValueError('Объем двигателя слишком большой')
        return value
    
    fuel: str
    
    @field_validator('fuel')
    def lower_fuel(cls,value:str):
        if not value.split():
            raise ValueError('Некорреткный тип топлива') 
        else:
            allowed_values = {'petrol','diesel','hybrid'}
            value = ''.join(value.split())
            value = value.lower()
            if value not in allowed_values:
                raise ValueError(f'Тип топлива не соответсвует допустимым значениям: {allowed_values}')
            else: return value
    
    transmission: str
    
    @field_validator('transmission')
    def lower_transmission(cls,value):
        if not value.split():
            raise ValueError('Некорректный тип КПП') 
        else:
            allowed_values = {'manual','automatic'}
            value = ''.join(value.split())
            value = value.lower()
            if value not in allowed_values:
                raise ValueError(f'Тип КПП не соответствует допустимым значениям: {allowed_values}')
            else: return value
    
    city: str
    
    @field_validator('city')
    def capitalize_city(cls,value:str):
        if not value.split():
            raise ValueError('Некорректное название города')
        else:
            value = ' '.join(value.split())
            value = re.sub(r'\s*-\s*','-',value)
            return value.title()    


def register_endpoints(app: FastAPI):
    
    @app.get('/')
    
    async def root():
        return {'message': 'Car Market Analyzer API'}
    
    @app.get('/cars')
    
    async def get_cars(brand: str | None = None, fuel: str | None = None, year_min: int | None = None, year_max: int | None = None):
        current_year = date.today().year
        
        if year_max is not None:
            if year_max < 1920 or year_max > current_year:
                raise HTTPException(status_code=400, detail=f'Некорректное значение максимального года: {year_max}') 
            
        if year_min is not None:
            if year_min > current_year or year_min < 1920:
                raise HTTPException(status_code=400,detail=f'Некорректное значение минимального года: {year_min}')
            
        if (year_min is not None) and (year_max is not None):
            if year_min > year_max:
                raise HTTPException(status_code=400, detail='Минимальный год не может быть больше максимального года')
            
        r = convert_to_api_all(clear_df,brand,fuel,year_min,year_max)
        if r:
            return r
        
        else: raise HTTPException(status_code=404, detail='Неправильно передан фильтр или такое значение отсутвует')

    @app.get('/stats')
    
    async def get_stats():
        return convert_to_api_stat(clear_df)
    
    @app.get('/stats/brands')
    
    async def get_stats_brand():
        return convert_to_api_brands_stats(clear_df,'')
    
    @app.get('/stats/brands/{brand}')
    
    async def get_stats_brand_choose(brand: str):
        r = convert_to_api_brands_stats(clear_df,brand)
        if r:
            return r
        else:
            raise HTTPException(status_code=404, detail='Неправильное название бренда или данный броенд отсутсвует')
    
    @app.post('/predict/')

    async def get_data_predict(data: predcit_data):
        r = convert_from_api(data.model_dump())
        if not r.empty:
            res = get_predict(r)
            return {'predicted_price': res}
        else:
            raise HTTPException(status_code=422,detail=f'Некорректная комбинация брэнда и модели: {data.brand,data.model}')
        
    @app.exception_handler(RequestValidationError)
    async def exception_engine(request: Request,exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                'error': 'Ошибка валидации данных',
                'fields': [
                    {
                        'loc': '.'.join(str(x) for x in err['loc']),
                        'msg': err['msg'],
                        'type': err['type'],
                    }
                    for err in exc.errors()
                ],
            },
        )