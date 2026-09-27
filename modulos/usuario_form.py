import sys
import sqlite3
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, 
    QPushButton, QMessageBox, QVBoxLayout
)
from conexion import ejecutar_consulta

class FormularioUsuario(QDialog):
    def __init__(self, id_usuario=None):
        super().__init__()
        self.id_usuario = id_usuario  # Si es None, es Registro. Si tiene ID, es Edición.
        
        titulo = "Editar Usuario" if self.id_usuario else "Registrar Nuevo Usuario"
        self.setWindowTitle(titulo)
        self.resize(320, 280)
        self.setModal(True)

        layout = QFormLayout(self)

        # Campos del formulario (según las columnas de la tabla 'usuarios')
        self.input_usuario = QLineEdit()
        self.input_nombre = QLineEdit()
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        
        # ComboBox para el estado (Activo / Inactivo)
        self.combo_activo = QComboBox()
        self.combo_activo.addItem("Activo", 1)
        self.combo_activo.addItem("Inactivo", 0)

        layout.addRow("Nombre de usuario:", self.input_usuario)
        layout.addRow("Nombre completo:", self.input_nombre)
        layout.addRow("Contraseña:", self.input_password)
        layout.addRow("Estado:", self.combo_activo)

        # Botón Guardar
        btn_guardar = QPushButton("Actualizar" if self.id_usuario else "Guardar")
        btn_guardar.clicked.connect(self.guardar_datos)
        layout.addRow(btn_guardar)

        # Si estamos editando, rellenar los campos con los datos actuales
        if self.id_usuario:
            self.cargar_datos_usuario()

    def cargar_datos_usuario(self):
        """Rellena los campos al abrir la ventana en modo edición."""
        resultado = ejecutar_consulta(
            "SELECT usuario, nombre, activo FROM usuarios WHERE id_usuario = ?", 
            (self.id_usuario,), 
            es_lectura=True
        )
        if resultado:
            usuario, nombre, activo = resultado[0]
            self.input_usuario.setText(usuario)
            self.input_nombre.setText(nombre)
            self.input_password.setPlaceholderText("(Dejar en blanco para no cambiar)")
            
            # Seleccionar estado actual
            index = self.combo_activo.findData(activo)
            if index >= 0:
                self.combo_activo.setCurrentIndex(index)

    def guardar_datos(self):
        usuario = self.input_usuario.text().strip()
        nombre = self.input_nombre.text().strip()
        password = self.input_password.text().strip()
        activo = self.combo_activo.currentData()

        if not usuario or not nombre:
            QMessageBox.warning(self, "Campos vacíos", "El usuario y el nombre completo son obligatorios.")
            return

        if not self.id_usuario and not password:
            QMessageBox.warning(self, "Contraseña requerida", "Debes ingresar una contraseña para el nuevo usuario.")
            return

        try:
            if self.id_usuario:
                # Operación de UPDATE (Editar)
                if password:
                    # Si ingresó una nueva contraseña, la actualizamos también
                    query = "UPDATE usuarios SET usuario = ?, nombre = ?, contraseña = ?, activo = ? WHERE id_usuario = ?"
                    ejecutar_consulta(query, (usuario, nombre, password, activo, self.id_usuario), es_lectura=False)
                else:
                    # Si dejó la contraseña en blanco, no la sobrescribimos
                    query = "UPDATE usuarios SET usuario = ?, nombre = ?, activo = ? WHERE id_usuario = ?"
                    ejecutar_consulta(query, (usuario, nombre, activo, self.id_usuario), es_lectura=False)
                
                QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente.")
            else:
                # Operación de INSERT (Registrar)
                query = "INSERT INTO usuarios (usuario, nombre, contraseña, activo) VALUES (?, ?, ?, ?)"
                ejecutar_consulta(query, (usuario, nombre, password, activo), es_lectura=False)
                QMessageBox.information(self, "Éxito", "Usuario registrado correctamente.")

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el usuario:\n{e}")