import re
from random import randint, choice

import pytest


def generate_random_big_body(elements: int = 10000, minimal_value: int = 0, maximal_value: int = 1000,
                             types: tuple = ('value1', 'value2', 'value3')):
    body = {'status': 'status', 'data': []}

    for i in range(elements):
        body['data'].append(
            {
                'value': randint(minimal_value, maximal_value),
                'type': choice(types),
            })
    return body


@pytest.mark.asyncio
async def test_big_request(client, mocker):
    mocker.patch('config.LOG_PROPAGATE', False)
    body = generate_random_big_body(10000)
    res = client.post('/pointless/endpoint', json=body)
    assert res
    assert res.status_code == 404
