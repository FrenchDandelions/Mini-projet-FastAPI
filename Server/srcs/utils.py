import pandas as pd
import uuid
import os
import matplotlib.pyplot as plt
import io
from models import Dataset


SAVE_DIR=os.environ["DATA_DIR"]
in_memory_dataframes={int: pd.DataFrame}


def save_csv(file) -> (str | str | int | pd.DataFrame):
    content = file.file.read()
    filename = file.filename
    df = pd.read_csv(io.BytesIO(content))
    uid = uuid.uuid4().hex
    filepath = os.path.join(SAVE_DIR, f'{uid}.csv')

    with open(filepath, 'wb') as f:
        f.write(content)

    return filename, filepath, len(content), df


def to_excel(dataset: Dataset) -> any:
    df = in_memory_dataframes[dataset.id]
    filename = dataset.filename
    filename = filename.removesuffix(".csv")
    sheetname = str(filename)
    filename += f"_id_{dataset.id}.xlsx"
    if not os.path.isfile(filename):
        df.to_excel(filename, sheet_name=sheetname)
    return filename
