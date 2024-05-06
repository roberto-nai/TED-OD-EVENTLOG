### IMPORT ###
from pathlib import Path
import pandas as pd

### FUNCTIONS ###

def list_files_by_type(directory: str, extension: str) -> list:
    """
    Returns a list of files with a given extension (case sensitive) in a specified directory, excluding temporary files.
    
    Args:
        directory (str): The path to the directory where to search for files.
        extension (str): The extension of the files to be searched for, including the dot (e.g., '.txt').
    
    Returns:
        list: List of Path objects for the found files, excluding temporary and hidden files.
    """

    file_list = []
    # Create a Path object from the directory
    dir_path = Path(directory)
    # Use the glob method to find all files with the given extension and filter out temporary files
    file_list = [file for file in dir_path.glob(f'*{extension}') if not file.name.startswith('.') and not file.name.startswith('~$')]
    return file_list


def read_csv_data(path: str, col_type: dict, csv_sep: str = ",") -> pd.DataFrame:
    """
    Reads data from a CSV file into a pandas DataFrame with specified columns and data types.

    Parameters:
        path (str): the file path to the CSV file to be read.
        col_type (dict): a dictionary of column names and type.
        sep (str): the delimiter string used in the CSV file. Defaults to ';'.

    Returns:
        pd.DataFrame: a pandas DataFrame containing the data read from the CSV file.
    """

    df = pd.read_csv(path, dtype=col_type, sep=csv_sep, low_memory=False)
    df = df.drop_duplicates()
    return df

def fix_date(date: str) -> str:
    """
    Given a date string with named months (e.g., '25-MAR-22'), transforms it into a date string
    with numeric months (e.g., '2022-03-25').

    Args:
        date (str): A date string in the format 'DD-MMM-YY' or 'DD-MMM-YYYY'.

    Returns:
        str: The transformed date string in the format 'YYYY-MM-DD'.
    """
    month_mapping = {
        'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06',
        'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
    }
    day, month, year = date.upper().split("-")
    
    # Check year format and adjust if necessary
    if len(year) == 2:
        year = '20' + year
    elif len(year) == 4:
        year = year
    else:
        print(f"ERROR! Year '{year}' is not a valid year abbreviation.")
        return None

    # Validate month abbreviation
    if month not in month_mapping:
        print(f"ERROR! Month '{month}' is not a valid month abbreviation.")
        return None

    # Format the new date string
    new_date = f"{year}-{month_mapping[month]}-{day}"
    return new_date

def data_schema(df: pd.DataFrame) ->  pd.DataFrame:
    """
    Given a dataframe generates its schema (column_name, type)

    Parameters:
        df (pd.DataFrame): the file path to the CSV file to be read.

    Returns:
        pd.DataFrame: a dataframe with (column_name, type)
    """
    col_names_and_types = pd.DataFrame({
    'column_name': df.columns,
    'data_type': [str(dtype) for dtype in df.dtypes]
    })

    return col_names_and_types

