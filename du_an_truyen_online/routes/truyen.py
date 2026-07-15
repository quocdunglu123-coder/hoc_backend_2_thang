from fastapi import APIRouter,HTTPException,Depends,status
from pydantic import BaseModel
from database.db_comic import lay_ket_noi
from routes.auth import xac_thuc_nguoi_dung

router_truyen=APIRouter(tags=["Quản lý Truyện online"])

class TruyenForm(BaseModel):
    ten_truyen:str
    tac_gia:str
    noi_dung:str

@router_truyen.get("/xem-truyen")
def api_xem_truyen():
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT * FROM truyen")
    tat_ca_truyen=con_tro.fetchall()
    ket_noi.close()
    return [dict(t) for t in tat_ca_truyen]

@router_truyen.post("/them-truyen")
def api_them_truyen(truyen:TruyenForm ,nguoi_dung=Depends(xac_thuc_nguoi_dung)):
    if nguoi_dung.get("role") !="admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Thất bại! Bạn là đọc giả thường, không có đặc quyền Admin để xuất bản truyện!"
            )
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute(
        "INSERT INTO truyen(ten_truyen,tac_gia,noi_dung) VALUES (?,?,?)",
        (truyen.ten_truyen,truyen.tac_gia,truyen.noi_dung)
    )
    ket_noi.commit()
    ket_noi.close()
    return {"status":"Thành công","message":f"Admin '{nguoi_dung['sub']}' đã xuất bản thành công '{truyen.ten_truyen}'!"}