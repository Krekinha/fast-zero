from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import TokenData
from fast_zero.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()

# esse scheme força o usuário logar para poder usar a rota pretendida
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# Gera um hash da senha do usuário que será armazenada no banco de dados
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Verifica se a sebha informada está correta comparando a hash da senha
# digitada com o hash armazenado no banco de dados
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Gera um jwt que será a assinatura que o servidor fornece ao usuário para
# dizer que ele está autorizado a usar a aplicação
def create_access_token(data: dict):
    to_encode = data.copy()
    # Gera a data de expiração do token que será a data/hora atual + o tempo de
    # expiração em minutos que setamos anteriormente
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # Atualiza o campo "exp" do cionário com a data gerada anteriormente
    to_encode.update({"exp": expire})
    # Encoda a informações do nosso dicionário usando a senha que definimos
    # na variável de ambiente e o algoritimo definido anteriormente
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if user is None:
        raise credentials_exception

    return user
