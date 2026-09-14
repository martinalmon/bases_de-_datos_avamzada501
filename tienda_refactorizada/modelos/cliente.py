"""Modelo de cliente."""

from persistent import Persistent


class Cliente(Persistent):
    """Representa a un cliente de la tienda."""

    def __init__(self, id_cliente, nombre, telefono, correo):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    def modificar(self, nombre, telefono, correo):
        """Actualiza los datos del cliente."""
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
