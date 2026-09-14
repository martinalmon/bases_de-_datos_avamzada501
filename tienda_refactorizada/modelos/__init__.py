"""Modelos de la Tienda La Económica."""

from modelos.categoria import Categoria
from modelos.cliente import Cliente
from modelos.inventario import Inventario
from modelos.producto import Producto
from modelos.proveedor import Proveedor
from modelos.venta import DetalleVenta, Venta

__all__ = [
    "Categoria",
    "Cliente",
    "Inventario",
    "Producto",
    "Proveedor",
    "DetalleVenta",
    "Venta",
]
