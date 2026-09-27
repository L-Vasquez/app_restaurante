import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QPushButton, QStyle, QMessageBox, QToolBar, QDialog
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize, Qt

# Importar las ventanas de autenticación y los nuevos módulos
from login import VentanaLogin
from modulos.producto_form import FormularioProducto
from modulos.usuario_form import FormularioUsuario
from modulos.venta_form import FormularioVenta
from modulos.busqueda_venta import FormularioBusquedaVenta
from modulos.reporte_ventas import FormularioReporteVentas

class VentanaPrincipal(QMainWindow):
    def __init__(self, id_usuario_actual=1):
        super().__init__()
        self.id_usuario_actual = id_usuario_actual  # Guardamos el ID del usuario logueado

        self.setWindowTitle("Sistema de Ventas - Restaurante")
        self.resize(750, 520)

        estilo = QApplication.style()
        
        # Íconos clásicos del sistema
        icon_inicio = estilo.standardIcon(QStyle.SP_ComputerIcon)
        icon_registrar = estilo.standardIcon(QStyle.SP_FileDialogNewFolder)
        icon_producto = estilo.standardIcon(QStyle.SP_FileIcon)
        icon_usuario = estilo.standardIcon(QStyle.SP_DirIcon)
        icon_reporte = estilo.standardIcon(QStyle.SP_FileDialogDetailedView)
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
                spacing: 6px;
            }
            QToolButton {
                border: 1px solid #a0a0a0;
                border-radius: 4px;
                background-color: #ffffff;
                padding: 6px 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
                border-color: #707070;
            }
            QToolButton:pressed {
                background-color: #d0d0d0;
            }
        """)

        # Acciones para la barra superior (Menú superior limpio)
        action_inicio = QAction(icon_inicio, "Inicio", self)
        action_registrar = QAction(icon_registrar, "Registrar venta", self)
        action_producto = QAction(icon_producto, "Registrar producto", self)
        action_reporte = QAction(icon_reporte, "Reporte de ventas", self)
        action_salir = QAction(icon_salir, "Salir", self)

        # Conectar acciones de la barra superior
        action_inicio.triggered.connect(self.ir_inicio)
        action_registrar.triggered.connect(self.abrir_registrar_venta)
        action_producto.triggered.connect(self.abrir_registrar_producto)
        action_reporte.triggered.connect(self.abrir_reporte_ventas)
        action_salir.triggered.connect(self.close)

        # Agregar a la barra superior
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

        # Creación de los Botones Grandes del Panel Central
        btn_registrar = self.crear_boton_grande("Registrar Venta", icon_registrar)
        btn_producto = self.crear_boton_grande("Registrar Producto", icon_producto)
        btn_usuario = self.crear_boton_grande("Registrar Usuario", icon_usuario)
        btn_reporte = self.crear_boton_grande("Reporte de Ventas", icon_reporte)
        btn_buscar = self.crear_boton_grande("Búsqueda de Venta", icon_buscar)
        btn_salir = self.crear_boton_grande("Salir", icon_salir)

        # Conectar botones centrales a sus respectivos submódulos
        btn_registrar.clicked.connect(self.abrir_registrar_venta)
        btn_producto.clicked.connect(self.abrir_registrar_producto)
        btn_usuario.clicked.connect(self.abrir_registrar_usuario)
        btn_reporte.clicked.connect(self.abrir_reporte_ventas)
        btn_buscar.clicked.connect(self.abrir_busqueda_venta)
        btn_salir.clicked.connect(self.close)

        # Organizar botones en la cuadrícula (3 filas x 2 columnas)
        grid_botones.addWidget(btn_registrar, 0, 0)
        grid_botones.addWidget(btn_producto, 0, 1)
        grid_botones.addWidget(btn_usuario, 1, 0)
        grid_botones.addWidget(btn_reporte, 1, 1)
        grid_botones.addWidget(btn_buscar, 2, 0)
        grid_botones.addWidget(btn_salir, 2, 1)

        layout_principal.addLayout(grid_botones)

    def crear_boton_grande(self, texto, icono):
        """Función auxiliar para dar estilo y tamaño uniforme a los botones del panel."""
        btn = QPushButton(texto)
        btn.setIcon(icono)
        btn.setIconSize(QSize(35, 35))
        btn.setMinimumSize(180, 75)
        btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
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

    # -------------------------------------------------------------
    # Métodos que abren cada uno de los módulos desarrollados
    # -------------------------------------------------------------
    def ir_inicio(self):
        QMessageBox.information(self, "Inicio", "Te encuentras en la pantalla principal del sistema.")

    def abrir_registrar_venta(self):
        dialogo = FormularioVenta(id_usuario_actual=self.id_usuario_actual)
        dialogo.exec()

    def abrir_registrar_producto(self):
        dialogo = FormularioProducto(id_producto=None)
        dialogo.exec()

    def abrir_registrar_usuario(self):
        dialogo = FormularioUsuario(id_usuario=None)
        dialogo.exec()

    def abrir_reporte_ventas(self):
        dialogo = FormularioReporteVentas()
        dialogo.exec()

    def abrir_busqueda_venta(self):
        dialogo = FormularioBusquedaVenta()
        dialogo.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. Validar inicio de sesión antes de desplegar la ventana principal
    login = VentanaLogin()
    if login.exec() == QDialog.Accepted and login.usuario_valido:
        # Nota: Si el login devuelve el ID del usuario, podrías pasarlo aquí. Por defecto usa 1.
        ventana = VentanaPrincipal(id_usuario_actual=1)
        ventana.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)