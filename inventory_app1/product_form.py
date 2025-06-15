from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QDoubleSpinBox, QMessageBox
)
from db import create_connection

class ProductForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")

        # Form Fields
        self.sku_input = QLineEdit()
        self.barcode_input = QLineEdit()
        self.category_input = QLineEdit()
        self.subcategory_input = QLineEdit()
        self.name_input = QLineEdit()
        self.description_input = QTextEdit()
        self.tax_input = QDoubleSpinBox()
        self.tax_input.setSuffix(" %")
        self.tax_input.setRange(0, 100)

        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix("₹ ")
        self.price_input.setRange(0, 100000)

        self.unit_input = QLineEdit()

        self.save_button = QPushButton("Save Product")
        self.save_button.clicked.connect(self.save_product)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("SKU ID:"))
        layout.addWidget(self.sku_input)
        layout.addWidget(QLabel("Barcode:"))
        layout.addWidget(self.barcode_input)
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_input)
        layout.addWidget(QLabel("Subcategory:"))
        layout.addWidget(self.subcategory_input)
        layout.addWidget(QLabel("Product Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Tax (%):"))
        layout.addWidget(self.tax_input)
        layout.addWidget(QLabel("Price (INR):"))
        layout.addWidget(self.price_input)
        layout.addWidget(QLabel("Default Unit:"))
        layout.addWidget(self.unit_input)

        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_product(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO product_master
                (sku_id, barcode, category, subcategory, name, description, tax, price, default_unit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                int(self.sku_input.text()),
                self.barcode_input.text(),
                self.category_input.text(),
                self.subcategory_input.text(),
                self.name_input.text(),
                self.description_input.toPlainText(),
                float(self.tax_input.value()),
                float(self.price_input.value()),
                self.unit_input.text()
            )

            cursor.execute(query, values)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Product saved successfully!")

            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_fields(self):
        self.sku_input.clear()
        self.barcode_input.clear()
        self.category_input.clear()
        self.subcategory_input.clear()
        self.name_input.clear()
        self.description_input.clear()
        self.tax_input.setValue(0.0)
        self.price_input.setValue(0.0)
        self.unit_input.clear()
