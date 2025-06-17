import pandas as pd
from pandas.api.types import is_numeric_dtype
# from pandas.api.types import is_bool_dtype, is_object_dtype, is_categorical_dtype
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from models import Dataset
from limiter import get_file_lock
import io
import uuid
import os
import re


SAVE_DIR=os.environ["DATA_DIR"]
in_memory_dataframes={int: pd.DataFrame}


def save_csv(file) -> (str | str | int | pd.DataFrame):
    """
    Save uploaded CSV file to disk and load it as a DataFrame.
    
    Returns:
        filename (str): original filename
        filepath (str): path where file is saved
        size (int): size in bytes
        df (pd.DataFrame): loaded dataframe
    """
    content = file.file.read()
    filename = file.filename
    df = pd.read_csv(io.BytesIO(content))
    uid = uuid.uuid4().hex
    filepath = os.path.join(SAVE_DIR, f'{uid}.csv')

    with open(filepath, 'wb') as f:
        f.write(content)

    return filename, filepath, len(content), df


async def to_excel(dataset: Dataset) -> str | None:
    """
    Export dataset as an Excel file.
    
    Returns:
        filepath (str): path to the Excel file or None if dataset not found.
    """
    df = in_memory_dataframes.get(dataset.id, None)
    if df is None:
        return None
    lock = await get_file_lock(dataset_id=dataset.id)
    async with lock:
        filename = dataset.filename
        filename = filename.removesuffix(".csv")
        sheetname = str(filename)
        sheetname = re.sub(r'[:\\/?*\[\]]', '_', sheetname)
        filename += f"_id_{dataset.id}.xlsx"
        if not os.path.isfile(filename):
            df.to_excel(filename, sheet_name=sheetname)
    return filename


def to_json(dataset: Dataset) -> any:
    """
    Generate descriptive statistics of dataset as JSON.
    
    Returns:
        JSON string or None if dataset not found.
    """
    df = in_memory_dataframes.get(dataset.id, None)
    if df is None:
        return None
    return df.describe().to_json()


def plot_numerical_data(ax, data, column):
    """
    Plot histogram with mean and median lines for numerical data.
    
    Args:
        ax (matplotlib.axes.Axes): plot axes
        data (pd.Series): numerical data to plot
        column (str): column name
    """
    unique_vals = data.nunique()
    bins = unique_vals if unique_vals > 1 else 1
    ax.hist(data, bins=bins, edgecolor='black')
    mean = data.mean()
    median = data.median()
    ax.axvline(mean, color='red', linestyle='--', label=f'Mean: {mean:.2f}')
    ax.axvline(median, color='green', linestyle=':', label=f'Median: {median:.2f}')
    ax.set_title(f'Histogram of {column}')
    ax.set_xlabel(column)
    ax.legend()
    return


# def plot_boolean_data(ax, data, column):
    # counts = data.value_counts()
    # ax.bar(counts.index.astype(str), counts.values, color='orange', edgecolor='black')
    # ax.set_title(f'Boolean Count of {column}')
    # ax.set_ylabel("Count")
    # return
#
#
# def plot_other_data(ax, data, column):
    # counts = data.value_counts().head(20)
    # ax.bar(counts.index.astype(str), counts.values, color='lightgreen', edgecolor='black')
    # ax.set_title(f'Top Categories in {column}')
    # ax.set_ylabel("Count")
    # ax.tick_params(axis='x', rotation=45)
    # return
#
#
async def to_pdf(dataset) -> str | None:
    """
    Generate PDF with histograms of all numerical columns.
    
    Returns:
        filepath (str): path to the PDF file or None if dataset not found.
    """
    df = in_memory_dataframes.get(dataset.id, None)
    if df is None:
        return None

    lock = await get_file_lock(dataset_id=dataset.id)
    async with lock:
        filename = dataset.filename.removesuffix(".csv") + f"_id_{dataset.id}.pdf"
        if os.path.isfile(filename):
            return filename
        with PdfPages(filename) as pdf:
            for column in df.columns:
                data = df[column].dropna()
                if data.empty:
                    continue
                fig, ax = plt.subplots(figsize=(8, 5))
                if is_numeric_dtype(data):
                    plot_numerical_data(ax=ax, data=data, column=column)
                # test with bool data types, unquote the function and condition
                # to test them
                # elif is_bool_dtype(data):
                    # plot_boolean_data(ax=ax, data=data, column=column)
                # test with object and category data types, unquote the function
                # and condition to test them
                # elif is_object_dtype(data) or is_categorical_dtype(data):
                    # plot_other_data(ax=ax, data=data, column=column)
                else:
                    plt.close(fig)
                    continue
                fig.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)
    return filename
