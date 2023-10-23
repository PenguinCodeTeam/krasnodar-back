from urllib.parse import urljoin

import config


def test_status_endpoint(client):
    response = client.get(urljoin(config.APP_URL_PREFIX, 'api/status'))
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_ping_endpoint(client):
    response = client.get(urljoin(config.APP_URL_PREFIX, 'api/ping'))
    assert response.status_code == 200
    assert response.text == 'PONG'


def test_add_no_cache_header(client):
    response = client.get(urljoin(config.APP_URL_PREFIX, 'api/status'))
    assert response.status_code == 200
    assert response.headers['Cache-Control'] == 'No-Cache'
    assert response.json() == {'status': 'ok'}
