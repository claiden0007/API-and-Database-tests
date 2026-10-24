
def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden@example.com",
            "age": 25,
        },
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Claiden"
    assert data["email"] == "claiden@example.com"
    assert data["age"] == 25
    assert "id" in data


def test_get_all_users(client):
    client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden@example.com",
            "age": 25,
        },
    )

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["name"] == "Claiden"


def test_get_specific_user(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden@example.com",
            "age": 25,
        },
    )
    user_id = create_response.get_json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.get_json()["id"] == user_id
    assert response.get_json()["email"] == "claiden@example.com"


def test_update_user(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden@example.com",
            "age": 25,
        },
    )
    user_id = create_response.get_json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Claiden QA",
            "email": "claiden@example.com",
            "age": 26,
        },
    )

    assert response.status_code == 200
    assert response.get_json()["name"] == "Claiden QA"
    assert response.get_json()["age"] == 26


def test_delete_user(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden@example.com",
            "age": 25,
        },
    )
    user_id = create_response.get_json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204

    missing_response = client.get(f"/users/{user_id}")
    assert missing_response.status_code == 404



def test_create_user_without_email(client):
    response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "age": 25
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Email is required"
    }



def test_create_user_without_name(client):
    response = client.post(
        "/users",
        json={
            "email": "claiden@example.com",
            "age": 25
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Name is required"
    }



def test_create_user_without_age(client):
    response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden@example.com"
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }



def test_create_user_underage(client):
    response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_underage@example.com",
            "age": 16
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }



def test_create_user_age_as_string(client):
    response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_string_age@example.com",
            "age": "25"
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }



def test_create_user_without_json_body(client):
    response = client.post("/users")

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "JSON object required"
    }



def test_create_user_duplicate_email(client):
    user_data = {
        "name": "Claiden",
        "email": "duplicate@example.com",
        "age": 25
    }

    first_response = client.post("/users", json=user_data)

    assert first_response.status_code == 201

    second_response = client.post("/users", json=user_data)

    assert second_response.status_code == 409
    assert second_response.get_json() == {
        "error": "Email already exists or data is invalid"
    }



def test_get_nonexistent_user(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "User not found"
    }



def test_create_user_with_json_array(client):
    response = client.post(
        "/users",
        json=["Claiden", "claiden@example.com", 25]
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "JSON object required"
    }



def test_create_user_age_as_boolean(client):
    response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_boolean_age@example.com",
            "age": True
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }



def test_create_user_negative_age(client):
    response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_negative_age@example.com",
            "age": -5
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }



def test_update_nonexistent_user(client):
    response = client.put(
        "/users/999",
        json={
            "name": "Claiden",
            "email": "claiden_updated@example.com",
            "age": 25
        }
    )

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "User not found"
    }



def test_delete_nonexistent_user(client):
    response = client.delete("/users/999")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "User not found"
    }



def test_update_user_with_duplicate_email(client):
    first_user = {
        "name": "Claiden One",
        "email": "claiden_one@example.com",
        "age": 25
    }

    second_user = {
        "name": "Claiden Two",
        "email": "claiden_two@example.com",
        "age": 30
    }

    first_response = client.post("/users", json=first_user)
    second_response = client.post("/users", json=second_user)

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_user_id = first_response.get_json()["id"]
    second_user_id = second_response.get_json()["id"]

    update_response = client.put(
        f"/users/{second_user_id}",
        json={
            "name": "Claiden Two Updated",
            "email": "claiden_one@example.com",
            "age": 30
        }
    )

    assert update_response.status_code == 409
    assert update_response.get_json() == {
        "error": "Email already exists or data is invalid"
    }

    unchanged_user = client.get(f"/users/{second_user_id}")

    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["email"] == "claiden_two@example.com"



def test_update_user_with_invalid_age(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_update_age@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201

    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Claiden",
            "email": "claiden_update_age@example.com",
            "age": 16
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }

    unchanged_user = client.get(f"/users/{user_id}")

    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["age"] == 25



def test_update_user_without_email(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_missing_email@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201

    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Claiden Updated",
            "age": 25
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Email is required"
    }

    unchanged_user = client.get(f"/users/{user_id}")

    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["email"] == (
        "claiden_missing_email@example.com"
    )



def test_update_user_without_name(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_missing_name@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201

    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "email": "claiden_missing_name@example.com",
            "age": 25
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Name is required"
    }

    unchanged_user = client.get(f"/users/{user_id}")

    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["name"] == "Claiden"



def test_update_user_without_age(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_missing_age@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201

    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Claiden Updated",
            "email": "claiden_missing_age@example.com"
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }

    unchanged_user = client.get(f"/users/{user_id}")

    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["age"] == 25



def test_update_user_age_as_string(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_string_update@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Claiden",
            "email": "claiden_string_update@example.com",
            "age": "30"
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }

    unchanged_user = client.get(f"/users/{user_id}")
    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["age"] == 25



def test_update_user_age_as_boolean(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_boolean_update@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Claiden",
            "email": "claiden_boolean_update@example.com",
            "age": True
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }

    unchanged_user = client.get(f"/users/{user_id}")
    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["age"] == 25



def test_update_user_negative_age(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_negative_update@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Claiden",
            "email": "claiden_negative_update@example.com",
            "age": -5
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }

    unchanged_user = client.get(f"/users/{user_id}")
    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["age"] == 25


def test_update_user_with_empty_name(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_empty_name@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "   ",
            "email": "claiden_empty_name@example.com",
            "age": 25
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Name is required"
    }

    unchanged_user = client.get(f"/users/{user_id}")
    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["name"] == "Claiden"



def test_update_user_with_empty_email(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_empty_email@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Claiden",
            "email": "   ",
            "age": 25
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Email is required"
    }

    unchanged_user = client.get(f"/users/{user_id}")
    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["email"] == (
        "claiden_empty_email@example.com"
    )



def test_update_user_without_json_body(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_empty_body@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.get_json()["id"]

    update_response = client.put(f"/users/{user_id}")

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "JSON object required"
    }

    unchanged_user = client.get(f"/users/{user_id}")
    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["name"] == "Claiden"
    assert unchanged_user.get_json()["age"] == 25



def test_update_user_with_json_array(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_array_update@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json=["Claiden Updated", "claiden_array_update@example.com", 30]
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "JSON object required"
    }

    unchanged_user = client.get(f"/users/{user_id}")
    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["name"] == "Claiden"
    assert unchanged_user.get_json()["age"] == 25



def test_update_user_with_empty_name_and_email(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_empty_fields@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "   ",
            "email": "   ",
            "age": 25
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Name is required"
    }

    unchanged_user = client.get(f"/users/{user_id}")
    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["name"] == "Claiden"
    assert unchanged_user.get_json()["email"] == (
        "claiden_empty_fields@example.com"
    )



def test_create_user_age_as_decimal(client):
    response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_decimal_age@example.com",
            "age": 25.5
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }



def test_update_user_age_as_decimal(client):
    create_response = client.post(
        "/users",
        json={
            "name": "Claiden",
            "email": "claiden_decimal_update@example.com",
            "age": 25
        }
    )

    assert create_response.status_code == 201
    user_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/users/{user_id}",
        json={
            "name": "Claiden",
            "email": "claiden_decimal_update@example.com",
            "age": 25.5
        }
    )

    assert update_response.status_code == 400
    assert update_response.get_json() == {
        "error": "Age must be an integer of at least 18"
    }

    unchanged_user = client.get(f"/users/{user_id}")
    assert unchanged_user.status_code == 200
    assert unchanged_user.get_json()["age"] == 25


