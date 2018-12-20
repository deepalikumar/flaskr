import pytest

def test_index(client, auth):
    response = client.get('/')
    assert b"Login" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Logout' in response.data
    assert b'test title' in response.data
    assert b'by test on' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data