from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import news_cache as news



# 创建APIRouter 实例
# prefix 路由前缀
router = APIRouter(prefix="/api/news", tags=["news"])


# 接口实现流程
# 1.模块胡路由-> API接口规范文档
# 2.定义模块类型 -> 数据库表（数据库设计文档）
# 3.在crud 文件夹里创建文件，封装操作数据库的方法
# 4.在路由处理函数中调用crud封装好的方法，相应结果

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100,db:AsyncSession = Depends(get_db)):
    # 先获取数据库里的新闻模块模型类
    categories = await news.get_categories(db,skip=skip, limit=limit)
    return {
        "code": 200,
        "message": "获取分类成功",
        "data": categories
    }

@router.get("/list")
async def get_news_list(
        category_id:int=Query(...,alias="categoryId"),
        page:int=1,
        page_size:int=Query(10,alias="pageSize",le=100),
        db:AsyncSession = Depends(get_db),
):
    # 思想 处理分页则-> 查询新闻列表->计算总量-> 计算是否还有更多
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db,category_id,offset,page_size)
    news_count = await news.get_news_count(db,category_id)
    has_next = (offset+ len(news_list))< news_count
    return{
        "code": 200,
        "message": "获取新闻列表成功",
        "data":{
            "list":news_list,
            "total":news_count,
            "hasMore":has_next

        }
    }

@router.get("/detail")
async def get_news_detail(news_id:int = Query(...,alias="id"),db:AsyncSession = Depends(get_db)):
    news_detail = await news.get_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")
    views_res = await  news.increase_news_views(db,news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")
    related_news = await news.get_related_news(db,news_detail.id,news_detail.category_id)
    return{
        "code": 200,
        "message": "success",
        "data":{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":related_news,
        }
    }