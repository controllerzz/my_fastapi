from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1)]


PaginationDep = Annotated[PaginationParams, Depends()]