import sqlite3
import bcrypt
import jwt
from fastapi import APIRouter ,Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel
from database.db_helper import lay_ket_noi

auth_route=APIRouter(tags=["Xác thực người dùng"])
SECRET_KEY="bi mat sieu cap cua dung_coder"
sercurity=HTTPBearer()

class TaiKhoan(BaseModel):
    tai_khoan:str
    mat_khau:str

def bam_mat_khau(mat_khau_goc:str)->str:
    muoi=bcrypt.gensalt()
    return bcrypt.hashpw(mat_khau_goc.encode('utf-8'),muoi).decode('utf-8')

def kiem_tra_mat_khau(mat_khau_goc:str,mat_khau_ma_hoa:str)->bool:
    return bcrypt.checkpw(mat_khau_goc.encode('utf-8'),mat_khau_ma_hoa.encode('utf-8'))

def xac_thuc_nguoi_dung(credentials:HTTPAuthorizationCredentials=Depends(sercurity)):
    token=credentials.credentials
    try:
        du_lieu_the=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return du_lieu_the
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mã token không hợp lệ hoặc đã hết hạn"
        )
    
@auth_route.post("/dang-ky")
def api_dang_ky(user:TaiKhoan):
    try:
        mat_khau_ma_hoa=bam_mat_khau(user.mat_khau)
        ket_noi=lay_ket_noi()
        con_tro=ket_noi.cursor()
        con_tro.execute(
            "INSERT INTO nguoi_dung(tai_khoa,mat_khau_ma_hoa) VALUES (?,?)",
            (user.tai_khoan,mat_khau_ma_hoa)
        )
        ket_noi.commit()
        ket_noi.close()
        return{"status":"Thành công","message":f"Tài khoản '{user.tai_khoan}' đã được tạo!"}
    except sqlite3.IntegrityError:
        return{"status":"Thất bại","message":"Tài khoản này đã tồn tại!"}
    
@auth_route.post("/dang-nhap")
def api_dang_nhap(user:TaiKhoan):
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT mat_khau_ma_hoa FROM nguoi_dung WHERE tai_khoan=?",(user.tai_khoan,))
    dong_du_lieu=con_tro.fetchone()
    ket_noi.close()

    if dong_du_lieu is None:
        return{"status":"Thất bại","message":"Tài khoản hoặc mật khẩu không đúng"}
    if kiem_tra_mat_khau(user.mat_khau,dong_du_lieu[0]):
        ma_token=jwt.encode({"sub":user.tai_khoan},SECRET_KEY,algorithm="HS256")
        return{"status":"Thành công","access_token":ma_token,"token_type":"bearer"}
    else:
        return{"status":"Thất bại","message":"Tài khoản hoặc mật khẩu không đúng!"}
    