import sqlite3
def lay_ket_noi():
    ket_noi=sqlite3.connect("kho_hang_mvc.db")
    ket_noi.row_factory=sqlite3.Row
    return ket_noi

def khoi_tao_bang():
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute("""
        CREATE TABLE IF NOT EXISTS san_pham(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten_sp TEXT,
        gia REAL
    )
    """)
    ket_noi.commit()
    ket_noi.close()
    