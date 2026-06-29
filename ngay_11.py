from fastapi import FastAPI 
app = FastAPI()
@app.get("/")
def trang_chu():
    return {"message" : "Chào mừng đến với trang chủ của tôi !"}
@app.get("/")
def thong_tin_coder():
    return{
        "ten":"Quốc Dũng",
        "vai_tro":"Backend Developer",
        "ngay_hoc":11
    }
@app.get("/kho-hang")
def xem_kho():
    danh_sach = [
        {"ten":"Chuột máy tính","gia":500},
        {"ten":"Bàn phím cơ","gia":1500},
        {"ten":"Màn hình Asus","gia":4500}
    ]
    return danh_sach
