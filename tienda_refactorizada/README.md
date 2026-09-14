# Tienda La Económica - BDOO con ZODB

Proyecto de Base de Datos Avanzada desarrollado en Python y ZODB.

Esta versión corresponde a la refactorización del proyecto original. El sistema
mantiene el mismo propósito, pero ahora está organizado en módulos separados
para mejorar su legibilidad, mantenimiento y reutilización.

## Funciones principales

El sistema permite:

- Registrar categorías.
- Registrar proveedores.
- Registrar clientes.
- Registrar productos.
- Consultar productos.
- Modificar productos.
- Eliminar productos.
- Asociar proveedores a productos.
- Incrementar y disminuir existencias.
- Registrar ventas.
- Actualizar el inventario al vender.
- Calcular el total de una venta.
- Consultar productos disponibles.
- Consultar productos con bajo stock.
- Consultar productos por proveedor.
- Consultar ventas por cliente.
- Consultar productos más vendidos.
- Consultar el total acumulado de ventas.
- Generar un reporte de venta total diaria.

## Estructura del proyecto

```text
tienda_bdoo_refactorizada/
│
├── modelos/
│   ├── __init__.py
│   ├── categoria.py
│   ├── cliente.py
│   ├── inventario.py
│   ├── producto.py
│   ├── proveedor.py
│   └── venta.py
│
├── persistencia/
│   ├── __init__.py
│   └── base_datos.py
│
├── servicios/
│   ├── __init__.py
│   ├── catalogo_service.py
│   ├── producto_service.py
│   └── venta_service.py
│
├── consultas/
│   ├── __init__.py
│   └── consultas.py
│
├── interfaz/
│   ├── __init__.py
│   └── consola.py
│
├── constantes.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Responsabilidades

### Modelos

Contienen las clases que representan los objetos de la tienda:

- Categoria
- Cliente
- Proveedor
- Producto
- Inventario
- Venta
- DetalleVenta

### Persistencia

`persistencia/base_datos.py` se encarga de:

- Abrir ZODB.
- Crear la conexión.
- Inicializar las colecciones.
- Ejecutar commit.
- Ejecutar abort cuando es necesario.
- Cerrar la base de datos.

### Servicios

Contienen la lógica de negocio:

- Registro de productos.
- Modificación y eliminación.
- Actualización de inventario.
- Asociación de proveedores.
- Registro de ventas.
- Cálculo de totales.

### Consultas

`consultas/consultas.py` contiene las operaciones de lectura y reportes.

### Interfaz

`interfaz/consola.py` contiene únicamente la interacción por línea de comandos.
La lógica de negocio no se encuentra dentro de la interfaz, por lo que
posteriormente puede sustituirse por una interfaz gráfica sin reescribir los
servicios ni los modelos.

## Instalación

En la terminal, dentro de la carpeta del proyecto:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Persistencia

ZODB crea el archivo `tienda.fs`. La información almacenada permanece disponible
después de cerrar y volver a ejecutar el programa.

Los archivos generados por la base de datos están incluidos en `.gitignore`
para evitar subirlos al repositorio.

## Convenciones aplicadas

- Variables y funciones en `snake_case`.
- Clases en `PascalCase`.
- Constantes en mayúsculas.
- Nombres descriptivos.
- Docstrings en clases y funciones importantes.
- Manejo específico de excepciones.
- Validación de datos antes de almacenar información.
- Separación entre modelos, persistencia, servicios, consultas e interfaz.
- Importaciones explícitas y organizadas.
- Uso de `if __name__ == "__main__"` en el punto de entrada.
