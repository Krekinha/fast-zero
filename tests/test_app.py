import email
import ftplib
from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")  # Act (ação)
    dir = "lef"

    assert response.status_code == HTTPStatus.OK  # Assert (afirmação)
    assert response.json() == {"message": "tamos junto"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testname",
            "email": "test@mail.com",
            "password": "testpwd",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        "id": 1,
        "username": "testname",
        "email": "test@mail.com",
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "username": "testname",
                "email": "test@mail.com",
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "id": 1,
            "username": "testname2",
            "email": "test@mail.com",
            "password": "testpwd",
        },
    )

    # Validar UserPublic
    assert response.json() == {
        "id": 1,
        "username": "testname2",
        "email": "test@mail.com",
    }


def test_delete_user(client):
    response = client.delete("/users/1")

    # Validar UserPublic
    assert response.json() == {"message": "usuário excluído"}
