from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox
)
from db import create_connection

class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Entry Form")

        self.product_dropdown = QComboBox()
        self.load_products()

        self.customer_input = QLineEdit()

        self.qty_input = QSpinBox()
        self.qty_input.setRange(1, 10000)

        self.unit_input = QComboBox()
        self.unit_input.addItems(["kg", "litre", "piece", "pack", "box", "unit"])

        self.rate_input = QDoubleSpinBox()
        self.rate_input.setRange(0.0, 100000.0)
        self.rate_input.setPrefix("₹ ")

        self.total_input = QLineEdit()
        self.total_input.setReadOnly(True)

        self.tax_input = QDoubleSpinBox()
        self.tax_input.setSuffix(" %")
        self.tax_input.setRange(0.0, 100.0)

        self.save_button = QPushButton("Save Sale")
        self.save_button.clicked.connect(self.save_sale)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Product:"))
        layout.addWidget(self.product_dropdown)

        layout.addWidget(QLabel("Customer Name:"))
        layout.addWidget(self.customer_input)

        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(self.qty_input)

        layout.addWidget(QLabel("Unit:"))
        layout.addWidget(self.unit_input)

        layout.addWidget(QLabel("Rate per Unit:"))
        layout.addWidget(self.rate_input)

        layout.addWidget(QLabel("Total Rate:"))
        layout.addWidget(self.total_input)

        layout.addWidget(QLabel("Tax (%):"))
        layout.addWidget(self.tax_input)

        layout.addWidget(self.save_button)
        self.setLayout(layout)

        self.qty_input.valueChanged.connect(self.calculate_total)
        self.rate_input.valueChanged.connect(self.calculate_total)

    def load_products(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT sku_id, name FROM product_master")
            results = cursor.fetchall()
            self.products = {f"{name} (SKU {sku})": sku for sku, name in results}
            self.product_dropdown.addItems(self.products.keys())
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error loading products", str(e))

    def calculate_total(self):
        qty = self.qty_input.value()
        rate = self.rate_input.value()
        total = qty * rate
        self.total_input.setText(f"{total:.2f}")

    def save_sale(self):
        try:
            product_id = self.products[self.product_dropdown.currentText()]
            customer = self.customer_input.text()
            quantity = self.qty_input.value()
            unit = self.unit_input.currentText()
            rate = self.rate_input.value()
            total = quantity * rate
            tax = self.tax_input.value()

            conn = create_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO sales (product_id, customer_name, quantity, unit, rate_per_unit, total_rate, tax)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (product_id, customer, quantity, unit, rate, total, tax))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Sales entry saved.")
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Error saving sale", str(e))

    def clear_form(self):
        self.customer_input.clear()
        self.qty_input.setValue(1)
        self.unit_input.setCurrentIndex(0)
        self.rate_input.setValue(0.0)
        self.tax_input.setValue(0.0)
        self.total_input.clear()
