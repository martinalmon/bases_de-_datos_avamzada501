"""Consultas del sistema de tienda."""

from datetime import date

from constantes import LIMITE_STOCK


class ConsultasTienda:
    """Agrupa consultas que no modifican información."""

    def __init__(self, base_datos):
        self.base_datos = base_datos

    @property
    def productos(self):
        """Devuelve todos los productos almacenados."""
        return self.base_datos.root["inventario"].productos.values()

    @property
    def ventas(self):
        """Devuelve todas las ventas almacenadas."""
        return self.base_datos.root["ventas"].values()

    def todos_los_productos(self):
        """Devuelve todos los productos registrados."""
        return list(self.productos)

    def productos_precio_superior(self, precio_minimo):
        """Devuelve productos con precio mayor al indicado."""
        return [
            producto
            for producto in self.productos
            if producto.precio > precio_minimo
        ]

    def productos_disponibles(self):
        """Devuelve productos con existencias disponibles."""
        return [
            producto
            for producto in self.productos
            if producto.esta_disponible()
        ]

    def productos_bajo_stock(self, limite=LIMITE_STOCK):
        """Devuelve productos con existencias menores al límite."""
        return [
            producto
            for producto in self.productos
            if producto.existencias < limite
        ]

    def productos_por_proveedor(self, id_proveedor):
        """Devuelve productos asociados a un proveedor."""
        proveedor = self.base_datos.root["proveedores"].get(id_proveedor)

        if proveedor is None:
            raise ValueError("Proveedor no encontrado.")

        return list(proveedor.productos)

    def ventas_cliente(self, id_cliente):
        """Devuelve las ventas realizadas por un cliente."""
        return [
            venta
            for venta in self.ventas
            if venta.cliente.id_cliente == id_cliente
        ]

    def total_ventas(self):
        """Calcula el total acumulado de todas las ventas."""
        return sum(venta.total for venta in self.ventas)

    def venta_total_diaria(self, fecha=None):
        """Calcula el total vendido en una fecha determinada."""
        fecha_consulta = fecha or date.today()

        ventas_dia = [
            venta
            for venta in self.ventas
            if venta.fecha.date() == fecha_consulta
        ]

        total_dia = sum(venta.total for venta in ventas_dia)
        return ventas_dia, total_dia

    def productos_mas_vendidos(self):
        """Devuelve productos ordenados por unidades vendidas."""
        cantidades_vendidas = {}

        for venta in self.ventas:
            for detalle in venta.detalles:
                codigo = detalle.producto.codigo
                nombre = detalle.producto.nombre

                if codigo not in cantidades_vendidas:
                    cantidades_vendidas[codigo] = {
                        "nombre": nombre,
                        "cantidad": 0,
                    }

                cantidades_vendidas[codigo]["cantidad"] += detalle.cantidad

        return sorted(
            cantidades_vendidas.items(),
            key=lambda elemento: elemento[1]["cantidad"],
            reverse=True,
        )
