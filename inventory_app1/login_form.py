from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from db import create_connection


class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 User Login")
        self.setFixedSize(350, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Title
        title = QLabel("Welcome to Inventory App")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Username Field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Username")
        self.username_input.setFont(QFont("Segoe UI", 11))
        self.username_input.setStyleSheet("padding: 8px; border-radius: 6px;")

        # Password Field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔒 Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 11))
        self.password_input.setStyleSheet("padding: 8px; border-radius: 6px;")

        # Login Button
        self.login_button = QPushButton("🔓 Login")
        self.login_button.setFont(QFont("Segoe UI", 12))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.check_login)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()

        conn.close()

        if result:
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
