from pydantic import BaseModel
from typing import Optional

#Defino los esquemas de las Publicaciones y Usuarios
class User_Schema(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_active:bool = True