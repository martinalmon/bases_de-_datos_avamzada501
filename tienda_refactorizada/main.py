"""Punto de entrada de la Tienda La Económica."""

from consultas.consultas import ConsultasTienda
from interfaz.consola import InterfazConsola
from persistencia.base_datos import BaseDatosZODB
from servicios.catalogo_service import CatalogoService
from servicios.producto_service import ProductoService
from servicios.venta_service import VentaService


def main():
    """Inicializa los componentes y ejecuta la interfaz."""
    base_datos = BaseDatosZODB()

    try:
        base_datos.abrir()

        catalogo_service = CatalogoService(base_datos)
        producto_service = ProductoService(base_datos)
        venta_service = VentaService(
            base_datos,
            producto_service,
        )
        consultas = ConsultasTienda(base_datos)

        interfaz = InterfazConsola(
            base_datos,
            catalogo_service,
            producto_service,
            venta_service,
            consultas,
        )
        interfaz.ejecutar()
    finally:
        base_datos.cerrar()


if __name__ == "__main__":
    main()
