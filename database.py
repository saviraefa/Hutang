import sqlite3

def init_db():
    conn = sqlite3.connect("hutang_app.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS data_hutang (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama TEXT NOT NULL,
                        jumlah REAL NOT NULL,
                        dibayar REAL DEFAULT 0,
                        tanggal TEXT,
                        kategori TEXT,
                        status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def tambah_data(nama, jml, tgl, kat):
    conn = sqlite3.connect("hutang_app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data_hutang (nama, jumlah, dibayar, tanggal, kategori, status) VALUES (?,?,?,?,?,?)",
                   (nama, jml, 0, tgl, kat, "Belum Lunas"))
    conn.commit()
    conn.close()

def ambil_data():
    conn = sqlite3.connect("hutang_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nama, jumlah, dibayar, tanggal, kategori, status FROM data_hutang")
    rows = cursor.fetchall()
    conn.close()
    return rows

def hapus_data(nama):
    conn = sqlite3.connect("hutang_app.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM data_hutang WHERE nama=?", (nama,))
    conn.commit()
    conn.close()

def hitung_total_kolom(nama_kolom):
    conn = sqlite3.connect("hutang_app.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT SUM({nama_kolom}) FROM data_hutang")
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0
def bayar_hutang(nama, jumlah_bayar):
    """Menambahkan nominal ke kolom dibayar dan update status jika sudah lunas."""
    conn = sqlite3.connect("hutang_app.db")
    cursor = conn.cursor()
    
    
    # 1. Ambil data saat ini
    cursor.execute("SELECT jumlah, dibayar FROM data_hutang WHERE nama=?", (nama,))
    res = cursor.fetchone()
    if res:
        total_hutang, sudah_dibayar_lama = res
        baru_dibayar = sudah_dibayar_lama + jumlah_bayar
        
        # 2. Update nominal dibayar
        status = "Lunas" if baru_dibayar >= total_hutang else "Belum Lunas"
        cursor.execute("UPDATE data_hutang SET dibayar=?, status=? WHERE nama=?", 
                       (baru_dibayar, status, nama))
    
    conn.commit()
    conn.close()