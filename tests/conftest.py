import pytest
from project import create_app


@pytest.fixture
def app():
    app = create_app()
    return app
