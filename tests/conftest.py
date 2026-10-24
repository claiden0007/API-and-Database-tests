
import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / "test_users.db"
    return create_app(str(database_path))


@pytest.fixture
def client(app):
    return app.test_client()
