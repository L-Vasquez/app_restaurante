import sys
from PySide6.QtWidgets import QDialog, QLineEdit, QFormLayout, QPushButton, QMessageBox
from conexion import ejecutar_consulta

class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión - Sistema de Restaurante")
        self.resize(320, 160)
        self.setModal(True)

        layout = QFormLayout(self)

        self.input_usuario = QLineEdit()
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        layout.addRow("Usuario:", self.input_usuario)
        layout.addRow("Contraseña:", self.input_password)

        btn_login = QPushButton("Ingresar")
        btn_login.clicked.connect(self.verificar_credenciales)
        layout.addRow(btn_login)

        self.usuario_valido = False

    def verificar_credenciales(self):
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text().strip()

        if not usuario or not password:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, completa todos los campos.")
            return

        # Consulta centralizada usando conexion.py
        query = "SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ? AND activo = 1"
        resultado = ejecutar_consulta(query, (usuario, password), es_lectura=True)

        if resultado:
            self.usuario_valido = True
            self.accept()
        else:
            QMessageBox.critical(self, "Error de acceso", "Usuario o contraseña incorrectos, o cuenta inactiva.")