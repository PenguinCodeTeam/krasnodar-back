from fastapi import HTTPException

from tests.unit import app_test


@app_test.get('/')
def success_handler():
    return {'isSuccess': True, 'data': []}


@app_test.get('/not-found')
def http_error_handler():
    raise HTTPException(status_code=404)


@app_test.get('/internal-error')
def internal_error_handler():
    raise ValueError()


def test_error_middleware_without_exception(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'isSuccess': True, 'data': []}


def test_error_middleware_with_http_exception(client):
    response = client.get('/not-found')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_error_middleware_with_unknown_exception(client):
    response = client.get('/internal-error')
    assert response.status_code == 500
    assert response.json()['errors'][0]['code'] == 'APP.APP.00001'
    assert response.json()['errors'][0]['name'] == 'UnknownException'
