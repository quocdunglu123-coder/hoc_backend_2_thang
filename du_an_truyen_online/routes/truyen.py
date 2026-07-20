import sqlite3
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
def api_xem_truyen(tu_khoa:str="",trang:int=1,so_luong:int=5):
    bo_qua=(trang-1)*so_luong
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    cau_lenh_sql="""
        SELECT * FROM truyen
        WHERE ten_truyen LIKE ?
        LIMIT ? OFFSET ?
    """
    tu_khoa_tim_kiem=f"%{tu_khoa}%"
    con_tro.execute(cau_lenh_sql,(tu_khoa_tim_kiem,so_luong,bo_qua))
    tat_ca_truyen=con_tro.fetchall()
    ket_noi.close()
    return {
        "status":"Thành công",
        "bo_loc":{
            "tu_khoa_tim_kiem":tu_khoa,
            "trang_hien_tai":trang,
            "so_luong_moi_trang":so_luong
        },
        "danh_sach_truyen":[dict(t) for t in tat_ca_truyen]
    }

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

@router_truyen.put("/sua_truyen/{truyen_id}")
def api_sua_truyen(truyen_id:int,truyen:TruyenForm,nguoi_dung=Depends(xac_thuc_nguoi_dung)):
    if nguoi_dung.get("role")!="admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Thất bại ! Bạn không có đặc quyền Admin để chỉnh sửa nội dung Truyện!"
        )
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute(
        "UPDATE truyen SET ten_truyen=?,tac_gia=?,noi_dung=? WHERE id=?",
        (truyen.ten_truyen,truyen.noi_dung,truyen.tac_gia,truyen_id)
    )
    ket_noi.commit()
    ket_noi.close()
    return{"status":"Thành công","message":f"Admin '{nguoi_dung['sub']}' đã cập nhật truyện ID số {truyen_id} vĩnh viễn!"}

@router_truyen.delete("/xoa-truyen/{id_truyen}")
def api_xoa_truyen(truyen_id:int,nguoi_dung=Depends(xac_thuc_nguoi_dung)):
    if nguoi_dung.get("role") !="admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Thất bại! Bạn không có đặc quyền Admin để xóa truyện!"
        )
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute("DELETE FROM truyen WHERE id=?",(truyen_id,))
    ket_noi.commit()
    ket_noi.close()
    return{"status":"Thành công","message":f"Admin '{nguoi_dung['sub']}' đã xóa hoàn toàn truyện ID số {truyen_id}!"}

class LichSuForm(BaseModel):
    truyen_id:int

@router_truyen.post("/luu_lich_su")
def api_luu_lich_su(form_data:LichSuForm,nguoi_dung=Depends(xac_thuc_nguoi_dung)):
    ket_noi=lay_ket_noi()
    con_tro=ket_noi.cursor()
    con_tro.execute("SELECT id FROM nguoi_dung WHERE tai_khoan=?",(nguoi_dung["sub"],))
    user_db=con_tro.fetchone()

    if user_db is None:
        ket_noi.close()
        raise HTTPException(status_code=404,detail="Không tìm thấy thông tin người dùng!")
    
    user_id=user_db["id"]

    con_tro.execute(
        "INSERT INTO lich_su_doc (nguoi_dung_id,truyen_id) VALUES (?,?)",
        (user_id,form_data.truyen_id)
    )
    ket_noi.commit()
    ket_noi.close()
    return{"status":"Thành công","message":f"Đã lưu truyện id số {form_data.truyen_id} vào lịch sử đọc của bạn!"}

@router_truyen.get("/xem-lich-su")
def api_xem_lich_su(nguoi_dung=Depends(xac_thuc_nguoi_dung)):
    ket_noi=lay_ket_noi()
    ket_noi.row_factory = sqlite3.Row
    con_tro=ket_noi.cursor()
    cau_lenh_sql = """
        SELECT truyen.ten_truyen,truyen.tac_gia,lich_su_doc.ngay_doc
        FROM lich_su_doc
        INNER JOIN truyen ON lich_su_doc.truyen_id=truyen.id
        INNER JOIN nguoi_dung ON lich_su_doc.nguoi_dung_id=nguoi_dung.id
        WHERE nguoi_dung.tai_khoan=?
        ORDER BY lich_su_doc.ngay_doc DESC
    """
    con_tro.execute(cau_lenh_sql,(nguoi_dung["sub"],))
    tat_ca_lich_su=con_tro.fetchall()
    ket_noi.close()

    danh_sach_ls=[]
    for dong in tat_ca_lich_su:
        danh_sach_ls.append({
            "ten_truyen":dong["ten_truyen"],
            "tac_gia":dong["tac_gia"],
            "ngay_doc":dong["ngay_doc"]
        })
    return{
        "status":"Thành công",
        "tai_khoan":nguoi_dung["sub"],
        "lich_su_doc":danh_sach_ls
    }