import sqlite3
import bcrypt
import jwt
from fastapi import FastAPI ,Depends ,HTTPException ,status
from fastapi.security import HTTPAuthorizationCredentials ,HTTPBearer
from pydantic import BaseModel

app=FastAPI()
SECRET_KEY = "bi mat sieu cap cua dung_coder"

sercurity=HTTPBearer()
class TaiKhoan(BaseModel):
    tai_khoan:str
    mat_khau:str
class SanPhamNhap(BaseModel):
    ten_sp:str
    gia:float
def bam_mat_khau(mat_khau_goc:str)->str:
    muoi=bcrypt.gensalt()
    return bcrypt.hashpw(mat_khau_goc.encode('utf-8'),muoi).decode('utf-8')
def kiem_tra_mat_khau(mat_khau_goc:str,mat_khau_ma_hoa:str)->bool:
    return bcrypt.checkpw(mat_khau_goc.encode('utf-8'),mat_khau_ma_hoa.encode('utf-8'))

def xac_thuc_nguoi_dung(Credentials:HTTPAuthorizationCredentials=Depends(sercurity)):
    token=Credentials.credentials
    try:
        du_lieu_the=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return du_lieu_the
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mã token của bạn không hợp lệ hoặc đã hết hạn!"
        )
def khoi_tao_database():
    ket_noi=sqlite3.connect("kho_hang.db")
    con_tro=ket_noi.cursor()
    con_tro.execute("""
    CREATE TABLE IF NOT EXISTS nguoi_dung(
        id INTEGET PRIMARY KEY AUTOINCREMENT,
        tai_khoa TEXT UNIQUE,
        mat_khau_ma_hoa TEXT
    )
    """)
    con_tro.execute("""
    CREATE TABLE IF NOT EXISTS san_pham (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten_sp TEXT,
        gia REAL
    )
    """)
    ket_noi.commit()
    ket_noi.close()
khoi_tao_database()
@app.post("/dang-ky")
def api_dang_ky(user:TaiKhoan):
    try:
        mat_khau_ma_hoa=bam_mat_khau(user.mat_khau)
        ket_noi=sqlite3.connect("kho_hang.db")
        con_tro=ket_noi.cursor()
        con_tro.execute(
            "INSERT INTO nguoi_dung (tai_khoan,mat_khau_ma_hoa) VALUES (?,?)",
            (user.tai_khoan,mat_khau_ma_hoa)
        )
        ket_noi.commit()
        ket_noi.close()
        return {"status":"Thành công","message":f"Tài khoản '{user.tai_khoan}' đã được tạo!"}
    except sqlite3.IntegrityError:
        return {"status":"Thất bại","message":"Tài khoản này đã được tồn tại!"}
@app.post("/dang-nhap")
def api_dang_nhap(user:TaiKhoan):
    ket_noi=sqlite3.connect("kho_hang.db")
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT mat_khau_ma_hoa FROM nguoi_dung WHERE tai_khoan=?",(user.tai_khoan,))
    dong_du_lieu=con_tro.fetchone()
    ket_noi.close()
    if dong_du_lieu is None:
        return {"status":"Thất bại","message":"Tài khoản hoặc mật khẩu không đúng!"}
    mat_khau_ma_hoa_db =dong_du_lieu[0]
    if kiem_tra_mat_khau(user.mat_khau,mat_khau_ma_hoa_db):
        ma_token=jwt.encode({"sub":user.tai_khoan},SECRET_KEY,algorithm="HS256")
        return {"status":"Thành công","access_token":ma_token,"token_type":"bearer"}
    else:
        return {"status":"Thất bại","message":"Tài khoản hoặc mật khẩu không đúng!"}
    
@app.get("/xem_kho_bao_mat")
def api_xem_kho_bao_mat(nguoi_dung=Depends(xac_thuc_nguoi_dung)):
    ket_noi=sqlite3.connect("kho_hang.db")
    ket_noi.row_factory=sqlite3.Row
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT * FROM san_pham")
    tat_ca_hang=con_tro.fetchall()
    ket_noi.close()
    
    danh_sach_sp=[]
    for hang in tat_ca_hang:
        danh_sach_sp.append({
            "id":hang["id"],
            "ten_sp":hang["ten_sp"],
            "gia":hang["gia"]
        })

    return{
        "status":"Thành công",
        "thong_bao":f"Chào {nguoi_dung['sub']}! Bạn đã truy cập kho bảo mật thành công",
        "kho_hang":danh_sach_sp
    }

@app.post("/them-hang-bao-mat")
def api_them_hang_bao_mat(hang:SanPhamNhap,nguoi_dung=Depends(xac_thuc_nguoi_dung)):
    ket_noi=sqlite3.connect("kho_hang.db")
    con_tro=ket_noi.cursor()
    con_tro.execute("INSERT INTO san_pham (ten_sp,gia) VALUES (?,?)",(hang.ten_sp,hang.gia))
    ket_noi.commit()
    ket_noi.close()
    return{"status":"Thành công","message":f"Người dùng '{nguoi_dung['sub']}' đã thêm món '{hang.ten_sp}' vào kho!"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=9000)
