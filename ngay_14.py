import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
class Sanphammoi(BaseModel):
    ten_sp:str
    gia:float

@app.post("/them_hang")
def api_them_hang(du_lieu:Sanphammoi):
    ket_noi=sqlite3.connect("kho_hang.db")
    con_tro=ket_noi.cursor()
    con_tro.execute(
        "INSERT INTO san_pham(ten_sp ,gia) VALUES (?,?)",
        (du_lieu.ten_sp,du_lieu.gia),
    )
    ket_noi.commit()
    ket_noi.close()
    return{
        "status":"Thành công",
        "message":f"Đã lưu vĩnh viễn sản phẩm '{du_lieu.ten_sp}' vào Database!"
    }
@app.get("/xem-kho")
def api_xem_kho():
    ket_noi=sqlite3.connect("kho_hang.db")
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT * FROM san_pham")
    tat_ca_hang=con_tro.fetchall()
    ket_noi.close()
    danh_sach_sp=[]
    for hang in tat_ca_hang:
        danh_sach_sp.append({
            "id":hang[0],
            "ten_sp":hang[1],
            "gia":hang[2]
        })
    return danh_sach_sp

import sqlite3
ket_noi=sqlite3.connect("kho_hang.db")
con_tro=ket_noi.cursor()
con_tro.execute("DELETE FROM san_pham WHERE ten_sp='string'")
ket_noi.commit()
ket_noi.close()
print("Đã dọn dẹp sạch sẽ kho hàng!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=9000)