import sqlite3
import bcrypt
import jwt
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
SECRET_KEY = "bi mat sieu cap cua dung_coder"

class TaiKhoan(BaseModel):
    tai_khoan:str
    mat_khau:str

def kiem_tra_mat_khau(mat_khau_goc:str ,mat_khau_ma_hoa:str)->bool:
    return bcrypt.checkpw(mat_khau_goc.encode('utf-8'),mat_khau_ma_hoa.encode('utf-8'))

@app.post("/dang-nhap")
def api_dang_nhap(user:TaiKhoan):
    ket_noi=sqlite3.connect("kho_hang.db")
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT mat_khau_ma_hoa FROM nguoi_dung WHERE tai_khoan=?",(user.tai_khoan,))
    dong_du_lieu=con_tro.fetchone()
    ket_noi.close()

    if dong_du_lieu is None:
        return{"status":"Thất bại","message":"Tài khoản hoặc mật khẩu không chính xác!"}
    mat_khau_ma_hoa_db=dong_du_lieu[0]
    if kiem_tra_mat_khau(user.mat_khau , mat_khau_ma_hoa_db):
        du_lieu_the={"sub":user.tai_khoan}
        ma_token=jwt.encode(du_lieu_the,SECRET_KEY,algorithm="HS256")

        return{
        "Status":"Thành công",
        "message":"Đăng nhập thành công!",
        "access_token":ma_token,
        "token_type":"bearer"
    }
    else:
        return{"Status":"Thất bại","message":"Tài khoản hoặc mật khẩu không chính xác!"}

import uvicorn
if __name__=="__main__":
    uvicorn.run(app,host="0.0.0.0",port=9000)