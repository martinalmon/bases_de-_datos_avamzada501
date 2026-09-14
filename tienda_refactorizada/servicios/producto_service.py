"""Lógica de negocio relacionada con productos e inventario."""

from modelos.producto import Producto


class ProductoService:
    """Administra productos y existencias."""

    def __init__(self, base_datos):
        self.base_datos = base_datos

    @property
    def inventario(self):
        """Devuelve el inventario almacenado en ZODB."""
        return self.base_datos.root["inventario"]

    def registrar_producto(
        self,
        codigo,
        nombre,
        descripcion,
        precio,
        existencias,
        categoria,
    ):
        """Valida, crea y guarda un producto."""
        self._validar_producto(
            codigo,
            nombre,
            precio,
            existencias,
            categoria,
        )

        producto = Producto(
            codigo,
            nombre,
            descripcion,
            precio,
            existencias,
            categoria,
        )

        self.inventario.agregar_producto(producto)
        self.base_datos.confirmar_cambios()
        return producto

    def buscar_producto(self, codigo):
        """Busca un producto por código."""
        return self.inventario.buscar_producto(codigo)

    def modificar_producto(
        self,
        codigo,
        nombre,
        descripcion,
        precio,
        categoria,
    ):
        """Modifica un producto existente."""
        producto = self._obtener_producto_o_error(codigo)

        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        producto.modificar(
            nombre,
            descripcion,
            precio,
            categoria,
        )
        self.base_datos.confirmar_cambios()
        return producto

    def eliminar_producto(self, codigo):
        """Elimina un producto y sus relaciones con proveedores."""
        producto = self._obtener_producto_o_error(codigo)

        for proveedor in list(producto.proveedores):
            proveedor.eliminar_producto(producto)

        producto_eliminado = self.inventario.eliminar_producto(codigo)
        self.base_datos.confirmar_cambios()
        return producto_eliminado

    def asociar_proveedor(self, codigo, proveedor):
        """Asocia un proveedor a un producto."""
        producto = self._obtener_producto_o_error(codigo)
        producto.agregar_proveedor(proveedor)
        self.base_datos.confirmar_cambios()
        return producto

    def incrementar_existencias(self, codigo, cantidad):
        """Incrementa las existencias de un producto."""
        producto = self._obtener_producto_o_error(codigo)
        producto.incrementar_existencias(cantidad)
        self.base_datos.confirmar_cambios()
        return producto

    def disminuir_existencias(self, codigo, cantidad):
        """Disminuye las existencias de un producto."""
        producto = self._obtener_producto_o_error(codigo)
        producto.disminuir_existencias(cantidad)
        self.base_datos.confirmar_cambios()
        return producto

    def _obtener_producto_o_error(self, codigo):
        """Obtiene un producto o genera un error descriptivo."""
        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        return producto

    @staticmethod
    def _validar_producto(
        codigo,
        nombre,
        precio,
        existencias,
        categoria,
    ):
        """Valida los datos necesarios para registrar un producto."""
        if not codigo.strip():
            raise ValueError("El código no puede estar vacío.")

        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        if existencias < 0:
            raise ValueError("Las existencias no pueden ser negativas.")

        if categoria is None:
            raise ValueError("La categoría no existe.")
