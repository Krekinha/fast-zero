from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get("/")
def read_root():
    return {"message": "tamos junto"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.get("/users/", response_model=UserList)
def read_users():
    return {"users": database}


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="ID NÃO EXISTE"
        )

    user_with_id = UserDB(id=user_id, **user.model_dump())

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete("/users/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.OK, detail="ID NÃO EXISTE")

    del database[user_id - 1]

    return {"message": "usuário excluído"}
