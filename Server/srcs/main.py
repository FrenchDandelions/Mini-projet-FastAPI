from typing import Annotated
from database import init_db, get_session, lifespan
from fastapi import FastAPI, Depends, UploadFile, File
from sqlmodel import Session, select
from models import Dataset
from schemas import DatasetInfo
from utils import save_csv, in_memory_dataframes


app = FastAPI(lifespan=lifespan)
SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/datasets/", response_model=DatasetInfo)
async def upload_dataset(file: UploadFile = File(...), session: Session = Depends(get_session)):
    filename, filepath, size, df = save_csv(file)
    dataset = Dataset(filename=filename, filepath=filepath, size=size)
    session.add(dataset)
    session.commit()
    session.refresh(dataset)
    in_memory_dataframes[dataset.id] = df
    return dataset


@app.get("/datasets/", response_model=list[DatasetInfo])
async def list_dataset(session: Session = Depends(get_session)):
    statement = select(Dataset)
    return session.exec(statement).all()
