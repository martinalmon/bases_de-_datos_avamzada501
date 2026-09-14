"""Modelo del inventario."""

from persistent import Persistent
from persistent.mapping import PersistentMapping


class Inventario(Persistent):
    """Mantiene los productos registrados por código."""

    def __init__(self):
        self.productos = PersistentMapping()

    def agregar_producto(self, producto):
        """Agrega un producto si su código no está registrado."""
        if producto.codigo in self.productos:
            raise ValueError("Ya existe un producto con ese código.")

        self.productos[producto.codigo] = producto

    def buscar_producto(self, codigo):
        """Busca un producto por su código."""
        return self.productos.get(codigo)

    def eliminar_producto(self, codigo):
        """Elimina un producto del inventario."""
        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        del self.productos[codigo]
        return producto
