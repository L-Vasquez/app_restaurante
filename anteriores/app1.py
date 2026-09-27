import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QPushButton, QStyle, QMessageBox, QToolBar
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize, Qt

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Ventas")
        self.resize(700, 500)

        # -------------------------------------------------------------
        # Obtener íconos clásicos del sistema
        # -------------------------------------------------------------
        estilo = QApplication.style()
        
        icon_registrar = estilo.standardIcon(QStyle.SP_FileDialogNewFolder)
        icon_reporte = estilo.standardIcon(QStyle.SP_FileDialogDetailedView)
        icon_buscar = estilo.standardIcon(QStyle.SP_FileDialogContentsView)
        icon_salir = estilo.standardIcon(QStyle.SP_DialogCloseButton)

        # -------------------------------------------------------------
        # Menú Superior Horizontal (QToolBar)
        # -------------------------------------------------------------
        barra_herramientas = QToolBar("Menú Principal")
        barra_herramientas.setMovable(False)  # Fijar la barra para que no se arrastre
        barra_herramientas.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon) # Texto al lado del ícono
        barra_herramientas.setIconSize(QSize(20, 20))
        
        # Añadir la barra en la parte superior
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, barra_herramientas)

        # Estilo CSS para marcar claramente los BORDES de las acciones/botones del menú superior
        barra_herramientas.setStyleSheet("""
            QToolBar {
                background-color: #f0f0f0;
                padding: 5px;
                border-bottom: 1px solid #cccccc;
                spacing: 8px; /* Espacio entre botones */
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

        # Crear las acciones para el menú superior
        action_registrar = QAction(icon_registrar, "Registrar venta", self)
        action_reporte = QAction(icon_reporte, "Reporte de ventas", self)
        action_buscar = QAction(icon_buscar, "Búsqueda de venta", self)
        action_salir = QAction(icon_salir, "Salir", self)

        # Conectar acciones a sus funciones
        action_registrar.triggered.connect(self.registrar_venta)
        action_reporte.triggered.connect(self.reporte_ventas)
        action_buscar.triggered.connect(self.buscar_venta)
        action_salir.triggered.connect(self.close)

        # Agregar acciones directamente a la barra horizontal
        barra_herramientas.addAction(action_registrar)
        barra_herramientas.addAction(action_reporte)
        barra_herramientas.addAction(action_buscar)
        barra_herramientas.addAction(action_salir)

        # -------------------------------------------------------------
        # Contenedor y Layout principal del cuerpo
        # -------------------------------------------------------------
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)
        layout_principal.setContentsMargins(20, 20, 20, 20)

        # Layout en cuadrícula para los botones grandes
        grid_botones = QGridLayout()
        grid_botones.setSpacing(20)

        # Crear los Botones Grandes del centro
        btn_registrar = self.crear_boton_grande("Registrar Venta", icon_registrar)
        btn_reporte = self.crear_boton_grande("Reporte de Ventas", icon_reporte)
        btn_buscar = self.crear_boton_grande("Búsqueda de Venta", icon_buscar)
        btn_salir = self.crear_boton_grande("Salir", icon_salir)

        # Conectar botones a sus funciones
        btn_registrar.clicked.connect(self.registrar_venta)
        btn_reporte.clicked.connect(self.reporte_ventas)
        btn_buscar.clicked.connect(self.buscar_venta)
        btn_salir.clicked.connect(self.close)

        # Organizar botones en la cuadrícula (2x2)
        grid_botones.addWidget(btn_registrar, 0, 0)
        grid_botones.addWidget(btn_reporte, 0, 1)
        grid_botones.addWidget(btn_buscar, 1, 0)
        grid_botones.addWidget(btn_salir, 1, 1)

        layout_principal.addLayout(grid_botones)

    def crear_boton_grande(self, texto, icono):
        """Función auxiliar para dar estilo y tamaño uniforme a los botones grandes."""
        btn = QPushButton(texto)
        btn.setIcon(icono)
        btn.setIconSize(QSize(40, 40))  # Ícono grande
        btn.setMinimumSize(200, 100)    # Tamaño mínimo del botón
        btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
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
    # Métodos / Funciones de los botones
    # -------------------------------------------------------------
    def registrar_venta(self):
        QMessageBox.information(self, "Opción Seleccionada", "Has seleccionado: Registrar venta")

    def reporte_ventas(self):
        QMessageBox.information(self, "Opción Seleccionada", "Has seleccionado: Reporte de ventas")

    def buscar_venta(self):
        QMessageBox.information(self, "Opción Seleccionada", "Has seleccionado: Búsqueda de venta")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())