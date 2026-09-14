"""Lógica de negocio de ventas."""

from modelos.venta import DetalleVenta, Venta


class VentaService:
    """Gestiona la creación y registro de ventas."""

    def __init__(self, base_datos, producto_service):
        self.base_datos = base_datos
        self.producto_service = producto_service

    def iniciar_venta(self, cliente):
        """Crea una venta nueva todavía no guardada."""
        if cliente is None:
            raise ValueError("El cliente no existe.")

        id_venta = self._generar_id_venta()
        return Venta(id_venta, cliente)

    def agregar_producto_venta(self, venta, codigo_producto, cantidad):
        """Agrega un producto y actualiza el inventario."""
        producto = self.producto_service.buscar_producto(codigo_producto)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        producto.disminuir_existencias(cantidad)
        detalle = DetalleVenta(producto, cantidad)
        venta.agregar_detalle(detalle)
        return detalle

    def registrar_venta(self, venta):
        """Guarda una venta terminada en ZODB."""
        if not venta.detalles:
            raise ValueError("La venta debe contener al menos un producto.")

        venta.calcular_total()
        self.base_datos.root["ventas"][venta.id_venta] = venta
        self.base_datos.confirmar_cambios()
        return venta

    def cancelar_venta(self):
        """Revierte los cambios no confirmados de una venta."""
        self.base_datos.cancelar_cambios()

    def _generar_id_venta(self):
        """Genera un identificador secuencial para la siguiente venta."""
        cantidad_ventas = len(self.base_datos.root["ventas"])
        return f"V{cantidad_ventas + 1:03d}"
