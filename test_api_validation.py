from fastapi.testclient import TestClient
from api import app
from datetime import date
import pandas as pd

from validation import validate_data
from datasets_for_tests import df_test_num,df_test_nans,df_test_cat,df_test_comb,nans_expected,num_expected,cat_expected,comb_expected

current_year = date.today().year

client = TestClient(app)

b = 'Kia'
f = 'diesel'
y_m = 2012

def test_get_cars():
    response = client.get('/cars')
    data = response.json()
    assert response.status_code == 200
    assert data
    assert isinstance(data,list)

def test_get_cars_filters():
    response = client.get(f'/cars?brand={b}&fuel={f}&year_min={y_m}')
    data = response.json()
    assert response.status_code == 200
    assert data
    assert isinstance(data,list)
    for i in data:
        assert i['year']>= y_m
        assert i['brand']== b
        assert i['fuel'] == f
        
def test_invalid_year_type():
    response = client.get('/cars?year_min=hello')
    assert response.status_code == 422
    
def test_invalid_fliter():
    response = client.get('/cars?brand=sob')
    assert response.status_code == 404
    assert  response.json() == {'detail':'Неправильно передан фильтр или такое значение отсутвует'}
    
def test_invalid_max_year():
    for year_max in (1910,current_year+1):
        response = client.get(f'/cars?year_max={year_max}')
        assert response.status_code == 400
        assert response.json() == {'detail':f'Некорректное значение максимального года: {year_max}'}
    
def test_invalid_min_year():
    for year_min in (1910,current_year+1):
        response = client.get(f'/cars?year_min={year_min}')
        assert response.status_code == 400
        assert response.json() == {'detail':f'Некорректное значение минимального года: {year_min}'}
        
def test_invalid_max_min_years():
    response = client.get('/cars?year_min=2020&year_max=2010')
    assert response.status_code == 400
    assert response.json() == {'detail':'Минимальный год не может быть больше максимального года'}
    
def test_validation_from_validation():
    test_cases =((df_test_comb,comb_expected),
                 (df_test_cat,cat_expected),
                 (df_test_nans,nans_expected),
                 (df_test_num,num_expected))
   
    for data,expected in test_cases:
        res = validate_data(data.copy())
        pd.testing.assert_frame_equal(res,expected)
        
def test_api_city_validation():
    response_city = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "saint   -    petersburg   "
                                                    })
    assert response_city.status_code == 200
    
    response_city_empty = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": ""
                                                    })
    assert response_city_empty.status_code == 422
    
def test_api_brand_validation():
    response_brand = client.post('/predict',json = {
                                                    "brand": "ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_brand.status_code == 200
        
    response_brand_empty = client.post('/predict',json = {
                                                    "brand": "",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_brand_empty.status_code == 422
    
def test_api_model_validation():
    response_model = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_model.status_code == 200
        
    response_model_empty = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_model_empty.status_code == 422
    
def test_api_fuel_validation():
    response_fuel = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "Petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_fuel.status_code == 200
        
    response_fuel_empty = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_fuel_empty.status_code == 422
    
    response_fuel_wrong_name = client.post('/predict',json = {
                                                        "brand": "Ford",
                                                        "model": "Focus",
                                                        "year": 2008,
                                                        "mileage_km": 137000,
                                                        "engine_l": 1.6,
                                                        "fuel": "water",
                                                        "transmission": "manual",
                                                        "city": "Moscow"
                                                        })
    assert response_fuel_wrong_name.status_code == 422
    
def test_api_transmission_validation():
    response_transmission = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "Manual",
                                                    "city": "Moscow"
                                                    })
    assert response_transmission.status_code == 200
        
    response_transmission_empty = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "",
                                                    "city": "Moscow"
                                                    })
    assert response_transmission_empty.status_code == 422
    
    response_transmission_wrong = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "sobasd",
                                                    "city": "Moscow"
                                                    })
    assert response_transmission_wrong.status_code == 422
    
def test_api_year_validation():
    response_year = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_year.status_code == 200
        
    response_year_wrong_less = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 20,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_year_wrong_less.status_code == 422
    
    response_year_wrong_greater = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": current_year+1,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_year_wrong_greater.status_code == 422
    
    response_year_empty = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": '',
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_year_empty.status_code == 422
    
def test_api_mileage_validation():
    response_mileage = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_mileage.status_code == 200
        
    response_mileage_wrong_less = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": -137,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_mileage_wrong_less.status_code == 422
    
    response_mileage_wrong_greater = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 1037000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_mileage_wrong_greater.status_code == 422
    
    response_mileage_empty = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": '',
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_mileage_empty.status_code == 422


def test_api_engine_validation():
    response_engine = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_engine.status_code == 200
        
    response_engine_wrong_less = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": -1.6,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_engine_wrong_less.status_code == 422
    
    response_engine_wrong_greater = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 15.0,
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_engine_wrong_greater.status_code == 422
    
    response_engine_empty = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": '',
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_engine_empty.status_code == 422
    
    response_engine_nan = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 'nan',
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_engine_nan.status_code == 422
    
    response_engine_NaN = client.post('/predict',json = {
                                                    "brand": "Ford",
                                                    "model": "Focus",
                                                    "year": 2008,
                                                    "mileage_km": 137000,
                                                    "engine_l": 'NaN',
                                                    "fuel": "petrol",
                                                    "transmission": "manual",
                                                    "city": "Moscow"
                                                    })
    assert response_engine_NaN.status_code == 422