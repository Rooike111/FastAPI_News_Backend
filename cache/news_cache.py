# 新闻相关的缓存方法:新闻分类的读取与写入
# key -value
from config import cache_conf
from typing import List, Any, Dict, Optional

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"
#获取新闻分类
async def get_cached_categories():
    return await cache_conf.get_json_cache(CATEGORIES_KEY)

#  写入新闻分类的缓存: 缓存的数据、过期时间
# 分类 配置 7200， 列表 600 详情 1800 验证码 120 数据越稳定 缓存越持久
async def set_cached_categories(value:List[Dict[str,Any]],expire:int = 7200):
    return await cache_conf.set_cache(CATEGORIES_KEY,value,expire)

# 写入缓存 - 新闻列表
async def set_cached_news_list(
        category_id:Optional[int],
        page:int,
        size:int,
        news_list:List[Dict[str,Any]],
        expire:int = 1800
):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_id}:{page}:{size}"
    return await cache_conf.set_cache(key,news_list,expire)

# 读取缓存 - 新闻列表
async def get_cached_news_list(
        category_id:Optional[int]
        ,page:int
        ,size:int
):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_id}:{page}:{size}"
    return await cache_conf.get_json_cache(key)