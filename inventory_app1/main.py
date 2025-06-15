from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem,
    QSizePolicy
)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt
import sys

from product_form import ProductForm
from goods_receiving_form import GoodsReceivingForm
from sales import SalesForm
from login_form import LoginForm


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📦 Inventory Management System")
        self.setFixedSize(400, 350)  # Fixed size dashboard window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title
        title = QLabel("📊 Inventory Dashboard")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Buttons
        self.product_button = QPushButton("🧾 Product Master")
        self.goods_button = QPushButton("🚚 Goods Receiving")
        self.sales_button = QPushButton("💰 Sales Entry")

        for btn in [self.product_button, self.goods_button, self.sales_button]:
            btn.setFixedHeight(50)
            btn.setFont(QFont("Segoe UI", 12))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            layout.addWidget(btn)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

        self.product_button.clicked.connect(self.open_product_form)
        self.goods_button.clicked.connect(self.open_goods_form)
        self.sales_button.clicked.connect(self.open_sales_form)

    def open_product_form(self):
        self.pf = ProductForm()
        self.pf.show()

    def open_goods_form(self):
        self.gf = GoodsReceivingForm()
        self.gf.show()

    def open_sales_form(self):
        self.sf = SalesForm()
        self.sf.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login = LoginForm()
    if login.exec():
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
