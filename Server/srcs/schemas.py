from pydantic import BaseModel
from datetime import datetime


class DatasetInfo(BaseModel):
    """
    Schema for detailed dataset information returned by API.
    """
    id: int
    filename: str
    size: int
    upload_time: datetime
    
    class Config:
        orm_mode = True

class DatasetBasicInfo(BaseModel):
    """
    Schema for basic dataset information (id and filename).
    """
    id: int
    filename: str

    class Config:
        orm_mode = True
