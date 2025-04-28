import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hsc.settings")
django.setup()

from fastapi import FastAPI, HTTPException, status
from typing import List

from Inicio.models import TipoUsuario, Usuario, TipoProd, Categoria
from api.schemas import (
    TipoUsuarioOut,
    UsuarioIn,
    UsuarioOut,
    TipoProdOut,
    CategoriaOut
)
from api.utils import (
    serialize_tipo_usuario,
    serialize_usuario,
    serialize_tipo_prod, serialize_categoria
)

app = FastAPI(title="HCS API")


# Obtenemos la lista de tipos de usuario
@app.get("/api/tipousuarios/", response_model=List[TipoUsuarioOut])
def list_tipo_usuarios():
    qs = TipoUsuario.objects.all()
    return [serialize_tipo_usuario(t) for t in qs]

# Obtenemos un tipo de usuario especifico mediante su ID
@app.get("/api/tipousuarios/{pk}/", response_model=TipoUsuarioOut)
def get_tipo_usuario(pk: int):
    try:
        t = TipoUsuario.objects.get(pk=pk)
    except TipoUsuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="TipoUsuario no encontrado")
    return serialize_tipo_usuario(t)


# Obtenemos la lista de categorias
@app.get("/api/categorias/", response_model=List[CategoriaOut])
def list_categorias():
    qs = Categoria.objects.all()
    return [serialize_categoria(c) for c in qs]

# Obtenemos todos los productos de la pagina
@app.get("/api/productos/", response_model=List[TipoProdOut])
def list_categorias():
    qs = TipoProd.objects.prefetch_related("productos").all()
    return [serialize_tipo_prod(tp) for tp in qs]

# Obtenemos un producto especifico mediante su ID
@app.get("/api/productos/{pk}/", response_model=TipoProdOut)
def get_tipo_prod(pk: int):
    try:
        tp = TipoProd.objects.prefetch_related("productos").get(pk=pk)
    except TipoProd.DoesNotExist:
        raise HTTPException(status_code=404, detail="TipoProd no encontrado")
    return serialize_tipo_prod(tp)

# Obtenemos una lista de usuarios
@app.get("/api/usuarios/", response_model=List[UsuarioOut])
def list_usuarios():
    qs = Usuario.objects.select_related("tipousuario").all()
    return [serialize_usuario(u) for u in qs]

# Obtenemos a un usuario especifico mediante su username
# quizas debamos hacerlo mediante su ID. CRUD DE USUARIOS
@app.get("/api/usuarios/{username}/", response_model=UsuarioOut)
def get_usuario(username: str):
    try:
        u = Usuario.objects.select_related("tipousuario").get(username=username)
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return serialize_usuario(u)

# Creamos a un usuario mediante la API (CRUD)
@app.post("/api/usuarios/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_usuario(payload: UsuarioIn):
    # valida si el username ya existe
    if Usuario.objects.filter(username=payload.username).exists():
        raise HTTPException(status_code=400, detail="Username ya existe")
    # crea el usuario
    u = Usuario.objects.create(
        username=payload.username,
        contrasennia=payload.contrasennia,
        nombre=payload.nombre,
        apellido=payload.apellido,
        email=payload.email,
        tipousuario_id=payload.tipousuario
    )
    return serialize_usuario(u)

# Actualizamos a un usuario mediante su username
@app.put("/api/usuarios/{username}/", response_model=UsuarioOut)
def update_usuario(username: str, payload: UsuarioIn):
    try:
        u = Usuario.objects.get(username=username)
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for field, val in payload.dict().items():
        setattr(u, field, val)
    u.save()
    return serialize_usuario(u)

# Eliminamos a un usuario mediante su username
@app.delete("/api/usuarios/{username}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(username: str):
    deleted, _ = Usuario.objects.filter(username=username).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None