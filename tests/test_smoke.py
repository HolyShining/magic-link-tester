from flask import url_for


def test_index_is_available(client):
    assert client.get(url_for('main.index')).status_code == 200


def test_secret_is_available(client):
    assert client.get(url_for('main.secret')).status_code == 302


def test_generate_is_available(client):
    assert client.get(url_for('auth.generate_get')).status_code == 200


def test_logout_is_available(client):
    assert client.get(url_for('auth.logout')).status_code == 302