import sys
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QMessageBox, QHeaderView, 
    QLabel, QDateEdit
)
from PySide6.QtCore import QDate, Qt
from conexion import ejecutar_consulta

class FormularioReporteVentas(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reporte de Ventas por Fecha")
        self.resize(800, 500)
        self.setModal(True)

        layout_principal = QVBoxLayout(self)

        # 1. Filtros por Fecha
        layout_filtros = QHBoxLayout()
        
        self.date_inicio = QDateEdit()
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.setDate(QDate.currentDate().addDays(-30))  # Por defecto hace 30 días

        self.date_fin = QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QDate.currentDate())  # Fecha actual

        btn_filtrar = QPushButton("Filtrar Reporte")
        btn_filtrar.setStyleSheet("background-color: #0056b3; color: white; font-weight: bold; padding: 6px 12px;")
        btn_filtrar.clicked.connect(self.cargar_reporte)

        layout_filtros.addWidget(QLabel("Desde:"))
        layout_filtros.addWidget(self.date_inicio)
        layout_filtros.addWidget(QLabel("Hasta:"))
        layout_filtros.addWidget(self.date_fin)
        layout_filtros.addWidget(btn_filtrar)
        layout_filtros.addStretch()
        
        layout_principal.addLayout(layout_filtros)

        # 2. Tabla de Resultados de Ventas
        self.tabla_reporte = QTableWidget()
        self.tabla_reporte.setColumnCount(6)
        self.tabla_reporte.setHorizontalHeaderLabels(["ID Venta", "Fecha y Hora", "Mesa", "Atendido por", "Estado", "Total (S/.)"])
        self.tabla_reporte.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_reporte.setEditTriggers(QTableWidget.NoEditTriggers)
        layout_principal.addWidget(self.tabla_reporte)

        # 3. Cuadro Resumen Final con el Total Sencillo
        layout_inferior = QHBoxLayout()
        self.lbl_total_recaudado = QLabel("Total General Vendido: S/. 0.00")
        self.lbl_total_recaudado.setStyleSheet("font-size: 16px; font-weight: bold; color: #28a745;")

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)

        layout_inferior.addWidget(self.lbl_total_recaudado)
        layout_inferior.addStretch()
        layout_inferior.addWidget(btn_cerrar)
        layout_principal.addLayout(layout_inferior)

        # Cargar datos iniciales al abrir
        self.cargar_reporte()

    def cargar_reporte(self):
        """Consulta las ventas filtradas por rango de fechas y calcula el total."""
        # Obtenemos las fechas de los widgets en formato string YYYY-MM-DD
        f_inicio = self.date_inicio.date().toString("yyyy-MM-dd") + " 00:00:00"
        f_fin = self.date_fin.date().toString("yyyy-MM-dd") + " 23:59:59"

        # Consulta SQL filtrando por fecha (excluyendo ventas anuladas para el cálculo financiero si se prefiere, o sumando todas)
        query = """
            SELECT v.id_venta, v.fecha, m.numero, u.nombre, v.estado, v.total
            FROM ventas v
            LEFT JOIN mesas m ON v.id_mesa = m.id_mesa
            LEFT JOIN usuarios u ON v.id_usuario = u.id_usuario
            WHERE v.fecha BETWEEN ? AND ?
            ORDER BY v.fecha DESC
        """
        
        ventas = ejecutar_consulta(query, (f_inicio, f_fin), es_lectura=True)
        
        self.tabla_reporte.setRowCount(0)
        total_ingresos = 0.0

        if ventas:
            self.tabla_reporte.setRowCount(len(ventas))
            for row, v in enumerate(ventas):
                id_venta, fecha, mesa, usuario, estado, total = v
                
                self.tabla_reporte.setItem(row, 0, QTableWidgetItem(str(id_venta)))
                self.tabla_reporte.setItem(row, 1, QTableWidgetItem(str(fecha)))
                self.tabla_reporte.setItem(row, 2, QTableWidgetItem(f"Mesa N° {mesa}" if mesa else "N/A"))
                self.tabla_reporte.setItem(row, 3, QTableWidgetItem(str(usuario)))
                
                item_estado = QTableWidgetItem(str(estado))
                if estado == 'Anulada':
                    item_estado.setForeground(Qt.red)
                self.tabla_reporte.setItem(row, 4, item_estado)
                
                self.tabla_reporte.setItem(row, 5, QTableWidgetItem(f"S/. {total:.2f}"))

                # Sumar al total únicamente si la venta está completada (no sumamos las anuladas)
                if estado != 'Anulada':
                    total_ingresos += float(total)

        # Actualizar el texto del cuadro resumen inferior
        self.lbl_total_recaudado.setText(f"Total General Vendido: S/. {total_ingresos:.2f}")