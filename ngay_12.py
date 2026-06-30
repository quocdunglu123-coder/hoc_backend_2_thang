from fastapi import FastAPI
app=FastAPI()
@app.get("/search")
def tim_kiem_san_pham(keyword: str):
    return{
        "thong_bao":f"Bạn đang muốn tìm từ khóa : {keyword}",
        "goi_y_backend":f"Lát nửa chúng ta sẽ dùng từ khóa '{keyword}' này để chạy lệnh WHERE trong SQL Database!"
    }
@app.get("/product/{sanpham_id}")
def chi_tiet_san_pham(sanpham_id:int):
    return{
        "thong_bao":f"Bạn đang xem sản phẩm có ID số : {sanpham_id}",
        "goi_y_backend":f"Lát nữa chúng ta sẽ chạy lệnh SQL: SELECT * FROM san_pham WHERE id = {sanpham_id}"
    }
if __name__ == "__main__" :
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0",port=9000)