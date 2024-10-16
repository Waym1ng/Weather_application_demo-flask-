import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_weather(client):
    response = client.get('/weather?city=广州')
    assert response.status_code == 200
    data = response.get_json()
    assert 'date' in data[0]
    assert 'weather' in data[0]
    assert 'temp2m' in data[0]
    assert 'wind10m_max' in data[0]

def test_index(client):
    response = client.post('/')
    assert response.status_code == 200
    assert b'Weather Application' in response.data