from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    data: list[dict]
    page: int
    per_page: int