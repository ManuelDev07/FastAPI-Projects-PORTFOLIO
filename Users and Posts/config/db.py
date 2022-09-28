from sqlalchemy import create_engine, MetaData

#Conexión a bbdd mediante su URI:
engine = create_engine("postgresql://postgres:28016558@localhost/pruebas_fastapi")
meta = MetaData()

#Cursor:
cursor = engine.connect()