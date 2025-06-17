from typing import Annotated
from database import get_session
from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session, select
from models import Dataset
from schemas import DatasetInfo, DatasetBasicInfo
from utils import save_csv, in_memory_dataframes, to_excel
from fastapi.responses import JSONResponse, FileResponse
import os


SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/", response_model=DatasetBasicInfo)
async def upload_dataset(file: UploadFile = File(...), session: Session = Depends(get_session)):
    filename, filepath, size, df = save_csv(file)
    dataset = Dataset(filename=filename, filepath=filepath, size=size)
    session.add(dataset)
    session.commit()
    session.refresh(dataset)
    in_memory_dataframes[dataset.id] = df
    return dataset


@router.get("/", response_model=list[DatasetBasicInfo])
async def list_dataset(session: Session = Depends(get_session)):
    statement = select(Dataset)
    return session.exec(statement).all()


@router.get("/{dataset_id}/", response_model=DatasetInfo)
async def info_dataset(dataset_id: int, session: Session = Depends(get_session)):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    return dataset


@router.delete("/{dataset_id}/")
async def delete_dataset(dataset_id: int, session: Session = Depends(get_session)):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    os.remove(dataset.filepath)
    in_memory_dataframes.pop(dataset.id)
    session.delete(dataset)
    session.commit()
    return JSONResponse(status_code=200, content={"detail": "Dataset deleted successfully"})


@router.get("/{dataset_id}/excel/")
async def export_dataset(dataset_id: int, session: Session = Depends(get_session)):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    filepath = to_excel(dataset)
    filename = filepath.split("/")[-1]
    return FileResponse(filepath,
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        filename=filename)