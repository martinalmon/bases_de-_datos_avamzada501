# Tienda La Económica - BDOO con ZODB

Proyecto para la materia de Base de Datos Avanzada.

El sistema utiliza Python, Programación Orientada a Objetos y ZODB.

## Clases implementadas

- Categoria
- Proveedor
- Cliente
- Producto
- DetalleVenta
- Venta
- Inventario

## Funciones principales

El sistema permite:

- Alta de objetos.
- Consulta de productos.
- Modificación de productos.
- Eliminación de productos.
- Registrar ventas.
- Agregar productos a una venta.
- Actualizar inventario automáticamente.
- Incrementar existencias.
- Disminuir existencias.
- Calcular el total de una venta.

## Consultas

1. Mostrar todos los productos registrados.
2. Mostrar productos cuyo precio sea superior a una cantidad.
3. Mostrar productos disponibles o con existencias menores a un límite.
4. Mostrar productos proporcionados por un proveedor.
5. Mostrar el total obtenido por ventas.

## Instalación

En la terminal:

```bash
pip install -r requirements.txt
```

Después:

```bash
python main.py
```

## Prueba de persistencia

La base de datos se guarda en el archivo `tienda.fs`.

Para demostrar que los objetos permanecen almacenados:

1. Ejecutar `python main.py`.
2. Seleccionar la opción 18 para cargar datos de prueba, o registrar objetos manualmente.
3. Consultar los productos.
4. Elegir la opción 0 para salir.
5. Ejecutar otra vez `python main.py`.
6. Al iniciar, el programa mostrará cuántos objetos fueron recuperados desde ZODB.
7. Seleccionar la opción 12 para comprobar que los productos siguen disponibles.

Los cambios se guardan usando `transaction.commit()`.

## Archivo de base de datos

Los archivos generados por ZODB no deben subirse al repositorio. Por eso se incluyen en `.gitignore`.
