from fastapi import APIRouter
from models.models import posts_table #tabla de los modelos
from schemas.schema_post import Post_Schema #Esquemas
from typing import List
from config.db import cursor 

#Objeto APIRouter:
post = APIRouter()

#Enpoints:
@post.get("/all-posts/", description='Enpoint para el Listado de Todas las PUBLICACIONES/POST de la API', response_model=List[Post_Schema], tags=['Posts'])
def all_posts() -> List:
    """Enpoint para el Listado de Todas las PUBLICACIONES/POST de la API.

    Returns:
        List: Devolverá una lista con un JSON con los datos solicitados.
    """

    return cursor.execute(posts_table.select()).fetchall()