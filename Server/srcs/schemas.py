from pydantic import BaseModel
from datetime import datetime


class DatasetInfo(BaseModel):
    id: int
    filename: str
    size: int
    upload_time: datetime
    
    class Config:
        orm_mode = True
