import sys
import sqlite3
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, 
    QPushButton, QMessageBox, QVBoxLayout
)
from conexion import ejecutar_consulta

class FormularioProducto(QDialog):
    def __init__(self, id_producto=None):
        super().__init__()
        self.id_producto = id_producto  # Si es None, es Registro. Si tiene ID, es Edición.
        
        titulo = "Editar Producto" if self.id_producto else "Registrar Nuevo Producto"
        self.setWindowTitle(titulo)
        self.resize(300, 250)
        self.setModal(True)

        layout = QFormLayout(self)

        # Campos del formulario
        self.input_nombre = QLineEdit()
        self.input_precio = QLineEdit()
        self.combo_tipo = QComboBox()
        
        # Cargar los tipos de productos desde la BD (Platos, Bebidas, etc.)
        self.cargar_tipos_producto()

        layout.addRow("Nombre del producto:", self.input_nombre)
        layout.addRow("Precio (S/.):", self.input_precio)
        layout.addRow("Tipo de producto:", self.combo_tipo)

        # Botón Guardar
        btn_guardar = QPushButton("Actualizar" if self.id_producto else "Guardar")
        btn_guardar.clicked.connect(self.guardar_datos)
        layout.addRow(btn_guardar)

        # Si estamos editando, rellenar los campos con los datos actuales
        if self.id_producto:
            self.cargar_datos_producto()

    def cargar_tipos_producto(self):
        """Carga las categorías o tipos de la base de datos en el ComboBox."""
        tipos = ejecutar_consulta("SELECT id_tipo, nombre FROM tipos_producto", es_lectura=True)
        if tipos:
            for id_tipo, nombre in tipos:
                self.combo_tipo.addItem(nombre, id_tipo) # Guardamos el ID como valor interno

    def cargar_datos_producto(self):
        """Rellena los campos al abrir la ventana en modo edición."""
        resultado = ejecutar_consulta(
            "SELECT nombre, precio, id_tipo FROM productos WHERE id_producto = ?", 
            (self.id_producto,), 
            es_lectura=True
        )
        if resultado:
            nombre, precio, id_tipo = resultado[0]
            self.input_nombre.setText(nombre)
            self.input_precio.setText(str(precio))
            
            # Seleccionar el tipo correspondiente en el ComboBox
            index = self.combo_tipo.findData(id_tipo)
            if index >= 0:
                self.combo_tipo.setCurrentIndex(index)

    def guardar_datos(self):
        nombre = self.input_nombre.text().strip()
        precio_texto = self.input_precio.text().strip()
        id_tipo = self.combo_tipo.currentData()

        if not nombre or not precio_texto:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, completa todos los campos.")
            return

        try:
            precio = float(precio_texto)
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "El precio debe ser un número válido.")
            return

        if self.id_producto:
            # Operación de UPDATE (Editar)
            query = "UPDATE productos SET nombre = ?, precio = ?, id_tipo = ? WHERE id_producto = ?"
            ejecutar_consulta(query, (nombre, precio, id_tipo, self.id_producto), es_lectura=False)
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
        else:
            # Operación de INSERT (Registrar)
            query = "INSERT INTO productos (nombre, precio, id_tipo, activo) VALUES (?, ?, ?, 1)"
            ejecutar_consulta(query, (nombre, precio, id_tipo), es_lectura=False)
            QMessageBox.information(self, "Éxito", "Producto registrado correctamente.")

        self.accept()