"""Interfaz de línea de comandos del sistema."""

from datetime import datetime


class InterfazConsola:
    """Coordina la entrada y salida de datos por consola."""

    def __init__(
        self,
        base_datos,
        catalogo_service,
        producto_service,
        venta_service,
        consultas,
    ):
        self.base_datos = base_datos
        self.catalogo_service = catalogo_service
        self.producto_service = producto_service
        self.venta_service = venta_service
        self.consultas = consultas

    def ejecutar(self):
        """Muestra el menú principal hasta que el usuario decida salir."""
        while True:
            self._mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()

            try:
                if opcion == "1":
                    self._registrar_categoria()
                elif opcion == "2":
                    self._registrar_proveedor()
                elif opcion == "3":
                    self._registrar_cliente()
                elif opcion == "4":
                    self._registrar_producto()
                elif opcion == "5":
                    self._asociar_proveedor()
                elif opcion == "6":
                    self._consultar_producto()
                elif opcion == "7":
                    self._modificar_producto()
                elif opcion == "8":
                    self._eliminar_producto()
                elif opcion == "9":
                    self._incrementar_existencias()
                elif opcion == "10":
                    self._disminuir_existencias()
                elif opcion == "11":
                    self._registrar_venta()
                elif opcion == "12":
                    self._mostrar_todos_productos()
                elif opcion == "13":
                    self._productos_precio_superior()
                elif opcion == "14":
                    self._productos_disponibles()
                elif opcion == "15":
                    self._productos_bajo_stock()
                elif opcion == "16":
                    self._productos_por_proveedor()
                elif opcion == "17":
                    self._mostrar_total_ventas()
                elif opcion == "18":
                    self._reporte_venta_diaria()
                elif opcion == "19":
                    self._ventas_por_cliente()
                elif opcion == "20":
                    self._productos_mas_vendidos()
                elif opcion == "0":
                    print("Sistema cerrado correctamente.")
                    break
                else:
                    print("Opción no válida.")
            except ValueError as error:
                print(f"Error: {error}")

    @staticmethod
    def _mostrar_menu():
        print("\nTIENDA LA ECONÓMICA")
        print("1. Registrar categoría")
        print("2. Registrar proveedor")
        print("3. Registrar cliente")
        print("4. Registrar producto")
        print("5. Asociar proveedor a producto")
        print("6. Consultar producto")
        print("7. Modificar producto")
        print("8. Eliminar producto")
        print("9. Incrementar existencias")
        print("10. Disminuir existencias")
        print("11. Registrar venta")
        print("12. Mostrar todos los productos")
        print("13. Productos con precio superior")
        print("14. Productos disponibles")
        print("15. Productos con bajo stock")
        print("16. Productos por proveedor")
        print("17. Total de ventas")
        print("18. Reporte de venta total diaria")
        print("19. Ventas por cliente")
        print("20. Productos más vendidos")
        print("0. Salir")

    def _registrar_categoria(self):
        id_categoria = input("ID de categoría: ").strip()
        nombre = input("Nombre: ").strip()
        descripcion = input("Descripción: ").strip()

        self.catalogo_service.registrar_categoria(
            id_categoria,
            nombre,
            descripcion,
        )
        print("Categoría registrada.")

    def _registrar_proveedor(self):
        id_proveedor = input("ID de proveedor: ").strip()
        nombre = input("Nombre: ").strip()
        telefono = input("Teléfono: ").strip()
        correo = input("Correo: ").strip()

        self.catalogo_service.registrar_proveedor(
            id_proveedor,
            nombre,
            telefono,
            correo,
        )
        print("Proveedor registrado.")

    def _registrar_cliente(self):
        id_cliente = input("ID de cliente: ").strip()
        nombre = input("Nombre: ").strip()
        telefono = input("Teléfono: ").strip()
        correo = input("Correo: ").strip()

        self.catalogo_service.registrar_cliente(
            id_cliente,
            nombre,
            telefono,
            correo,
        )
        print("Cliente registrado.")

    def _registrar_producto(self):
        codigo = input("Código: ").strip()
        nombre = input("Nombre: ").strip()
        descripcion = input("Descripción: ").strip()
        precio = self._leer_float("Precio: ")
        existencias = self._leer_entero("Existencias: ")
        id_categoria = input("ID de categoría: ").strip()

        categoria = self.catalogo_service.buscar_categoria(id_categoria)

        self.producto_service.registrar_producto(
            codigo,
            nombre,
            descripcion,
            precio,
            existencias,
            categoria,
        )
        print("Producto registrado.")

    def _asociar_proveedor(self):
        codigo = input("Código del producto: ").strip()
        id_proveedor = input("ID del proveedor: ").strip()
        proveedor = self.catalogo_service.buscar_proveedor(id_proveedor)

        if proveedor is None:
            raise ValueError("Proveedor no encontrado.")

        self.producto_service.asociar_proveedor(codigo, proveedor)
        print("Proveedor asociado.")

    def _consultar_producto(self):
        codigo = input("Código del producto: ").strip()
        producto = self.producto_service.buscar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        self._mostrar_producto(producto)

    def _modificar_producto(self):
        codigo = input("Código del producto: ").strip()
        producto = self.producto_service.buscar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        nombre = input(f"Nombre [{producto.nombre}]: ").strip()
        descripcion = input(
            f"Descripción [{producto.descripcion}]: "
        ).strip()
        precio_texto = input(f"Precio [{producto.precio}]: ").strip()
        categoria_texto = input(
            f"ID categoría [{producto.categoria.id_categoria}]: "
        ).strip()

        nombre = nombre or producto.nombre
        descripcion = descripcion or producto.descripcion
        precio = (
            producto.precio
            if not precio_texto
            else float(precio_texto)
        )

        if categoria_texto:
            categoria = self.catalogo_service.buscar_categoria(
                categoria_texto
            )
            if categoria is None:
                raise ValueError("Categoría no encontrada.")
        else:
            categoria = producto.categoria

        self.producto_service.modificar_producto(
            codigo,
            nombre,
            descripcion,
            precio,
            categoria,
        )
        print("Producto modificado.")

    def _eliminar_producto(self):
        codigo = input("Código del producto: ").strip()
        self.producto_service.eliminar_producto(codigo)
        print("Producto eliminado.")

    def _incrementar_existencias(self):
        codigo = input("Código del producto: ").strip()
        cantidad = self._leer_entero("Cantidad a agregar: ")
        producto = self.producto_service.incrementar_existencias(
            codigo,
            cantidad,
        )
        print(f"Existencias actuales: {producto.existencias}")

    def _disminuir_existencias(self):
        codigo = input("Código del producto: ").strip()
        cantidad = self._leer_entero("Cantidad a disminuir: ")
        producto = self.producto_service.disminuir_existencias(
            codigo,
            cantidad,
        )
        print(f"Existencias actuales: {producto.existencias}")

    def _registrar_venta(self):
        id_cliente = input("ID del cliente: ").strip()
        cliente = self.catalogo_service.buscar_cliente(id_cliente)
        venta = self.venta_service.iniciar_venta(cliente)

        print("Escribe FIN para terminar de agregar productos.")

        try:
            while True:
                codigo = input("Código del producto: ").strip()

                if codigo.upper() == "FIN":
                    break

                cantidad = self._leer_entero("Cantidad: ")
                self.venta_service.agregar_producto_venta(
                    venta,
                    codigo,
                    cantidad,
                )
                print("Producto agregado a la venta.")

            venta = self.venta_service.registrar_venta(venta)
            print(
                f"Venta {venta.id_venta} registrada. "
                f"Total: ${venta.total:.2f}"
            )
        except ValueError:
            self.venta_service.cancelar_venta()
            raise

    def _mostrar_todos_productos(self):
        productos = self.consultas.todos_los_productos()
        self._mostrar_lista_productos(productos)

    def _productos_precio_superior(self):
        precio = self._leer_float("Precio mínimo: ")
        productos = self.consultas.productos_precio_superior(precio)
        self._mostrar_lista_productos(productos)

    def _productos_disponibles(self):
        productos = self.consultas.productos_disponibles()
        self._mostrar_lista_productos(productos)

    def _productos_bajo_stock(self):
        limite_texto = input(
            "Límite de stock (Enter para usar el predeterminado): "
        ).strip()

        if limite_texto:
            productos = self.consultas.productos_bajo_stock(
                int(limite_texto)
            )
        else:
            productos = self.consultas.productos_bajo_stock()

        self._mostrar_lista_productos(productos)

    def _productos_por_proveedor(self):
        id_proveedor = input("ID del proveedor: ").strip()
        productos = self.consultas.productos_por_proveedor(
            id_proveedor
        )
        self._mostrar_lista_productos(productos)

    def _mostrar_total_ventas(self):
        total = self.consultas.total_ventas()
        print(f"Total acumulado de ventas: ${total:.2f}")

    def _reporte_venta_diaria(self):
        fecha_texto = input(
            "Fecha AAAA-MM-DD (Enter para hoy): "
        ).strip()

        fecha = None
        if fecha_texto:
            fecha = datetime.strptime(
                fecha_texto,
                "%Y-%m-%d",
            ).date()

        ventas, total = self.consultas.venta_total_diaria(fecha)

        print(f"Ventas encontradas: {len(ventas)}")
        for venta in ventas:
            print(
                f"{venta.id_venta} | "
                f"{venta.cliente.nombre} | "
                f"${venta.total:.2f}"
            )

        print(f"Venta total del día: ${total:.2f}")

    def _ventas_por_cliente(self):
        id_cliente = input("ID del cliente: ").strip()
        ventas = self.consultas.ventas_cliente(id_cliente)

        if not ventas:
            print("No se encontraron ventas para ese cliente.")
            return

        for venta in ventas:
            print(
                f"{venta.id_venta} | "
                f"{venta.fecha:%Y-%m-%d %H:%M} | "
                f"${venta.total:.2f}"
            )

    def _productos_mas_vendidos(self):
        productos = self.consultas.productos_mas_vendidos()

        if not productos:
            print("No hay ventas registradas.")
            return

        for codigo, informacion in productos:
            print(
                f"{codigo} | "
                f"{informacion['nombre']} | "
                f"Unidades: {informacion['cantidad']}"
            )

    @staticmethod
    def _mostrar_lista_productos(productos):
        if not productos:
            print("No se encontraron productos.")
            return

        for producto in productos:
            InterfazConsola._mostrar_producto(producto)

    @staticmethod
    def _mostrar_producto(producto):
        proveedores = ", ".join(
            proveedor.nombre
            for proveedor in producto.proveedores
        )
        proveedores = proveedores or "Sin proveedor"

        print(
            f"{producto.codigo} | "
            f"{producto.nombre} | "
            f"${producto.precio:.2f} | "
            f"Existencias: {producto.existencias} | "
            f"Categoría: {producto.categoria.nombre} | "
            f"Proveedor(es): {proveedores}"
        )

    @staticmethod
    def _leer_entero(mensaje):
        try:
            return int(input(mensaje))
        except ValueError as error:
            raise ValueError(
                "Debes ingresar un número entero."
            ) from error

    @staticmethod
    def _leer_float(mensaje):
        try:
            return float(input(mensaje))
        except ValueError as error:
            raise ValueError(
                "Debes ingresar un número válido."
            ) from error
