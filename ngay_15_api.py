import sqlite3
import bcrypt
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
class TaiKhoanMoi(BaseModel):
    tai_khoan:str
    mat_khau:str

def bam_mat_khau(mat_khau_goc:str)->str:
    muoi=bcrypt.gensalt()
    return bcrypt.hashpw(mat_khau_goc.encode('utf-8'),muoi).decode('utf-8')

@app.post("/dang-ky")
def api_dang_ky(user: TaiKhoanMoi):
    try:
        mat_khau_ma_hoa=bam_mat_khau(user.mat_khau)
        ket_noi=sqlite3.connect("kho_hang.db")
        con_tro=ket_noi.cursor()
        con_tro.execute(
            "INSERT INTO nguoi_dung(tai_khoan ,mat_khau_ma_hoa) VALUES (?,?)",
            (user.tai_khoan,mat_khau_ma_hoa)
        )
        ket_noi.commit()
        ket_noi.close()
        return {"status":"Thành công","message":f"Tài khoản '{user.tai_khoan}' đã được tạo an toàn!"}
    except sqlite3.IntegrityError:
        return {"status":"Thất bại","message":f"Tài khoản này đã tồn tại trên hệ thống!"}
    
if __name__=="__main__":
        import uvicorn
        uvicorn.run(app,host="0.0.0.0",port=9000)
