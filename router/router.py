from fastapi import APIRouter, HTTPException
from schema.user_schema import UserSchema

from config.db import conn
from model.users import users

from werkzeug.security import generate_password_hash, check_password_hash

user = APIRouter()
base_user_url = '/api/user/'

@user.get('/')
def root():
    return {'Message':'I am Antonio'}

@user.post(base_user_url)
def create_user(data_user: UserSchema | None):
    try:
        user = data_user.dict()
        # Generar hash de la contraseña
        user['user_pass'] = generate_password_hash(data_user.user_pass, 'pbkdf2:sha256:30', 30)
        # Insertar usuario en la base de datos
        conn.execute(users.insert().values(user))
        return user
    except Exception as e:
        # Manejar la excepción y devolver una respuesta adecuada
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")