from fastapi import FastAPI
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)
#允许访问的来源
origins= [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8080",
]

# 解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 开发时 开发阶段允许所有源，，生产环境需要指定
    allow_credentials=True,
    allow_methods=["*"], # 允许访问的方法
    allow_headers=["*"], # 允许所有请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 挂在路由
app.include_router(news.router)

app.include_router(users.router)

app.include_router(favorite.router)

app.include_router(history.router)