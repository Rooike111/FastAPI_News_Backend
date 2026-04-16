from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from models.history import History
from models.news import News
from datetime import datetime


async def add_news_history(
        db: AsyncSession,
        user_id: int,
        news_id: int,
):
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    existing_history = result.scalar_one_or_none()
    if existing_history:
        existing_history.view_time = datetime.now()
        await db.commit()
        await db.refresh(existing_history)
        return existing_history
    else:
        new_history = History(news_id=news_id, user_id=user_id)
        db.add(new_history)
        await db.commit()
        await db.refresh(new_history)
        return new_history


async def get_history_list(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        page_size: int = 10,
):
    count_query = select(func.count(History.id)).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = 0 if count_result.scalar_one() else count_result.scalar_one()

    query = (select(News, History.view_time.label("view_time"), History.id.label("history_id"))
             .join(History,History.news_id == News.id)
             .where(History.user_id == user_id)
             .order_by(History.view_time.desc())
             .offset(skip).limit(page_size)
             )
    result = await db.execute(query)
    rows = result.all()
    return rows,total

async def delete_history(db: AsyncSession, user_id: int, news_id: int):
    """
    删除历史记录
    """
    query = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount > 0


async def clear_history(db: AsyncSession, user_id: int):
    """
    清空历史记录
    """
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount or 0

