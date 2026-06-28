import sqlite3
ket_noi=sqlite3.connect("kho_hang.db")
con_tro=ket_noi.cursor()
con_tro.execute("INSERT INTO san_pham(ten_sp,gia) VALUES('Chuột máy tính',500)")
ket_noi.commit()
con_tro.execute("SELECT * FROM san_pham")
tat_ca_hang=con_tro.fetchall()
for hang in tat_ca_hang:
    print("Món hàng trong database",hang)
ket_noi.close()