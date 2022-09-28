from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, String, Integer, DateTime, Boolean #tipos de dats
from config.db import meta, engine

#Defino las Tablas:
users_table = Table(
    "Usuarios", #Nombre de la Tabla
    meta, #metadata
    
    #Columnas de la Tabla:
    Column("id", Integer, primary_key=True),
    Column("username", String(120)),
    Column("email", String(255)),
    Column("password", String(255)),
    Column("is_active", Boolean)
)

posts_table = Table(
    "Publicaciones", #Nombre de la Tabla
    meta, #metadata
    
    #Columnas de la Tabla:
    Column("id", Integer, primary_key=True),
    Column("title", String(80)),
    Column("content", String(255)),
    Column("created_at", DateTime),
)

#Las creo con metadata:
meta.create_all(engine)