from typing import Annotated
from database import get_session
from fastapi import APIRouter, Depends, UploadFile, File, Request
from sqlmodel import Session, select
from models import Dataset
from schemas import DatasetInfo, DatasetBasicInfo
from utils import save_csv, in_memory_dataframes, to_excel, to_json, to_pdf
from fastapi.responses import JSONResponse, FileResponse
from limiter import limiter, get_file_lock, pop_file_lock
import os


SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/", response_model=DatasetBasicInfo)
@limiter.limit("15/minute")
async def upload_dataset(request: Request, file: UploadFile = File(...), session: Session = Depends(get_session)):
    filename, filepath, size, df = save_csv(file)
    dataset = Dataset(filename=filename, filepath=filepath, size=size)
    session.add(dataset)
    session.commit()
    session.refresh(dataset)
    in_memory_dataframes[dataset.id] = df
    return dataset


@router.get("/", response_model=list[DatasetBasicInfo])
@limiter.limit("15/minute")
async def list_dataset(request: Request, session: Session = Depends(get_session)):
    statement = select(Dataset)
    return session.exec(statement).all()


@router.get("/{dataset_id}/", response_model=DatasetInfo)
@limiter.limit("15/minute")
async def info_dataset(request: Request, dataset_id: int, session: Session = Depends(get_session)):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    return dataset


@router.delete("/{dataset_id}/")
@limiter.limit("15/minute")
async def delete_dataset(request: Request, dataset_id: int, session: Session = Depends(get_session)):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    lock = await get_file_lock(dataset_id=dataset_id)
    async with lock:
        os.remove(dataset.filepath)
        in_memory_dataframes.pop(dataset.id)
    await pop_file_lock(dataset_id=dataset_id)
    session.delete(dataset)
    session.commit()
    return JSONResponse(status_code=200, content={"detail": "Dataset deleted successfully"})


@router.get("/{dataset_id}/excel/")
@limiter.limit("15/minute")
async def export_dataset(request: Request, dataset_id: int, session: Session = Depends(get_session)):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    filepath = await to_excel(dataset)
    if not filepath:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    filename = filepath.split("/")[-1]
    return FileResponse(filepath,
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        filename=filename)


@router.get("/{dataset_id}/stats/")
@limiter.limit("15/minute")
async def export_dataset(request: Request, dataset_id: int, session: Session = Depends(get_session)):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    json = to_json(dataset)
    if not json:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    return JSONResponse(content=json)


@router.get("/{dataset_id}/plot/")
@limiter.limit("15/minute")
async def export_dataset(request: Request, dataset_id: int, session: Session = Depends(get_session)):
    dataset = session.get(Dataset, dataset_id)
    if not dataset:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    filepath = await to_pdf(dataset)
    if not filepath:
        return JSONResponse(status_code=404, content={"detail": "Dataset not found"})
    filename = filepath.split("/")[-1]
    return FileResponse(filepath,
                        media_type="application/pdf",
                        filename=filename)
