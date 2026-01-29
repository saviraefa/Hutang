import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QFormLayout, QLineEdit, QPushButton, QDialog
from ui_components import LoginDialog, MainWindow, TambahDialog
from database import init_db, tambah_data, ambil_data, hapus_data, hitung_total_kolom, bayar_hutang

class AppController:
    def __init__(self):
        init_db()
        self.login_dialog = LoginDialog()
        self.main_window = MainWindow()
        
        # 1. Menghubungkan tombol ke fungsi (PASTIKAN NAMA FUNGSI SAMA)
        self.main_window.btn_tambah.clicked.connect(self.buka_tambah_dialog)
        self.main_window.btn_hapus.clicked.connect(self.proses_hapus_data)
        self.main_window.btn_bayar.clicked.connect(self.buka_bayar_dialog)

    def jalankan(self):
        if self.login_dialog.exec():
            self.load_tabel_data()
            self.main_window.show()
            return True
        return False

    # 2. Fungsi Tambah Data (Yang tadi dianggap hilang oleh Python)
    def buka_tambah_dialog(self):
        dialog = TambahDialog()
        if dialog.exec():
            nama = dialog.nama_input.text()
            try:
                jumlah = float(dialog.jumlah_input.text())
                tanggal = dialog.tgl_input.date().toString("yyyy-MM-dd")
                kategori = dialog.kat_input.currentText()
                
                tambah_data(nama, jumlah, tanggal, kategori)
                self.load_tabel_data()
            except ValueError:
                QMessageBox.warning(None, "Error", "Nominal harus angka!")

    # 3. Fungsi Bayar Cicilan
    def buka_bayar_dialog(self):
        current_row = self.main_window.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(None, "Peringatan", "Pilih baris yang ingin dibayar!")
            return
        
        nama = self.main_window.table.item(current_row, 0).text()
        dialog = BayarDialog(nama)
        if dialog.exec():
            try:
                nominal = float(dialog.input_bayar.text())
                bayar_hutang (nama, nominal) # Memanggil fungsi di database.py
                self.load_tabel_data()
                QMessageBox.information(None, "Sukses", f"Berhasil membayar cicilan untuk {nama}")
            except ValueError:
                QMessageBox.warning(None, "Error", "Masukkan nominal yang benar!")

    def proses_hapus_data(self):
        current_row = self.main_window.table.currentRow()
        if current_row >= 0:
            nama = self.main_window.table.item(current_row, 0).text()
            hapus_data(nama)
            self.load_tabel_data()

    def load_tabel_data(self):
        data = ambil_data()
        self.main_window.table.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.main_window.table.insertRow(row_number)
            
            # Perhitungan Sisa untuk ditampilkan di kolom ke-4 (index 3)
            total = float(row_data[1])
            bayar = float(row_data[2])
            sisa = total - bayar
            
            self.main_window.table.setItem(row_number, 0, QTableWidgetItem(str(row_data[0])))
            self.main_window.table.setItem(row_number, 1, QTableWidgetItem(f"Rp {total:,.0f}"))
            self.main_window.table.setItem(row_number, 2, QTableWidgetItem(f"Rp {bayar:,.0f}"))
            self.main_window.table.setItem(row_number, 3, QTableWidgetItem(f"Rp {sisa:,.0f}")) # Kolom Sisa
            self.main_window.table.setItem(row_number, 4, QTableWidgetItem(str(row_data[3])))
            self.main_window.table.setItem(row_number, 5, QTableWidgetItem(str(row_data[4])))
            self.main_window.table.setItem(row_number, 6, QTableWidgetItem(str(row_data[5])))

        # Update Ringkasan Bawah
        th = hitung_total_kolom("jumlah")
        td = hitung_total_kolom("dibayar")
        self.main_window.label_ringkasan.setText(f"Total Hutang: Rp {th:,.0f} | Dibayar: Rp {td:,.0f} | Sisa: Rp {th-td:,.0f}")
        
class BayarDialog(QDialog):
    def __init__(self, nama):
        super().__init__()
        self.setWindowTitle(f"Bayar Hutang - {nama}")
        layout = QFormLayout(self)
        self.input_bayar = QLineEdit()
        self.btn_konfirmasi = QPushButton("Konfirmasi Bayar")
        self.btn_konfirmasi.clicked.connect(self.accept)
        layout.addRow("Jumlah Bayar:", self.input_bayar)
        layout.addWidget(self.btn_konfirmasi)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = AppController()
    if controller.jalankan():
        sys.exit(app.exec())