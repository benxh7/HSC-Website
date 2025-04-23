from Inicio.models import TipoUsuario, Usuario, Producto, TipoProd
from api.schemas import TipoUsuarioOut, UsuarioOut, ProductoOut, TipoProdOut


def serialize_tipo_usuario(t: TipoUsuario) -> TipoUsuarioOut:
    return TipoUsuarioOut(
        idTipoUsuario=t.idTipoUsuario,
        nombreTipo=t.nombreTipo
    )

def serialize_producto(p: Producto) -> ProductoOut:
    return ProductoOut(
        idProducto=p.idProducto,
        nombreProducto=p.nombreProducto,
        precioProducto=p.precioProducto,
        especificacionProd=p.especificacionProd,
        stockProd=p.stockProd,
        imagenProd=p.imagenProd.url if p.imagenProd else None,
    )


def serialize_tipo_prod(tp: TipoProd) -> TipoProdOut:
    return TipoProdOut(
        idTiporod=tp.idTiporod,
        nombreTipoProd=tp.nombreTipoProd,
        productos=[serialize_producto(p) for p in tp.productos.all()]
    )


def serialize_usuario(u: Usuario) -> UsuarioOut:
    tipo = serialize_tipo_usuario(u.tipousuario)
    return UsuarioOut(
        username=u.username,
        nombre=u.nombre,
        apellido=u.apellido,
        email=u.email,
        tipousuario=tipo
    )
