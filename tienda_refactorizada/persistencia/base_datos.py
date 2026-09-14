"""Persistencia del sistema mediante ZODB."""

import transaction
import ZODB
import ZODB.FileStorage

from persistent.mapping import PersistentMapping

from constantes import NOMBRE_BASE_DATOS
from modelos.inventario import Inventario


class BaseDatosZODB:
    """Administra la conexión y las transacciones de ZODB."""

    def __init__(self, ruta=NOMBRE_BASE_DATOS):
        self.ruta = ruta
        self.storage = None
        self.db = None
        self.connection = None
        self.root = None

    def abrir(self):
        """Abre la base de datos e inicializa sus colecciones."""
        self.storage = ZODB.FileStorage.FileStorage(self.ruta)
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()
        self._inicializar_estructura()
        return self.root

    def _inicializar_estructura(self):
        """Crea las colecciones principales si todavía no existen."""
        if "categorias" not in self.root:
            self.root["categorias"] = PersistentMapping()

        if "proveedores" not in self.root:
            self.root["proveedores"] = PersistentMapping()

        if "clientes" not in self.root:
            self.root["clientes"] = PersistentMapping()

        if "ventas" not in self.root:
            self.root["ventas"] = PersistentMapping()

        if "inventario" not in self.root:
            self.root["inventario"] = Inventario()

        self.confirmar_cambios()

    def confirmar_cambios(self):
        """Guarda permanentemente los cambios realizados."""
        transaction.commit()

    def cancelar_cambios(self):
        """Cancela los cambios de la transacción actual."""
        transaction.abort()

    def cerrar(self):
        """Cierra de forma segura la conexión con ZODB."""
        if self.connection is not None:
            self.connection.close()

        if self.db is not None:
            self.db.close()

        if self.storage is not None:
            self.storage.close()
