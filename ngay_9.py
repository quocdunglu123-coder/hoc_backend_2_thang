import sqlite3
ket_noi=sqlite3.connect("kho_hang.db")
con_tro=ket_noi.cursor()
con_tro.execute("""
CREATE TABLE IF NOT EXISTS san_pham (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten_sp TEXT,
    gia REAL
)
""")

ket_noi.commit()
ket_noi.close()

print("Đã tạo database kho_hang.db và bảng san_pham thành công!")


