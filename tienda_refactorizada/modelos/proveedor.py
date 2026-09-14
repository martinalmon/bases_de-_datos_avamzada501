"""Modelo de proveedor."""

from persistent import Persistent
from persistent.list import PersistentList


class Proveedor(Persistent):
    """Representa a un proveedor de productos."""

    def __init__(self, id_proveedor, nombre, telefono, correo):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.productos = PersistentList()

    def agregar_producto(self, producto):
        """Asocia un producto al proveedor sin duplicarlo."""
        if producto not in self.productos:
            self.productos.append(producto)

    def eliminar_producto(self, producto):
        """Elimina la relación con un producto."""
        if producto in self.productos:
            self.productos.remove(producto)

    def modificar(self, nombre, telefono, correo):
        """Actualiza los datos del proveedor."""
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
