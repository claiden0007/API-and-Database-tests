
import sqlite3


def get_connection(database_path):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def create_users_table(database_path):
    with get_connection(database_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL CHECK (age >= 18)
            )
        """)


def create_user(database_path, name, email, age):
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (name, email, age)
            VALUES (?, ?, ?)
            """,
            (name, email, age),
        )
        user_id = cursor.lastrowid

    return user_id


def get_user(database_path, user_id):
    with get_connection(database_path) as connection:
        user = connection.execute(
            "SELECT id, name, email, age FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

    return dict(user) if user else None


def get_all_users(database_path):
    with get_connection(database_path) as connection:
        users = connection.execute(
            "SELECT id, name, email, age FROM users ORDER BY id"
        ).fetchall()

    return [dict(user) for user in users]


def update_user(database_path, user_id, name, email, age):
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            UPDATE users
            SET name = ?, email = ?, age = ?
            WHERE id = ?
            """,
            (name, email, age, user_id),
        )

    return cursor.rowcount > 0


def delete_user(database_path, user_id):
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,),
        )

    return cursor.rowcount > 0
