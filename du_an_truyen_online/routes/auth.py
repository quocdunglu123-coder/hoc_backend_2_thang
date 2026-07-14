import sqlite3
import bcrypt
import jwt
from fastapi import APIRouter ,Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel
from database.db_comic import lay_ket_noi

auth_route=APIRouter(tags=["Xác thực người dùng"])
SECRET_KEY="chia_khoa_bi_mat_ma_hoa_truyen_tranh"
security=HTTPBearer()

class TaiKhoanForm(BaseModel):
    tai_khoan:str
    mat_khau:str
    vai_tro:str = "user"

def bam_mat_khau(mat_khau_goc:str)->str:
    muoi=bcrypt.gensalt()
    return bcrypt.hashpw(mat_khau_goc.encode('utf-8'),muoi).decode('utf-8')

def kiem_tra_mat_khau(mat_khau_goc:str,mat_khau_ma_hoa:str)->bool:
    return bcrypt.checkpw(mat_khau_goc.encode('utf-8'),mat_khau_ma_hoa.encode('utf-8'))

def xac_thuc_nguoi_dung(credentials:HTTPAuthorizationCredentials=Depends(security)):
    token=credentials.credentials
    try:
        du_lieu_the=jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        return du_lieu_the
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mã token không hợp lệ hoặc đã hết hạn!"
        )
    
@auth_route.post("/dang-ky")
def api_dang_ky(user:TaiKhoanForm):
    try:
        mat_khau_ma_hoa=bam_mat_khau(user.mat_khau)
        ket_noi=lay_ket_noi()
        con_tro=ket_noi.cursor()
        con_tro.execute(
            "INSERT INTO nguoi_dung(tai_khoan,mat_khau_ma_hoa,vai_tro) VALUES(?,?,?)",
            (user.tai_khoan,mat_khau_ma_hoa,user.vai_tro)
        )
        ket_noi.commit()
        ket_noi.close()
        return {"status":"Thành công","message":f"Tài khoản '{user.tai_khoan}' với vai trò '{user.vai_tro}' đã được tạo!"}
    except sqlite3.IntegrityError:
        return {"status":"Thất bại","message":"Tài khoản này đã tồn tại!"}

@auth_route.post("/dang-nhap")
def api_dang_nhap(user:TaiKhoanForm):
    tk=user.tai_khoan
    mk=user.mat_khau
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT mat_khau_ma_hoa,vai_tro FROM nguoi_dung WHERE tai_khoan=?",(tk,))
    dong_du_lieu=con_tro.fetchone()
    ket_noi.close()

    if dong_du_lieu is None:
        return{"status":"Thất bại","message":"Tài khoản hoặc mật khẩu không chính xác!"}
    
    mat_khau_ma_hoa_db=dong_du_lieu["mat_khau_ma_hoa"]
    vai_tro_db=dong_du_lieu["vai_tro"]

    if kiem_tra_mat_khau(mk,mat_khau_ma_hoa_db):
        ma_token=jwt.encode({"sub":tk,"role":vai_tro_db},SECRET_KEY,algorithm="HS256")
        return{
            "status":"Thành công",
            "access_token":ma_token,
            "token_type":"bearer"
        }
    else:
        return{"status":"Thất bại","message":"Tài khoản hoặc mật khẩu không chính xác!"}
    