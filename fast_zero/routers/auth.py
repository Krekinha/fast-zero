from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# O tipo Annotated nos permite combinar um tipo e os metadados associados a ele
# em uma única definição. Isso nos permite encapsular o tipo da variável e o
# Depends em uma única entidade, facilitando a definição dos endpoints.
# É uma boa prática usar o T_ antes do nome quando definimos um novo tipo
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]


# Esse path é exclusivo para autenticação/login na aplicação. Se os dados
# username e password forem enviados corretamente ele retorna um token
# form_data contém os dados digitados pelo usuário no formulário de login
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: T_OAuth2Form, session: T_Session):
    # busca o usuário que tenha o mesmo email digitado no campo username
    user = session.scalar(select(User).where(User.email == form_data.username))

    # se o usuário não for encontrado retorna um erro
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect email or password",
        )

    # se a senha estiver incorreta retorna um erro
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Incorrect email or password",
        )
    # criar nosso token jwt
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
