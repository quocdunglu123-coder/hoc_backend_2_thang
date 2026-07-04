import sqlite3
import bcrypt

ket_noi=sqlite3.connect("kho_hang.db")
con_tro=ket_noi.cursor()
con_tro.execute("""
CREATE TABLE IF NOT EXISTS nguoi_dung(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tai_khoan TEXT UNIQUE,
    mat_khau_ma_hoa TEXT
)
""")
ket_noi.commit()
ket_noi.close()

def bam_mat_khau(mat_khau_goc:str) ->str:
    muoi=bcrypt.gensalt()
    mat_khau_bytes=mat_khau_goc.encode('utf-8')
    token_da_bam=bcrypt.hashpw(mat_khau_bytes,muoi)
    return token_da_bam.decode('utf-8')
mat_khau_test="123456"
ket_qua_ma_hoa=bam_mat_khau(mat_khau_test)

print("Mật khẩu gốc ban đầu :",mat_khau_test)
print("Mật khẩu sau khi dùng bcrypt gốc băm nát :",ket_qua_ma_hoa)