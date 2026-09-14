"""Modelo de producto."""

from persistent import Persistent
from persistent.list import PersistentList


class Producto(Persistent):
    """Representa un producto disponible en la tienda."""

    def __init__(
        self,
        codigo,
        nombre,
        descripcion,
        precio,
        existencias,
        categoria,
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.existencias = existencias
        self.categoria = categoria
        self.proveedores = PersistentList()

    def agregar_proveedor(self, proveedor):
        """Asocia un proveedor con el producto."""
        if proveedor not in self.proveedores:
            self.proveedores.append(proveedor)

        proveedor.agregar_producto(self)

    def incrementar_existencias(self, cantidad):
        """Aumenta las existencias del producto."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self.existencias += cantidad

    def disminuir_existencias(self, cantidad):
        """Disminuye existencias si hay unidades suficientes."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if cantidad > self.existencias:
            raise ValueError("No hay existencias suficientes.")

        self.existencias -= cantidad

    def modificar(self, nombre, descripcion, precio, categoria):
        """Actualiza los datos principales del producto."""
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria

    def esta_disponible(self):
        """Indica si el producto tiene existencias."""
        return self.existencias > 0
