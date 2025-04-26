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


# Tipos de usuario
@app.get("/api/tipousuarios/", response_model=List[TipoUsuarioOut])
def list_tipo_usuarios():
    qs = TipoUsuario.objects.all()
    return [serialize_tipo_usuario(t) for t in qs]


@app.get("/api/tipousuarios/{pk}/", response_model=TipoUsuarioOut)
def get_tipo_usuario(pk: int):
    try:
        t = TipoUsuario.objects.get(pk=pk)
    except TipoUsuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="TipoUsuario no encontrado")
    return serialize_tipo_usuario(t)


# Categorias
@app.get("/api/categorias/", response_model=List[CategoriaOut])
def list_categorias():
    qs = Categoria.objects.all()
    return [serialize_categoria(c) for c in qs]

# Productos

@app.get("/api/productos/", response_model=List[TipoProdOut])
def list_categorias():
    qs = TipoProd.objects.prefetch_related("productos").all()
    return [serialize_tipo_prod(tp) for tp in qs]

@app.get("/api/productos/{pk}/", response_model=TipoProdOut)
def get_tipo_prod(pk: int):
    try:
        tp = TipoProd.objects.prefetch_related("productos").get(pk=pk)
    except TipoProd.DoesNotExist:
        raise HTTPException(status_code=404, detail="TipoProd no encontrado")
    return serialize_tipo_prod(tp)

# Usuarios

@app.get("/api/usuarios/", response_model=List[UsuarioOut])
def list_usuarios():
    qs = Usuario.objects.select_related("tipousuario").all()
    return [serialize_usuario(u) for u in qs]


@app.get("/api/usuarios/{username}/", response_model=UsuarioOut)
def get_usuario(username: str):
    try:
        u = Usuario.objects.select_related("tipousuario").get(username=username)
    except Usuario.DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return serialize_usuario(u)