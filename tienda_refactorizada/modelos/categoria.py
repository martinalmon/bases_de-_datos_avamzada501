"""Modelo de categoría."""

from persistent import Persistent


class Categoria(Persistent):
    """Representa una categoría de productos."""

    def __init__(self, id_categoria, nombre, descripcion):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion

    def modificar(self, nombre, descripcion):
        """Actualiza los datos de la categoría."""
        self.nombre = nombre
        self.descripcion = descripcion
