from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class Dataset(SQLModel, table=True):
    """
    Database model for storing dataset metadata.
    
    Attributes:
        id (int): unique dataset ID (primary key)
        filename (str): original uploaded filename
        filepath (str): path where CSV is saved
        size (int): file size in bytes
        upload_time (datetime): timestamp when dataset was uploaded
    """
    id: Optional[int] | None = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    filepath: str
    size: int
    upload_time: datetime = Field(default_factory=datetime.now)