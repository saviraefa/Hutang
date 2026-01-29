from PyQt6.QtWidgets import (QMainWindow, QTableWidget, QVBoxLayout, QWidget, 
                             QLineEdit, QPushButton, QLabel, QDialog, 
                             QFormLayout, QDateEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Sistem")
        self.setFixedSize(700, 700)
        main_layout = QVBoxLayout(self)
        self.logo_label = QLabel()
        pixmap = QPixmap("logo.png") # Ganti dengan nama file logomu
        # Atur ukuran logo agar pas (misal lebar 100px)
        self.logo_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.logo_label)
        form_widget = QWidget()
        layout = QFormLayout(form_widget)
        self.user_input = QLineEdit()
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.verifikasi_login)
        
        layout.addRow("Username:", self.user_input)
        layout.addRow("Password:", self.pass_input)
        layout.addWidget(self.btn_login)
        
        main_layout.addWidget(form_widget)

    def verifikasi_login(self):
        if self.user_input.text() == "eva" and self.pass_input.text() == "123":
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Username atau Password Salah!")

class TambahDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Catatan")
        layout = QFormLayout(self)
        self.nama_input = QLineEdit()
        self.jumlah_input = QLineEdit()
        self.tgl_input = QDateEdit(calendarPopup=True)
        self.tgl_input.setDate(QDate.currentDate())
        self.kat_input = QComboBox()
        self.kat_input.addItems(["Hutang Saya", "Piutang Orang Lain"])
        self.btn_simpan = QPushButton("Simpan")
        self.btn_simpan.clicked.connect(self.accept)
        layout.addRow("Nama:", self.nama_input)
        layout.addRow("Nominal Hutang:", self.jumlah_input)
        layout.addRow("Tanggal:", self.tgl_input)
        layout.addRow("Kategori:", self.kat_input)
        layout.addWidget(self.btn_simpan)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi CatatHutang Desktop")
        self.resize(800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel("DAFTAR HUTANG & PIUTANG")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
         "Nama", "Total Hutang", "Dibayar", "Sisa Hutang", "Tanggal", "Kategori", "Status"
        ])
        self.label_ringkasan = QLabel("Total Hutang: Rp 0 | Dibayar: Rp 0 | Sisa: Rp 0")
        self.label_ringkasan.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50; padding: 10px;")

        self.btn_tambah = QPushButton("Tambah Data Baru")
        self.btn_hapus = QPushButton("Hapus Terpilih")
        
        self.btn_bayar = QPushButton("Bayar Cicilan")
        self.btn_bayar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.layout.addWidget(self.btn_bayar)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.label_ringkasan)
        self.layout.addWidget(self.btn_tambah)
        self.layout.addWidget(self.btn_hapus)