from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse, Response
from config.db import cursor
from models.models import users_table #tabla de los modelos
from schemas.schema_user import User_Schema #Esquemas
from typing import List
from cryptography.fernet import Fernet

#Objeto APIRouter:
user = APIRouter()

#Endpoints:
#GET:
@user.get("/all-users/", description="Enpoint para el Listado de Todos los USUARIOS/USERS de la API", response_model=List[User_Schema], tags=['Users'])
def all_users() -> List:
    """Enpoint para el Listado de Todos los usuarios de la API

    Returns:
        List: Devolverá una lista con un JSON con los datos solicitados.
    """

    return cursor.execute(users_table.select()).fetchall()

@user.get("/get-user/{user_id}", response_model=List[User_Schema], tags=['Users'])
def get_user(user_id:int = Path(None, description='Ingrese el ID del Usuario (id).', gt=0,le=10)) -> list:
    """Endpoint que listará un usuario en específico mediante la búsqueda de su ID.

    Args:
        user_id (int, optional): ID del usuario a buscar, número entero. Defaults to Path(None, description='Ingrese el ID del Usuario (id).', ge=0, le=10).

    Returns:
        list: Mostrará una lista con el diccionario (JSON) con los datos del usuario.
    """
    
    return cursor.execute(users_table.select().where(users_table.c.id == user_id)).first()

#POST:
#Configuración para la encriptación de la contraseña:
key = Fernet.generate_key()
f_key = Fernet(key)

@user.post("/create-user/", description="Endpoint para la creación de un USUARIO.", response_model=User_Schema, tags=['Users'], status_code=status.HTTP_201_CREATED)
def create_user(schema:User_Schema) -> dict:
    """Endpoint para la creación de un USUARIO.

    Args:
        schema (User_Schema): Esquema para los datos de los usuarios.

    Returns:
        dict: Devolverá un JSON con los datos del objeto creado.
    """

    #Obtengo los datos:
    new_user = {"username":schema.username, "email":schema.email, "is_active":schema.is_active}

    #Encripto la contraseña:
    new_user['password'] = f_key.encrypt(schema.password.encode("utf-8"))

    #Guardo los datos en la bbdd:
    query = cursor.execute(users_table.insert().values(new_user))

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message":"New User Has Been Created.", "User": cursor.execute(users_table.select().where(users_table.c.id == query.lastrowid)).first()})

#PUT:
@user.put("/update-user/{user_id}", status_code=status.HTTP_202_ACCEPTED, tags=['Users'], description='Endpoint para actualizar los datos de un usuario de la API')
def update_user(schema:User_Schema, user_id:int=Path(None, description='Ingrese el ID del Usuario (id).', gt=0,le=10)) -> dict:
    """Endpoint para actualizar los datos de un usuario de la API.

    Args:
        schema (User_Schema): Esquema para los datos del usuario.
        user_id (int, optional): El ID del Usuario que será actualizado, número entero.(id) Defaults to Path(None, description='Ingrese el ID del Usuario (id).', gt=0,le=10).

    Returns:
        dict: Devolvera un JSON con los datos del usuario actualizados y un mensaje feedback.
    """
    
    query = cursor.execute(users_table.update().values(username=schema.username, email=schema.email, password=f_key.encrypt(schema.password.encode("utf-8"))).where(users_table.c.id == user_id))
    return {
        "message":"User Has Been Updated",
        "User":cursor.execute(users_table.select().where(users_table.c.id == user_id)).first()
    }


#DELETE:
@user.delete("/delete-user/{user_id}", description='Endpoint para eliminar un usuario de la API', status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id:int = Path(None, description='Ingrese el ID del Usuario a eliminar. (id)')) -> dict:
    """Endpoint para eliminar un usuario de la API.

    Args:
        user_id (int, optional): El ID del Usuario, número entero. Defaults to Path(None, description='Ingrese el ID del Usuario a eliminar. (id)').

    Returns:
        dict: Devolverá un JSON con un mensaje feedback de la acción realizada.
    """

    cursor.execute(users_table.delete().where(users_table.c.id == user_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)