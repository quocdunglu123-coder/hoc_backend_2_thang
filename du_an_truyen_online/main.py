import uvicorn
from fastapi import FastAPI
from database.db_comic import khoi_tao_he_thong
from routes.auth import auth_route
from routes.truyen import router_truyen

app=FastAPI(title="Hệ thống backend Truyện online - Ngày 22")
khoi_tao_he_thong()
app.include_router(auth_route)
app.include_router(router_truyen)

if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=9500,reload=True)