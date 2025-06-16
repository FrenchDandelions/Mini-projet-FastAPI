from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Dataset(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    filepath: str
    size: int
    upload_time: datetime = Field(default_factory=datetime.now)