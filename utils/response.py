from fastapi.encoders import  jsonable_encoder
from starlette.responses import JSONResponse


def success_response(message:str = "success",data=None) -> JSONResponse:
    content = {
        "code": 200,
        "message": message,
        "data": data
    }

    # 把任何的FastAPI， Pydantic ORM 对象 都正常响应-> code\message\data
    return JSONResponse(content=jsonable_encoder(content))