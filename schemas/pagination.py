from pydantic import BaseModel
from typing import Generic, TypeVar, List


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    limit: int
    data: List[T]
