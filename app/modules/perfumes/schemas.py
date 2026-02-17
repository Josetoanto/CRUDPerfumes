from pydantic import BaseModel
from typing import Optional



class PerfumeCreate(BaseModel):
    name: str
    brand: str
    description: Optional[str] = None
    stock: int
    price: float


class PerfumeResponse(PerfumeCreate):
    id: int

    class Config:
        orm_mode = True
