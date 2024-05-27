### IMPORT ###
from pathlib import Path
import pandas as pd
import json

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

def json_data_to_list_dict(json_file:str) -> list:
    """
    Extracts all keys and their associated values from a JSON file.

    Args:
        json_file (str): The path to the JSON file.

    Returns:
        list: A list of dictionaries, each containing a key and its associated values, or None if the file does not exist or cannot be decoded.
    """
    file_path = Path(json_file)
    
    if not file_path.exists():
        print(f"The file '{json_file}' does not exist.")
        return None
    
    try:
        with file_path.open('r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from the file '{json_file}': {e}")
        return None
    
    keys_and_values = [{key: values} for key, values in data.items()]
    
    return keys_and_values

def df_filter(df: pd.DataFrame, filter_conditions:list) -> pd.DataFrame:
    """
    Filters a DataFrame based on the conditions specified in filter_conditions.

    Parameters:
        df (pd.DataFrame): The DataFrame to be filtered.
        filter_conditions (list): A list of dictionaries containing column names as keys and lists of allowed values as values.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    for condition in filter_conditions:
        print("Filtering for:", condition, end="")
        for column, values in condition.items():
            df = df[df[column].isin(values)]
        print(" [OK]")
    return df

def df_uniques(df: pd.DataFrame, filter_conditions:list) -> None:
    """
    Displays unique/distinct values of a list of columns.

    arameters:
        df (pd.DataFrame): The DataFrame to be checked.
        filter_conditions (list): A list of dictionaries containing column names as keys and lists of allowed values as values.

    Returns:
        None.
    """
    for condition in filter_conditions:
        for column in condition.keys():
            unique_values = df[column].unique().tolist()
            print(f"Unique values for column '{column}': {unique_values}")


def df_stats_by_year(df: pd.DataFrame, list_stats_floats: list, list_stats_int: list) -> pd.DataFrame:
    """
    Calculate annual statistics for specified columns in a DataFrame.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame containing data.
    list_stats_floats (list): List of column names for which to calculate min, mean, and max values.
    list_stats_int (list): List of column names for which to count distinct values.
    
    Returns:
    pd.DataFrame: A DataFrame containing the annual statistics for the specified columns.
    """
    # Group by year
    grouped = df.groupby('YEAR')
    
    # List to store results
    stats = []
    
    for year, group in grouped:
        # Calculate statistics for float columns
        stats_floats = group[list_stats_floats].agg(['min', 'mean', 'max']).reset_index()
        stats_floats.columns = ['YEAR'] + ['{}_{}'.format(col[0], col[1]) for col in stats_floats.columns[1:]]
        stats_floats = stats_floats.melt(id_vars='YEAR', var_name='METRIC', value_name='VALUE')
        
        # Calculate distinct counts for int columns
        stats_int = group[list_stats_int].nunique().reset_index()
        stats_int = stats_int.melt(id_vars='YEAR', var_name='COLUMN', value_name='VALUE')
        stats_int['METRIC'] = 'nunique'
        
        # Combine the results
        stats_combined = pd.concat([stats_floats, stats_int], axis=0)
        stats.append(stats_combined)
    
    # Concatenate all annual DataFrames
    return pd.concat(stats).reset_index(drop=True)