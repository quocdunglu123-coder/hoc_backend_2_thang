from fastapi import APIRouter , Depends
from pydantic import BaseModel
from database.db_helper import lay_ket_noi
from routes.auth_route import xac_thuc_nguoi_dung

router = APIRouter(tags=["Quản lý kho hàng"])

class SanPhamNhap(BaseModel):
    ten_sp:str
    gia:float

@router.get("/xem-kho")
def api_xem_kho(nguoi_dung=Depends(xac_thuc_nguoi_dung)):
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT * FROM san_pham")
    tat_ca_hang=con_tro.fetchall()
    ket_noi.close()
    return{
        "status":"Thành công",
        "thong_bao":f"Chào chủ tài khoản '{nguoi_dung['sub']}' !Bạn đã vào kho mượt mà",
        "data": [dict(hang) for hang in tat_ca_hang]
    }

@router.post("/them-hang")
def api_them_hang(hang:SanPhamNhap,nguoi_dung= Depends(xac_thuc_nguoi_dung)):
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute("INSERT INTO san_pham(ten_sp,gia) VALUES (?,?)",(hang.ten_sp,hang.gia))
    ket_noi.commit()
    ket_noi.close()
    
    return{
        "status":"Thành công",
        "message":f"Tài khoản '{nguoi_dung['sub']}' đã nạp thành công món '{hang.ten_sp}' vào Database!"
    }