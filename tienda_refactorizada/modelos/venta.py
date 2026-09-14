"""Modelos relacionados con una venta."""

from datetime import datetime

from persistent import Persistent
from persistent.list import PersistentList


class DetalleVenta(Persistent):
    """Representa un producto y su cantidad dentro de una venta."""

    def __init__(self, producto, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = producto.precio
        self.subtotal = self.calcular_subtotal()

    def calcular_subtotal(self):
        """Calcula el importe del detalle."""
        return self.precio_unitario * self.cantidad


class Venta(Persistent):
    """Representa una venta realizada a un cliente."""

    def __init__(self, id_venta, cliente):
        self.id_venta = id_venta
        self.fecha = datetime.now()
        self.cliente = cliente
        self.detalles = PersistentList()
        self.total = 0.0

    def agregar_detalle(self, detalle):
        """Agrega un detalle y actualiza el total."""
        self.detalles.append(detalle)
        self.calcular_total()

    def calcular_total(self):
        """Calcula el total de la venta."""
        self.total = sum(detalle.subtotal for detalle in self.detalles)
        return self.total
