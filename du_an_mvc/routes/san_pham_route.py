from fastapi import APIRouter
from pydantic import BaseModel
from database.db_helper import lay_ket_noi

router=APIRouter()

class SanPhamNhap(BaseModel):
    ten_sp:str
    gia:float

@router.get("/xem-kho")
def api_xem_kho():
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT * FROM san_pham")
    tat_ca_hang=con_tro.fetchall()
    ket_noi.close()
    return[dict(hang) for hang in tat_ca_hang]