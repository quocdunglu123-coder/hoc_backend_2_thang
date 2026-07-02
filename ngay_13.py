from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
class sanphammoi(BaseModel):
    ten_sp : str
    gia : float
    so_luong : int
@app.post("/them_san_pham")
def them_san_pham(du_lieu:sanphammoi):
    return{
    "thong_bao": "Server backend đã nhận được dữ liệu thành công!",
    "du_lieu_nhan_duoc": du_lieu,
    "goi_y_ngay_mai": f"Ngày mai chúng ta sẽ bốc dữ liệu '{du_lieu.ten_sp}' này",
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=9000)