from pydantic import BaseModel
from typing import Optional, List

class TipoUsuarioOut(BaseModel):
    idTipoUsuario: int
    nombreTipo: str

    class Config:
        orm_mode = True

class CategoriaOut(BaseModel):
    idCategoria: int
    nombreCategoria: str

    class Config:
        orm_mode = True

class ProductoOut(BaseModel):
    idProducto: int
    nombreProducto: str
    precioProducto: int
    especificacionProd: str
    stockProd: int
    imagenProd: Optional[str]

    class Config:
        orm_mode = True

class TipoProdOut(BaseModel):
    idTiporod: int
    nombreTipoProd: str
    productos: List[ProductoOut]

    class Config:
        orm_mode = True

class UsuarioIn(BaseModel):
    username: str
    contrasennia: str
    nombre: str
    apellido: str
    email: str
    tipousuario: int


class UsuarioOut(BaseModel):
    username: str
    nombre: str
    apellido: str
    email: str
    tipousuario: TipoUsuarioOut

    class Config:
        orm_mode = True