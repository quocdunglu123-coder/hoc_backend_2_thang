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
        vai_tro TEXT DEFAULT 'user'
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

    con_tro.execute("""
    CREATE TABLE IF NOT EXISTS lich_su_doc(
        id INTEGER PRIMARY KEY AUTOINCREMENT,       
        nguoi_dung_id INTEGER,
        truyen_id INTEGER,
        ngay_doc TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (nguoi_dung_id) REFERENCES nguoi_dung(id),
        FOREIGN KEY (truyen_id) REFERENCES truyen(id)
    )
    """)

    con_tro.execute("""
    CREATE TABLE IF NOT EXISTS danh_gia(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nguoi_dung_id INTEGER,
        truyen_id INTEGER,
        so_sao INTEGER CHECK (so_sao >= 1 AND so_sao <= 5),
        binh_luan TEXT,
        FOREIGN KEY (nguoi_dung_id) REFERENCES nguoi_dung(id),
        FOREIGN KEY (truyen_id) REFERENCES truyen(id)
    )
    """)

    con_tro.execute("""
    CREATE INDEX IF NOT EXISTS idx_ten_truyen
    ON truyen(ten_truyen)
    """)

    ket_noi.commit()
    ket_noi.close()
