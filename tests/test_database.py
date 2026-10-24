
import pytest

from app.database import (
    create_users_table,
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user,
)


@pytest.fixture
def database_path(tmp_path):
    db_path = str(tmp_path / "test_users.db")
    create_users_table(db_path)
    return db_path


def test_create_and_get_user(database_path):
    user_id = create_user(
        database_path, "Claiden", "claiden@example.com", 25
    )

    user = get_user(database_path, user_id)

    assert user is not None
    assert user["name"] == "Claiden"
    assert user["email"] == "claiden@example.com"
    assert user["age"] == 25


def test_get_all_users(database_path):
    create_user(database_path, "Claiden", "claiden@example.com", 25)
    create_user(database_path, "Alex", "alex@example.com", 30)

    users = get_all_users(database_path)

    assert len(users) == 2


def test_update_user(database_path):
    user_id = create_user(
        database_path, "Claiden", "claiden@example.com", 25
    )

    updated = update_user(
        database_path, user_id, "Claiden QA", "claiden@example.com", 26
    )

    assert updated is True
    assert get_user(database_path, user_id)["age"] == 26


def test_delete_user(database_path):
    user_id = create_user(
        database_path, "Claiden", "claiden@example.com", 25
    )

    deleted = delete_user(database_path, user_id)

    assert deleted is True
    assert get_user(database_path, user_id) is None


def test_get_missing_user(database_path):
    assert get_user(database_path, 999) is None


def test_duplicate_email_is_rejected(database_path):
    create_user(database_path, "Claiden", "claiden@example.com", 25)

    with pytest.raises(Exception):
        create_user(database_path, "Alex", "claiden@example.com", 30)
