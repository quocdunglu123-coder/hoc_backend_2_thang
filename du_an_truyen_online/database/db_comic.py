import sqlite3

def lay_ket_noi():
    ket_noi=sqlite3.connect("data_truyen.db")
    ket_noi.row_factory=sqlite3.Row
    return ket_noi
def khoi_tao_he_thong():
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()

    con_tro.execute("""
        CREATE TABLE IF NOT EXISTS nguoi_dung(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tai_khoan TEXT UNIQUE,
        mat_khau_ma_hoa TEXT,
        vai_tro TEXT DEFAULT 'user'--'user' hoặc 'admin'
    )
    """) 

    con_tro.execute("""
        CREATE TABLE IF NOT EXISTS truyen(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten_truyen TEXT,
        tac_gia TEXT,
        noi_dung TEXT
    )
    """)

    ket_noi.commit()
    ket_noi.close()
