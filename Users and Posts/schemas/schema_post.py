from pydantic import BaseModel
from typing import Optional, List, Union, Text
from datetime import datetime
from schemas.schema_user import User_Schema

#Defino los esquemas de las Publicaciones y Usuarios
class Post_Schema(BaseModel):
    id:Optional[int]
    title:str
    content:Optional[Text]
    created_at: Optional[str] = datetime.utcnow()
    posted_by:Union[User_Schema, List[User_Schema]] = None