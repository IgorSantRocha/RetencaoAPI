from fastapi import HTTPException, status
import re
import random


def valida_pwd(self, pwd):
    # Verifica o comprimento da senha
    if len(pwd) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter pelo menos 6 caracteres!"
        )

    # Verifica se contém pelo menos uma letra maiúscula
    if not re.search(r'[A-Z]', pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter pelo menos uma letra maiúscula!"
        )

    # Verifica se contém pelo menos uma letra minúscula
    if not re.search(r'[a-z]', pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter pelo menos uma letra minúscula!"
        )

    # Verifica se contém pelo menos um número
    if not re.search(r'[0-9]', pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter pelo menos um número!"
        )

    # Verifica se contém pelo menos um caractere especial
    if not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:\'",<>\./?]', pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve conter pelo menos um caractere especial!"
        )

    return True


def valida_username(self, username: str):
    # Verifica o comprimento do nome de usuário
    if len(username) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O nome de usuário deve conter pelo menos 6 caracteres!"
        )

    # Verifica se contém apenas letras, números e underscore
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O nome de usuário deve conter apenas letras, números e underline! (Não use espaços)"
        )


def generate_token():
    return random.randint(100000, 999999)
