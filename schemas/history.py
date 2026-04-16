
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class HistoryAddRequest(BaseModel):
    news_id: int = Field(...,alias="newsId")

class HistoryNewsItemResponse(NewsItemBase):
    history_id: int = Field(...,alias="historyId")
    view_time: datetime = Field(...,alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HistoryListResponse(BaseModel):
    list: List[HistoryNewsItemResponse]
    total:int
    has_more: bool=Field(...,alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )