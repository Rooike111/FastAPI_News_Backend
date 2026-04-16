from fastapi import APIRouter, Depends,HTTPException
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from models.users import User
from schemas.history import HistoryAddRequest, HistoryNewsItemResponse, HistoryListResponse
from utils.auth import get_current_user
from utils.response import success_response
from crud import history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
        data: HistoryAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    new_history = await history.add_news_history(db, user.id, data.news_id)
    return success_response(message="添加成功", data=new_history)


@router.get("/list")
async def get_history_list(
        page: int = Query(1,ge=1),
        page_size: int = Query(10, le=100, ge=1, alias="pageSize"),
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),

):
    offset = (page - 1) * page_size
    rows, count = await history.get_history_list(db, user.id, offset, page_size)
    print("rows****",rows)
    has_more = count >page_size * page

    history_list = [HistoryNewsItemResponse.model_validate({
        **news.__dict__,
        "view_time": view_time,
        "history_id": history_id
    }) for news, view_time, history_id in rows]
    result = HistoryListResponse(list=history_list,total=count,hasMore=has_more)
    return success_response(message="获取成功",data=result)

@router.delete("/delete/{history_id}")
async def delete_history(history_id: int,
                         user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    """
    删除历史记录
    """
    result = await history.delete_history(db, user.id, history_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="历史记录不存在")
    return success_response(message="删除成功")

@router.delete("/clear")
async def clear_history(user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    """
    清空历史记录
    """
    result = await history.clear_history(db, user.id)
    return success_response(message="清空成功")