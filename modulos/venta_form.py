import sys
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QComboBox, QSpinBox, QPushButton, QTableWidget, 
    QTableWidgetItem, QLabel, QMessageBox, QHeaderView
)
from conexion import ejecutar_consulta

class FormularioVenta(QDialog):
    def __init__(self, id_usuario_actual=1):
        super().__init__()
        self.id_usuario = id_usuario_actual  # ID del cajero/mesero logueado
        self.setWindowTitle("Registrar Venta - Restaurante")
        self.resize(700, 500)
        self.setModal(True)

        layout_principal = QVBoxLayout(self)

        # 1. Cabecera: Selección de Mesa
        layout_superior = QHBoxLayout()
        self.combo_mesas = QComboBox()
        self.cargar_mesas()
        layout_superior.addWidget(QLabel("Seleccionar Mesa:"))
        layout_superior.addWidget(self.combo_mesas)
        layout_superior.addStretch()
        layout_principal.addLayout(layout_superior)

        # 2. Selección de Producto y Cantidad
        layout_producto = QHBoxLayout()
        self.combo_productos = QComboBox()
        self.cargar_productos()
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 100)
        self.spin_cantidad.setValue(1)

        btn_agregar = QPushButton("Agregar a la Venta")
        btn_agregar.clicked.connect(self.agregar_item)

        layout_producto.addWidget(QLabel("Producto:"))
        layout_producto.addWidget(self.combo_productos, 2)
        layout_producto.addWidget(QLabel("Cantidad:"))
        layout_producto.addWidget(self.spin_cantidad)
        layout_producto.addWidget(btn_agregar)
        layout_principal.addLayout(layout_producto)

        # 3. Tabla de Detalle de Venta
        self.tabla_detalle = QTableWidget()
        self.tabla_detalle.setColumnCount(4)
        self.tabla_detalle.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio Unitario", "Subtotal"])
        self.tabla_detalle.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout_principal.addWidget(self.tabla_detalle)

        # 4. Pie: Total y Botón Registrar Venta
        layout_inferior = QHBoxLayout()
        self.lbl_total = QLabel("Total a Pagar: S/. 0.00")
        self.lbl_total.setStyleSheet("font-size: 16px; font-weight: bold; color: #d9534f;")
        
        btn_finalizar = QPushButton("Finalizar y Cobrar Venta")
        btn_finalizar.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 10px;")
        btn_finalizar.clicked.connect(self.guardar_venta)

        layout_inferior.addWidget(self.lbl_total)
        layout_inferior.addStretch()
        layout_inferior.addWidget(btn_finalizar)
        layout_principal.addLayout(layout_inferior)

        self.lista_items = []  # Almacenará los productos añadidos temporalmente

    def cargar_mesas(self):
        """Carga las mesas disponibles en el ComboBox."""
        mesas = ejecutar_consulta("SELECT id_mesa, numero, capacidad FROM mesas", es_lectura=True)
        if mesas:
            for id_mesa, numero, capacidad in mesas:
                self.combo_mesas.addItem(f"Mesa N° {numero} (Cap: {capacidad})", id_mesa)

    def cargar_productos(self):
        """Carga los productos activos en el ComboBox."""
        productos = ejecutar_consulta("SELECT id_producto, nombre, precio FROM productos WHERE activo = 1", es_lectura=True)
        if productos:
            for id_prod, nombre, precio in productos:
                # Guardamos una tupla con (id_producto, precio) como datos internos
                self.combo_productos.addItem(f"{nombre} - S/. {precio:.2f}", (id_prod, precio))

    def agregar_item(self):
        """Agrega el producto seleccionado a la tabla temporal de la venta."""
        if self.combo_productos.count() == 0:
            QMessageBox.warning(self, "Aviso", "No hay productos disponibles.")
            return

        data_producto = self.combo_productos.currentData()
        id_producto = data_producto[0]
        precio_unitario = data_producto[1]
        nombre_producto = self.combo_productos.currentText().split(" - ")[0]
        cantidad = self.spin_cantidad.value()
        subtotal = cantidad * precio_unitario

        # Verificar si ya está en la lista para sumar cantidades o añadir nueva fila
        self.lista_items.append({
            "id_producto": id_producto,
            "nombre": nombre_producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal
        })

        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Refresca la tabla visual y calcula el total general."""
        self.tabla_detalle.setRowCount(len(self.lista_items))
        total_general = 0.0

        for row, item in enumerate(self.lista_items):
            self.tabla_detalle.setItem(row, 0, QTableWidgetItem(item["nombre"]))
            self.tabla_detalle.setItem(row, 1, QTableWidgetItem(str(item["cantidad"])))
            self.tabla_detalle.setItem(row, 2, QTableWidgetItem(f"S/. {item['precio_unitario']:.2f}"))
            self.tabla_detalle.setItem(row, 3, QTableWidgetItem(f"S/. {item['subtotal']:.2f}"))
            total_general += item["subtotal"]

        self.lbl_total.setText(f"Total a Pagar: S/. {total_general:.2f}")

    def guardar_venta(self):
        """Registra la venta y su detalle en la base de datos de manera transaccional."""
        if not self.lista_items:
            QMessageBox.warning(self, "Venta Vacía", "Debes agregar al menos un producto a la venta.")
            return

        if self.combo_mesas.count() == 0:
            QMessageBox.warning(self, "Sin Mesas", "No hay mesas disponibles para asociar la venta.")
            return

        id_mesa = self.combo_mesas.currentData()
        total_general = sum(item["subtotal"] for item in self.lista_items)

        try:
            # 1. Insertar en la tabla 'ventas' y obtener el ID generado
            query_venta = "INSERT INTO ventas (id_mesa, id_usuario, estado, total) VALUES (?, ?, 'Completada', ?)"
            id_venta = ejecutar_consulta(query_venta, (id_mesa, self.id_usuario, total_general), es_lectura=False)

            if id_venta:
                # 2. Insertar cada elemento en la tabla 'detalle_venta'
                for item in self.lista_items:
                    query_detalle = """
                        INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario, subtotal) 
                        VALUES (?, ?, ?, ?, ?)
                    """
                    ejecutar_consulta(
                        query_detalle, 
                        (id_venta, item["id_producto"], item["cantidad"], item["precio_unitario"], item["subtotal"]), 
                        es_lectura=False
                    )

                QMessageBox.information(self, "Éxito", "¡Venta registrada correctamente!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo registrar la cabecera de la venta.")
        except Exception as e:
            QMessageBox.critical(self, "Error crítico", f"Ocurrió un error al guardar la venta:\n{e}")