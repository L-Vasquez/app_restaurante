import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QPushButton, QStyle, QMessageBox, QToolBar, QDialog
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize, Qt
from login import VentanaLogin

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Ventas - Restaurante")
        self.resize(750, 500)

        estilo = QApplication.style()
        
        # Íconos del sistema
        icon_inicio = estilo.standardIcon(QStyle.SP_ComputerIcon)
        icon_registrar = estilo.standardIcon(QStyle.SP_FileDialogNewFolder)
        icon_producto = estilo.standardIcon(QStyle.SP_FileIcon)
        icon_reporte = estilo.standardIcon(QStyle.SP_FileDialogDetailedView)
        icon_usuario = estilo.standardIcon(QStyle.SP_DirIcon)
        icon_buscar = estilo.standardIcon(QStyle.SP_FileDialogContentsView)
        icon_salir = estilo.standardIcon(QStyle.SP_DialogCloseButton)

        # -------------------------------------------------------------
        # Menú Superior Horizontal (QToolBar)
        # -------------------------------------------------------------
        barra_herramientas = QToolBar("Menú Principal")
        barra_herramientas.setMovable(False)
        barra_herramientas.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        barra_herramientas.setIconSize(QSize(20, 20))
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, barra_herramientas)

        barra_herramientas.setStyleSheet("""
            QToolBar {
                background-color: #f0f0f0;
                padding: 5px;
                border-bottom: 1px solid #cccccc;
                spacing: 8px;
            }
            QToolButton {
                border: 1px solid #a0a0a0;
                border-radius: 4px;
                background-color: #ffffff;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
                border-color: #707070;
            }
            QToolButton:pressed {
                background-color: #d0d0d0;
            }
        """)

        # Acciones de la barra superior (exactamente las 5 pedidas)
        action_inicio = QAction(icon_inicio, "Inicio", self)
        action_registrar = QAction(icon_registrar, "Registrar venta", self)
        action_producto = QAction(icon_producto, "Registrar producto", self)
        action_reporte = QAction(icon_reporte, "Reporte sistema", self)
        action_salir = QAction(icon_salir, "Salir", self)

        # Conectar acciones de la barra superior
        action_inicio.triggered.connect(self.ir_inicio)
        action_registrar.triggered.connect(self.registrar_venta)
        action_producto.triggered.connect(self.registrar_producto)
        action_reporte.triggered.connect(self.reporte_sistema)
        action_salir.triggered.connect(self.close)

        # Añadir a la barra superior
        barra_herramientas.addAction(action_inicio)
        barra_herramientas.addSeparator()
        barra_herramientas.addAction(action_registrar)
        barra_herramientas.addAction(action_producto)
        barra_herramientas.addAction(action_reporte)
        barra_herramientas.addAction(action_salir)

        # -------------------------------------------------------------
        # Contenedor y Layout principal del cuerpo (Botones centrales)
        # -------------------------------------------------------------
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(20, 20, 20, 20)

        grid_botones = QGridLayout()
        grid_botones.setSpacing(15)

        # Botones centrales (todas las opciones del sistema)
        btn_registrar = self.crear_boton_grande("Registrar Venta", icon_registrar)
        btn_producto = self.crear_boton_grande("Registrar Producto", icon_producto)
        btn_usuario = self.crear_boton_grande("Registrar Usuario", icon_usuario)
        btn_reporte = self.crear_boton_grande("Reporte Sistema", icon_reporte)
        btn_buscar = self.crear_boton_grande("Búsqueda de Venta", icon_buscar)
        btn_salir = self.crear_boton_grande("Salir", icon_salir)

        # Conectar botones centrales
        btn_registrar.clicked.connect(self.registrar_venta)
        btn_producto.clicked.connect(self.registrar_producto)
        btn_usuario.clicked.connect(self.registrar_usuario)
        btn_reporte.clicked.connect(self.reporte_sistema)
        btn_buscar.clicked.connect(self.buscar_venta)
        btn_salir.clicked.connect(self.close)

        # Organizar en cuadrícula (3 filas x 2 columnas)
        grid_botones.addWidget(btn_registrar, 0, 0)
        grid_botones.addWidget(btn_producto, 0, 1)
        grid_botones.addWidget(btn_usuario, 1, 0)
        grid_botones.addWidget(btn_reporte, 1, 1)
        grid_botones.addWidget(btn_buscar, 2, 0)
        grid_botones.addWidget(btn_salir, 2, 1)

        layout_principal.addLayout(grid_botones)

    def crear_boton_grande(self, texto, icono):
        btn = QPushButton(texto)
        btn.setIcon(icono)
        btn.setIconSize(QSize(35, 35))
        btn.setMinimumSize(180, 80)
        btn.setStyleSheet("""
            QPushButton {
                font-size: 15px;
                font-weight: bold;
                padding: 10px;
                border: 2px solid #8f8f91;
                border-radius: 8px;
                background-color: #f8f9fa;
            }
            QPushButton:hover {
                background-color: #e2e6ea;
                border-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #dae0e5;
            }
        """)
        return btn

    # Métodos de navegación
    def ir_inicio(self):
        QMessageBox.information(self, "Inicio", "Te encuentras en la pantalla principal del sistema.")

    def registrar_venta(self):
        QMessageBox.information(self, "Opción Seleccionada", "Has seleccionado: Registrar venta")

    def registrar_producto(self):
        QMessageBox.information(self, "Opción Seleccionada", "Has seleccionado: Registrar producto")

    def registrar_usuario(self):
        QMessageBox.information(self, "Opción Seleccionada", "Has seleccionado: Registrar usuario")

    def reporte_sistema(self):
        QMessageBox.information(self, "Opción Seleccionada", "Has seleccionado: Reporte sistema")

    def buscar_venta(self):
        QMessageBox.information(self, "Opción Seleccionada", "Has seleccionado: Búsqueda de venta")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Control de flujo: Ejecutar login primero
    login = VentanaLogin()
    if login.exec() == QDialog.Accepted and login.usuario_valido:
        ventana = VentanaPrincipal()
        ventana.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)