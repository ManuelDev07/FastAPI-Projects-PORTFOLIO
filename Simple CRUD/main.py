from itertools import product
from math import prod
from fastapi import FastAPI, Path, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Text
from uuid import uuid4

app = FastAPI() #instancio el object FastAPI

products =[]

#Esquema del Producto:
class Product_Model(BaseModel):
    id:Optional[int]
    name:str
    description:Optional[Text]
    price:float
    stock:int
    available:bool=True #valor por defecto

#GET:
@app.get("/all-products/")
def all_products() -> dict:
    """Endpoint que mostrará todos los objetos de la API.

    Returns:
        dict: Devolverá un JSON con todos los datos de la API.
    """
    
    return products

@app.get("/get-product-by-name/{product_name}")
def get_product_by_name(product_name:str = Path(None, description="Insert the Name of the Product (name)")) -> dict:
    """Endpoint que mostrará los datos de un producto en específico mediante la búsqueda de su nombre (campo name).

    Args:
        product_name (str, optional): El nombre del Producto en string. Defaults to Path(None, description="Insert the Name of the Product (name)").

    Raises:
        HTTPException: Mostrará un código de error 404 por si no se ha encontrado/no existe.

    Returns:
        dict: Devolverá un doc JSON con los datos del producto buscado y encontrado.
    """
    
    #Itero en la lista de productos si alguno de ellos tiene el mismo "name" que se ha pasado a través de la función.
    for product in products:
        if product['name'] == product_name:
            return product
    
    raise HTTPException(status_code=404, detail="Product Name not Found.") #en caso de no encontrarlo devuelvo un error 404

@app.get("/get-product-by-id/{product_id}")
def get_product_by_id(product_id:str = Path(None, description="Insert the ID of the Product (id)")) -> dict:
    """Endpoint que mostrará los datos de un producto en específico mediante la búsqueda de su ID (campo id).

    Args:
        product_id (str, optional): El ID del Producto en string. Defaults to Path(None, description="Insert the ID of the Product (id)").

    Raises:
        HTTPException: Mostrará un código de error 404 por si no se ha encontrado/no existe.

    Returns:
        dict: Devolverá un doc JSON con los datos del producto buscado y encontrado.
    """    

    #Itero en la lista de productos si alguno de ellos tiene el mismo id que se ha pasado a través de la función.
    for product in products:
        if product['id'] == product_id:
            return product
    
    raise HTTPException(status_code=404, detail="Product ID not Found.") #en caso de no encontrarlo devuelvo un error 404

#POST:
@app.post("/create-product/", status_code=status.HTTP_201_CREATED, description="Create a New Product!.")
def create_product(new_product:Product_Model) -> dict:
    """Endpoint que se encargará de crear nuevos objetos (productos) a la API.

    Args:
        new_product (Product_Model): Esquema en el que está basado el producto.

    Returns:
        dict: Devolverá un JSON con un mensaje feedback que mostrará que se ha podido crear correctamente y los datos registrados.
    """
    
    new_product.id = str(uuid4()) #manipulo el id del nuevo producto para que sea un objeto UUID4 en forma de cadena
    products.append(new_product.dict()) #lo agrego a la lista

    return {"message":"Product Created Succesfully!", "New Product":products[-1]}

#PUT:
@app.put("/update-product/{product_id}", status_code=status.HTTP_201_CREATED, description="Update An Existing Product.")
def update_product(new_data_product:Product_Model, product_id:str=Path(None, description="Insert the ID of the Product."), ) -> dict:
    """Enpoint que actualizará los datos de un Producto en específico mediante la búsqueda de su ID.

    Args:
        new_data_product (Product_Model): Esquema del Producto.
        product_id (str, optional): ID del producto que se actualizará (id). Defaults to Path(None, description="Insert the ID of the Product.").

    Raises:
        HTTPException: mostrará un error 404 en caso de no ser encontrado o de no existir en la API.

    Returns:
        dict: Devolverá un JSON con un mensaje feedback informando de que los datos han sido actualizados correctamente.
    """

    #Itero en la lista si existe el producto qeu quiero actualizar
    for index, product in enumerate(products):
        if product['id'] == product_id:
            #asigno los nuevos valores con el esquema:
            product[index]['name'] = new_data_product.name
            product[index]['description'] = new_data_product.description
            product[index]['price'] = new_data_product.price
            product[index]['stock'] = new_data_product.stock
            product[index]['available'] = new_data_product.available

            return {"message":"Product Has Been Updated Successfully!"}

    raise HTTPException(status_code=404, detail="Product ID not Found.") #en caso de no encontrarlo devuelvo un error 404

@app.delete("/delete-product/{product_id}", description="Delete An Existing Product.")
def delete_product(product_id:str=Path(None, description="Insert the ID of the Product to Remove.")) -> dict:
    
    #Realizo una búsqueda:
    for index, product in enumerate(products):
        if product['id'] == product_id:
            #elimino el producto utilizando su indice:
            products.pop(index)

            return {"message":"Product Has Been Eliminated Succesfully!"}

    raise HTTPException(status_code=404, detail="Product ID Not Found.")