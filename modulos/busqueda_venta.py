import sys
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QMessageBox, QHeaderView, QLabel
)
from conexion import ejecutar_consulta
from PySide6.QtCore import Qt

class FormularioBusquedaVenta(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Búsqueda y Gestión de Ventas")
        self.resize(800, 500)
        self.setModal(True)

        layout_principal = QVBoxLayout(self)

        # Título o descripción
        layout_principal.addWidget(QLabel("Historial de Ventas Registradas (Selecciona una venta para ver detalles o anularla):"))

        # Tabla principal de ventas
        self.tabla_ventas = QTableWidget()
        self.tabla_ventas.setColumnCount(6)
        self.tabla_ventas.setHorizontalHeaderLabels(["ID Venta", "Fecha", "Mesa", "Usuario", "Estado", "Total (S/.)"])
        self.tabla_ventas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_ventas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_ventas.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_ventas.cellClicked.connect(self.cargar_detalle_venta)
        layout_principal.addWidget(self.tabla_ventas)

        # Subtítulo para el detalle
        layout_principal.addWidget(QLabel("Detalle de los productos de la venta seleccionada:"))

        # Tabla de detalle de la venta seleccionada
        self.tabla_detalle = QTableWidget()
        self.tabla_detalle.setColumnCount(4)
        self.tabla_detalle.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio Unitario", "Subtotal"])
        self.tabla_detalle.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_detalle.setEditTriggers(QTableWidget.NoEditTriggers)
        layout_principal.addWidget(self.tabla_detalle)

        # Botones inferiores (Anular venta y Cerrar)
        layout_inferior = QHBoxLayout()
        btn_anular = QPushButton("Anular Venta Seleccionada")
        btn_anular.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold; padding: 8px;")
        btn_anular.clicked.connect(self.anular_venta)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)

        layout_inferior.addWidget(btn_anular)
        layout_inferior.addStretch()
        layout_inferior.addWidget(btn_cerrar)
        layout_principal.addLayout(layout_inferior)

        # Cargar datos al iniciar
        self.cargar_ventas()

    def cargar_ventas(self):
        """Carga todas las ventas desde la base de datos uniendo con mesas y usuarios."""
        query = """
            SELECT v.id_venta, v.fecha, m.numero, u.nombre, v.estado, v.total
            FROM ventas v
            LEFT JOIN mesas m ON v.id_mesa = m.id_mesa
            LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
            ORDER BY v.id_venta DESC
        """
        ventas = ejecutar_consulta(query, es_lectura=True)
        
        if ventas:
            self.tabla_ventas.setRowCount(len(ventas))
            for row, v in enumerate(ventas):
                id_venta, fecha, mesa, usuario, estado, total = v
                self.tabla_ventas.setItem(row, 0, QTableWidgetItem(str(id_venta)))
                self.tabla_ventas.setItem(row, 1, QTableWidgetItem(str(fecha)))
                self.tabla_ventas.setItem(row, 2, QTableWidgetItem(f"Mesa N° {mesa}" if mesa else "N/A"))
                self.tabla_ventas.setItem(row, 3, QTableWidgetItem(str(usuario)))
                
                item_estado = QTableWidgetItem(str(estado))
                # Si está anulada, poner el texto en color rojo para distinguirla
                if estado == 'Anulada':
                    item_estado.setForeground(Qt.red)
                self.tabla_ventas.setItem(row, 4, item_estado)
                
                self.tabla_ventas.setItem(row, 5, QTableWidgetItem(f"S/. {total:.2f}"))

    def cargar_detalle_venta(self, row, column):
        """Carga los productos de la venta seleccionada en la tabla inferior."""
        id_venta_item = self.tabla_ventas.item(row, 0)
        if not id_venta_item:
            return

        id_venta = int(id_venta_item.text())
        query = """
            SELECT p.nombre, d.cantidad, d.precio_unitario, d.subtotal
            FROM detalle_venta d
            JOIN productos p ON d.id_producto = p.id_producto
            WHERE d.id_venta = ?
        """
        detalles = ejecutar_consulta(query, (id_venta,), es_lectura=True)

        if detalles:
            self.tabla_detalle.setRowCount(len(detalles))
            for r, d in enumerate(detalles):
                nombre, cantidad, precio, subtotal = d
                self.tabla_detalle.setItem(r, 0, QTableWidgetItem(str(nombre)))
                self.tabla_detalle.setItem(r, 1, QTableWidgetItem(str(cantidad)))
                self.tabla_detalle.setItem(r, 2, QTableWidgetItem(f"S/. {precio:.2f}"))
                self.tabla_detalle.setItem(r, 3, QTableWidgetItem(f"S/. {subtotal:.2f}"))
        else:
            self.tabla_detalle.setRowCount(0)

    def anular_venta(self):
        """Cambia el estado de la venta a 'Anulada' sin eliminar el registro físico."""
        fila_seleccionada = self.tabla_ventas.currentRow()
        if fila_seleccionada < 0:
            QMessageBox.warning(self, "Selección requerida", "Por favor, selecciona una venta de la tabla para anular.")
            return

        id_venta = int(self.tabla_ventas.item(fila_seleccionada, 0).text())
        estado_actual = self.tabla_ventas.item(fila_seleccionada, 4).text()

        if estado_actual == 'Anulada':
            QMessageBox.information(self, "Aviso", "Esta venta ya se encuentra anulada.")
            return

        confirmacion = QMessageBox.question(
            self, 
            "Confirmar Anulación", 
            f"¿Estás seguro de que deseas anular la venta N° {id_venta}?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            # Actualizamos el estado en lugar de hacer un DELETE (Preserva la base de datos intacta)
            query = "UPDATE ventas SET estado = 'Anulada' WHERE id_venta = ?"
            ejecutar_consulta(query, (id_venta,), es_lectura=False)
            
            QMessageBox.information(self, "Éxito", f"La venta N° {id_venta} ha sido anulada correctamente.")
            self.cargar_ventas()  # Refrescar la tabla
            self.tabla_detalle.setRowCount(0)  # Limpiar detalle