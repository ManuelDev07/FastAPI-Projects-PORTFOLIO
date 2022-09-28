from fastapi import FastAPI
from routers import posts, users

tags_metadata = [
    {
        "name":"Posts",
        "description":"C.R.U.D para los Endpoints de Publicaciones"
    },
    {
        "name":"Users",
        "description":"C.R.U.D para los Endpoints de los Usuarios"
    }
]

#Objeto FastAPI:
app = FastAPI(
    title="Products API",
    description='Simple API + SQL Connections',
    version='0.0.1',
    openapi_tags=tags_metadata
)

#Router:
app.include_router(posts.post)
app.include_router(users.user)
