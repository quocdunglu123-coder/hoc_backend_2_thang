import uvicorn
from fastapi import FastAPI

from database.db_helper import khoi_tao_bang
from routes.san_pham_route import router as san_pham_router
from routes.auth_route import auth_route

app=FastAPI(tittle="Hệ thống quản lý kho hàng chuẩn MVC - Bảo mật cao cấp")

khoi_tao_bang()

app.include_router(san_pham_router)
app.include_router(auth_route)

if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=9000,reload=True)