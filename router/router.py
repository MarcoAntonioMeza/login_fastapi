from fastapi import APIRouter, HTTPException, Response 
from fastapi.responses import JSONResponse  
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from schema.user_schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List

from config.db import engine
from model.users import users



user = APIRouter()
base_user_url = '/api/user'

@user.get('/')
def root():
    return {'Message':'I am Antonio'}

@user.get(base_user_url,response_model=List[UserSchema])
def list_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result

@user.get(f'{base_user_url}/{{id_user}}',response_model=UserSchema)
def get_user(id_user:int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == id_user)).first()
        if result:

            return  result
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail='Usuario no encontrado')



@user.post(base_user_url,status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema | None):
    with engine.connect() as conn:
        try:
            user = data_user.dict()
            # Generar hash de la contraseña
            user['user_pass'] = generate_password_hash(data_user.user_pass, 'pbkdf2:sha256:30', 30)
            # Insertar usuario en la base de datos
            result = conn.execute(users.insert().values(user))
            user['id'] =result.inserted_primary_key[0] 
            return JSONResponse(user,status_code=HTTP_201_CREATED)
        except Exception as e:
            # Manejar la excepción y devolver una respuesta adecuada
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")


@user.put(f'{base_user_url}/{{id_user}}', response_model=UserSchema)
def user_update(data_update:UserSchema,id_user:int):
    with engine.connect() as conn:
        user = conn.execute(users.select().where(users.c.id == id_user)).first()
        
        if user is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail='Usuario no encontrado')
        
        data_update = data_update.dict()
        del data_update['id']
        data_update['user_pass'] = generate_password_hash(data_update['user_pass'], 'pbkdf2:sha256:30', 30)
        conn.execute(users.update().values(**data_update).where(
            users.c.id == id_user))
        user = conn.execute(users.select().where(users.c.id == id_user)).first()
        return user
    
@user.delete(f'{base_user_url}/{{id_user}}',status_code=HTTP_204_NO_CONTENT|HTTP_404_NOT_FOUND)
def user_delete(id_user:int):
    with engine.connect() as conn:
        existing_user = conn.execute(users.select().where(users.c.id == id_user)).first()
        
        if existing_user is None:
            #return Response(content='Usuario no encontrado',status_code=HTTP_404_NOT_FOUND)
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail='Usuario no encontrado')
        conn.execute(users.delete().where(users.c.id == id_user))

        return Response(status_code=HTTP_204_NO_CONTENT)