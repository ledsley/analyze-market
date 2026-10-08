from fastapi.testclient import TestClient
from api import app
from datetime import date

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