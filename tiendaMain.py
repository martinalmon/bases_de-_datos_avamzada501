import ZODB
import ZODB.FileStorage
import transaction

from datetime import datetime
from persistent import Persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping


class Categoria(Persistent):
    def __init__(self, id_categoria, nombre, descripcion):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion

    def modificar(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion


class Proveedor(Persistent):
    def __init__(self, id_proveedor, nombre, telefono, correo):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.productos = PersistentList()

    def agregar_producto(self, producto):
        if producto not in self.productos:
            self.productos.append(producto)

    def eliminar_producto(self, producto):
        if producto in self.productos:
            self.productos.remove(producto)

    def modificar(self, nombre, telefono, correo):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo


class Cliente(Persistent):
    def __init__(self, id_cliente, nombre, telefono, correo):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo

    def modificar(self, nombre, telefono, correo):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo


class Producto(Persistent):
    def __init__(self, codigo, nombre, descripcion, precio, existencias, categoria):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.existencias = existencias
        self.categoria = categoria
        self.proveedores = PersistentList()

    def agregar_proveedor(self, proveedor):
        if proveedor not in self.proveedores:
            self.proveedores.append(proveedor)

        if self not in proveedor.productos:
            proveedor.productos.append(self)

    def incrementar_existencias(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self.existencias += cantidad

    def disminuir_existencias(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if cantidad > self.existencias:
            raise ValueError("No hay existencias suficientes.")

        self.existencias -= cantidad

    def modificar(self, nombre, descripcion, precio, categoria):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria


class DetalleVenta(Persistent):
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = producto.precio
        self.subtotal = self.precio_unitario * cantidad


class Venta(Persistent):
    def __init__(self, id_venta, cliente):
        self.id_venta = id_venta
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cliente = cliente
        self.detalles = PersistentList()
        self.total = 0.0

    def agregar_producto(self, producto, cantidad):
        producto.disminuir_existencias(cantidad)

        detalle = DetalleVenta(producto, cantidad)
        self.detalles.append(detalle)

        self.calcular_total()

    def calcular_total(self):
        self.total = sum(detalle.subtotal for detalle in self.detalles)
        return self.total


class Inventario(Persistent):
    def __init__(self):
        self.productos = PersistentMapping()

    def alta_producto(self, producto):
        if producto.codigo in self.productos:
            raise ValueError("Ya existe un producto con ese código.")

        self.productos[producto.codigo] = producto

    def consultar_producto(self, codigo):
        return self.productos.get(codigo)

    def modificar_producto(self, codigo, nombre, descripcion, precio, categoria):
        producto = self.consultar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        producto.modificar(nombre, descripcion, precio, categoria)

    def eliminar_producto(self, codigo):
        producto = self.consultar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        for proveedor in list(producto.proveedores):
            proveedor.eliminar_producto(producto)

        del self.productos[codigo]

    def incrementar_existencias(self, codigo, cantidad):
        producto = self.consultar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        producto.incrementar_existencias(cantidad)

    def disminuir_existencias(self, codigo, cantidad):
        producto = self.consultar_producto(codigo)

        if producto is None:
            raise ValueError("Producto no encontrado.")

        producto.disminuir_existencias(cantidad)


def abrir_bd():
    storage = ZODB.FileStorage.FileStorage("tienda.fs")
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root()

    if "categorias" not in root:
        root["categorias"] = PersistentMapping()

    if "proveedores" not in root:
        root["proveedores"] = PersistentMapping()

    if "clientes" not in root:
        root["clientes"] = PersistentMapping()

    if "ventas" not in root:
        root["ventas"] = PersistentMapping()

    if "inventario" not in root:
        root["inventario"] = Inventario()

    transaction.commit()

    return storage, db, connection, root


def cerrar_bd(storage, db, connection):
    connection.close()
    db.close()
    storage.close()


def mostrar_producto(producto):
    proveedores = ", ".join(
        proveedor.nombre for proveedor in producto.proveedores
    )

    if proveedores == "":
        proveedores = "Sin proveedor"

    print(
        f"Código: {producto.codigo} | "
        f"Nombre: {producto.nombre} | "
        f"Precio: ${producto.precio:.2f} | "
        f"Existencias: {producto.existencias} | "
        f"Categoría: {producto.categoria.nombre} | "
        f"Proveedor(es): {proveedores}"
    )


def alta_categoria(root):
    id_categoria = input("ID de categoría: ").strip()

    if id_categoria in root["categorias"]:
        print("Esa categoría ya existe.")
        return

    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()

    root["categorias"][id_categoria] = Categoria(
        id_categoria,
        nombre,
        descripcion
    )

    transaction.commit()
    print("Categoría guardada.")


def alta_proveedor(root):
    id_proveedor = input("ID de proveedor: ").strip()

    if id_proveedor in root["proveedores"]:
        print("Ese proveedor ya existe.")
        return

    nombre = input("Nombre: ").strip()
    telefono = input("Teléfono: ").strip()
    correo = input("Correo: ").strip()

    root["proveedores"][id_proveedor] = Proveedor(
        id_proveedor,
        nombre,
        telefono,
        correo
    )

    transaction.commit()
    print("Proveedor guardado.")


def alta_cliente(root):
    id_cliente = input("ID de cliente: ").strip()

    if id_cliente in root["clientes"]:
        print("Ese cliente ya existe.")
        return

    nombre = input("Nombre: ").strip()
    telefono = input("Teléfono: ").strip()
    correo = input("Correo: ").strip()

    root["clientes"][id_cliente] = Cliente(
        id_cliente,
        nombre,
        telefono,
        correo
    )

    transaction.commit()
    print("Cliente guardado.")


def alta_producto(root):
    inventario = root["inventario"]

    codigo = input("Código del producto: ").strip()

    if inventario.consultar_producto(codigo) is not None:
        print("Ese producto ya existe.")
        return

    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()

    try:
        precio = float(input("Precio: "))
        existencias = int(input("Existencias: "))
    except ValueError:
        print("Precio o existencias no válidos.")
        return

    if precio < 0 or existencias < 0:
        print("El precio y las existencias no pueden ser negativos.")
        return

    id_categoria = input("ID de categoría: ").strip()
    categoria = root["categorias"].get(id_categoria)

    if categoria is None:
        print("La categoría no existe.")
        return

    producto = Producto(
        codigo,
        nombre,
        descripcion,
        precio,
        existencias,
        categoria
    )

    inventario.alta_producto(producto)

    transaction.commit()
    print("Producto guardado.")


def asociar_proveedor(root):
    codigo = input("Código del producto: ").strip()
    id_proveedor = input("ID del proveedor: ").strip()

    producto = root["inventario"].consultar_producto(codigo)
    proveedor = root["proveedores"].get(id_proveedor)

    if producto is None:
        print("Producto no encontrado.")
        return

    if proveedor is None:
        print("Proveedor no encontrado.")
        return

    producto.agregar_proveedor(proveedor)

    transaction.commit()
    print("Proveedor asociado al producto.")


def consultar_producto(root):
    codigo = input("Código del producto: ").strip()
    producto = root["inventario"].consultar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
        return

    mostrar_producto(producto)


def modificar_producto(root):
    codigo = input("Código del producto: ").strip()
    producto = root["inventario"].consultar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
        return

    nombre = input(f"Nombre [{producto.nombre}]: ").strip()
    descripcion = input(
        f"Descripción [{producto.descripcion}]: "
    ).strip()
    precio_texto = input(f"Precio [{producto.precio}]: ").strip()
    categoria_texto = input(
        f"ID categoría [{producto.categoria.id_categoria}]: "
    ).strip()

    if nombre == "":
        nombre = producto.nombre

    if descripcion == "":
        descripcion = producto.descripcion

    if precio_texto == "":
        precio = producto.precio
    else:
        try:
            precio = float(precio_texto)
        except ValueError:
            print("Precio no válido.")
            return

    if categoria_texto == "":
        categoria = producto.categoria
    else:
        categoria = root["categorias"].get(categoria_texto)

        if categoria is None:
            print("La categoría no existe.")
            return

    try:
        root["inventario"].modificar_producto(
            codigo,
            nombre,
            descripcion,
            precio,
            categoria
        )
        transaction.commit()
        print("Producto modificado.")
    except ValueError as error:
        print(error)


def eliminar_producto(root):
    codigo = input("Código del producto: ").strip()

    try:
        root["inventario"].eliminar_producto(codigo)
        transaction.commit()
        print("Producto eliminado.")
    except ValueError as error:
        print(error)


def incrementar_existencias(root):
    codigo = input("Código del producto: ").strip()

    try:
        cantidad = int(input("Cantidad recibida: "))
        root["inventario"].incrementar_existencias(
            codigo,
            cantidad
        )
        transaction.commit()
        print("Existencias incrementadas.")
    except ValueError as error:
        print(error)


def disminuir_existencias(root):
    codigo = input("Código del producto: ").strip()

    try:
        cantidad = int(input("Cantidad a disminuir: "))
        root["inventario"].disminuir_existencias(
            codigo,
            cantidad
        )
        transaction.commit()
        print("Existencias disminuidas.")
    except ValueError as error:
        print(error)


def registrar_venta(root):
    id_cliente = input("ID del cliente: ").strip()
    cliente = root["clientes"].get(id_cliente)

    if cliente is None:
        print("Cliente no encontrado.")
        return

    id_venta = f"V{len(root['ventas']) + 1:03d}"
    venta = Venta(id_venta, cliente)

    print("Escribe FIN cuando termines de agregar productos.")

    while True:
        codigo = input("Código del producto: ").strip()

        if codigo.upper() == "FIN":
            break

        producto = root["inventario"].consultar_producto(codigo)

        if producto is None:
            print("Producto no encontrado.")
            continue

        try:
            cantidad = int(input("Cantidad: "))
            venta.agregar_producto(producto, cantidad)
            print("Producto agregado a la venta.")
        except ValueError as error:
            print(error)

    if len(venta.detalles) == 0:
        transaction.abort()
        print("La venta no contiene productos.")
        return

    root["ventas"][id_venta] = venta

    transaction.commit()

    print(f"Venta {id_venta} registrada.")
    print(f"Total: ${venta.calcular_total():.2f}")


def mostrar_todos_productos(root):
    productos = root["inventario"].productos

    if len(productos) == 0:
        print("No hay productos registrados.")
        return

    for producto in productos.values():
        mostrar_producto(producto)


def productos_precio_superior(root):
    try:
        cantidad = float(
            input("Mostrar productos con precio superior a: $")
        )
    except ValueError:
        print("Cantidad no válida.")
        return

    encontrados = False

    for producto in root["inventario"].productos.values():
        if producto.precio > cantidad:
            mostrar_producto(producto)
            encontrados = True

    if not encontrados:
        print("No se encontraron productos.")


def productos_disponibles_o_bajos(root):
    print("1. Productos disponibles")
    print("2. Productos con existencias menores a un límite")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        encontrados = False

        for producto in root["inventario"].productos.values():
            if producto.existencias > 0:
                mostrar_producto(producto)
                encontrados = True

        if not encontrados:
            print("No hay productos disponibles.")

    elif opcion == "2":
        try:
            limite = int(input("Límite de existencias: "))
        except ValueError:
            print("Límite no válido.")
            return

        encontrados = False

        for producto in root["inventario"].productos.values():
            if producto.existencias < limite:
                mostrar_producto(producto)
                encontrados = True

        if not encontrados:
            print("No se encontraron productos.")

    else:
        print("Opción no válida.")


def productos_por_proveedor(root):
    id_proveedor = input("ID del proveedor: ").strip()
    proveedor = root["proveedores"].get(id_proveedor)

    if proveedor is None:
        print("Proveedor no encontrado.")
        return

    if len(proveedor.productos) == 0:
        print("Ese proveedor no tiene productos asociados.")
        return

    print(f"Productos proporcionados por {proveedor.nombre}:")

    for producto in proveedor.productos:
        mostrar_producto(producto)


def total_ventas(root):
    total = sum(
        venta.calcular_total()
        for venta in root["ventas"].values()
    )

    print(f"Total obtenido por ventas: ${total:.2f}")


def mostrar_ventas(root):
    if len(root["ventas"]) == 0:
        print("No hay ventas registradas.")
        return

    for venta in root["ventas"].values():
        print(
            f"\nVenta: {venta.id_venta} | "
            f"Fecha: {venta.fecha} | "
            f"Cliente: {venta.cliente.nombre}"
        )

        for detalle in venta.detalles:
            print(
                f"  {detalle.producto.nombre} | "
                f"Cantidad: {detalle.cantidad} | "
                f"Subtotal: ${detalle.subtotal:.2f}"
            )

        print(f"Total: ${venta.total:.2f}")


def mostrar_datos_recuperados(root):
    print("\nDatos almacenados actualmente en ZODB:")
    print(
        f"Categorías: {len(root['categorias'])} | "
        f"Proveedores: {len(root['proveedores'])} | "
        f"Clientes: {len(root['clientes'])} | "
        f"Productos: {len(root['inventario'].productos)} | "
        f"Ventas: {len(root['ventas'])}"
    )

    if len(root["inventario"].productos) > 0:
        print(
            "Los objetos fueron recuperados desde la base tienda.fs."
        )


def cargar_datos_prueba(root):
    if (
        len(root["categorias"]) > 0
        or len(root["proveedores"]) > 0
        or len(root["clientes"]) > 0
        or len(root["inventario"].productos) > 0
    ):
        print("Ya existen datos. No se cargaron datos de prueba.")
        return

    abarrotes = Categoria(
        "C01",
        "Abarrotes",
        "Productos básicos de consumo"
    )

    bebidas = Categoria(
        "C02",
        "Bebidas",
        "Bebidas para consumo"
    )

    proveedor1 = Proveedor(
        "P01",
        "Distribuidora del Centro",
        "2281001000",
        "ventas@distribuidora.com"
    )

    proveedor2 = Proveedor(
        "P02",
        "Comercializadora Veracruz",
        "2282002000",
        "pedidos@comercializadora.com"
    )

    cliente1 = Cliente(
        "CL01",
        "Ana López",
        "2283003000",
        "ana@email.com"
    )

    producto1 = Producto(
        "A001",
        "Arroz 1 kg",
        "Bolsa de arroz",
        32.50,
        20,
        abarrotes
    )

    producto2 = Producto(
        "B001",
        "Refresco 600 ml",
        "Refresco individual",
        20.00,
        15,
        bebidas
    )

    producto3 = Producto(
        "A002",
        "Aceite 1 L",
        "Aceite vegetal",
        45.00,
        5,
        abarrotes
    )

    producto1.agregar_proveedor(proveedor1)
    producto2.agregar_proveedor(proveedor2)
    producto3.agregar_proveedor(proveedor1)
    producto3.agregar_proveedor(proveedor2)

    root["categorias"]["C01"] = abarrotes
    root["categorias"]["C02"] = bebidas

    root["proveedores"]["P01"] = proveedor1
    root["proveedores"]["P02"] = proveedor2

    root["clientes"]["CL01"] = cliente1

    root["inventario"].alta_producto(producto1)
    root["inventario"].alta_producto(producto2)
    root["inventario"].alta_producto(producto3)

    transaction.commit()

    print("Datos de prueba guardados con transaction.commit().")


def menu():
    storage, db, connection, root = abrir_bd()

    try:
        mostrar_datos_recuperados(root)

        while True:
            print("\nTIENDA LA ECONÓMICA")
            print("1. Alta de categoría")
            print("2. Alta de proveedor")
            print("3. Alta de cliente")
            print("4. Alta de producto")
            print("5. Asociar proveedor a producto")
            print("6. Consultar producto")
            print("7. Modificar producto")
            print("8. Eliminar producto")
            print("9. Incrementar existencias")
            print("10. Disminuir existencias")
            print("11. Registrar venta")
            print("12. Mostrar todos los productos")
            print("13. Productos con precio superior")
            print("14. Productos disponibles o con pocas existencias")
            print("15. Productos por proveedor")
            print("16. Total de ventas")
            print("17. Mostrar ventas")
            print("18. Cargar datos de prueba")
            print("0. Salir")

            opcion = input("Selecciona una opción: ").strip()

            if opcion == "1":
                alta_categoria(root)

            elif opcion == "2":
                alta_proveedor(root)

            elif opcion == "3":
                alta_cliente(root)

            elif opcion == "4":
                alta_producto(root)

            elif opcion == "5":
                asociar_proveedor(root)

            elif opcion == "6":
                consultar_producto(root)

            elif opcion == "7":
                modificar_producto(root)

            elif opcion == "8":
                eliminar_producto(root)

            elif opcion == "9":
                incrementar_existencias(root)

            elif opcion == "10":
                disminuir_existencias(root)

            elif opcion == "11":
                registrar_venta(root)

            elif opcion == "12":
                mostrar_todos_productos(root)

            elif opcion == "13":
                productos_precio_superior(root)

            elif opcion == "14":
                productos_disponibles_o_bajos(root)

            elif opcion == "15":
                productos_por_proveedor(root)

            elif opcion == "16":
                total_ventas(root)

            elif opcion == "17":
                mostrar_ventas(root)

            elif opcion == "18":
                cargar_datos_prueba(root)

            elif opcion == "0":
                transaction.commit()
                print("Cambios guardados.")
                print(
                    "Cierra el programa y vuelve a ejecutar main.py "
                    "para comprobar la persistencia."
                )
                break

            else:
                print("Opción no válida.")

    finally:
        cerrar_bd(storage, db, connection)


if __name__ == "__main__":
    menu()
