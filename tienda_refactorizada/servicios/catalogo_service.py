"""Servicios para categorías, clientes y proveedores."""

from modelos.categoria import Categoria
from modelos.cliente import Cliente
from modelos.proveedor import Proveedor


class CatalogoService:
    """Gestiona los catálogos básicos del sistema."""

    def __init__(self, base_datos):
        self.base_datos = base_datos

    def registrar_categoria(self, id_categoria, nombre, descripcion):
        """Registra una categoría nueva."""
        categorias = self.base_datos.root["categorias"]

        if id_categoria in categorias:
            raise ValueError("Ya existe una categoría con ese ID.")

        categoria = Categoria(id_categoria, nombre, descripcion)
        categorias[id_categoria] = categoria
        self.base_datos.confirmar_cambios()
        return categoria

    def registrar_cliente(self, id_cliente, nombre, telefono, correo):
        """Registra un cliente nuevo."""
        clientes = self.base_datos.root["clientes"]

        if id_cliente in clientes:
            raise ValueError("Ya existe un cliente con ese ID.")

        cliente = Cliente(id_cliente, nombre, telefono, correo)
        clientes[id_cliente] = cliente
        self.base_datos.confirmar_cambios()
        return cliente

    def registrar_proveedor(
        self,
        id_proveedor,
        nombre,
        telefono,
        correo,
    ):
        """Registra un proveedor nuevo."""
        proveedores = self.base_datos.root["proveedores"]

        if id_proveedor in proveedores:
            raise ValueError("Ya existe un proveedor con ese ID.")

        proveedor = Proveedor(
            id_proveedor,
            nombre,
            telefono,
            correo,
        )
        proveedores[id_proveedor] = proveedor
        self.base_datos.confirmar_cambios()
        return proveedor

    def buscar_categoria(self, id_categoria):
        """Busca una categoría por ID."""
        return self.base_datos.root["categorias"].get(id_categoria)

    def buscar_cliente(self, id_cliente):
        """Busca un cliente por ID."""
        return self.base_datos.root["clientes"].get(id_cliente)

    def buscar_proveedor(self, id_proveedor):
        """Busca un proveedor por ID."""
        return self.base_datos.root["proveedores"].get(id_proveedor)
