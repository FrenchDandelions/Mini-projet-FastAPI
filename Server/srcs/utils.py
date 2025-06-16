import pandas as pd
import uuid
import os
import matplotlib.pyplot as plt
import io


SAVE_DIR=os.environ["DATA_DIR"]
in_memory_dataframes={}


def save_csv(file) -> (str | str | int | pd.DataFrame):
    content = file.file.read()
    filename = file.filename
    df = pd.read_csv(io.BytesIO(content))
    uid = uuid.uuid4().hex
    filepath = os.path.join(SAVE_DIR, f'{uid}.csv')

    with open(filepath, 'wb') as f:
        f.write(content)

    return filename, filepath, len(content), df
