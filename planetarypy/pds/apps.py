# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/api/02c_pds.apps.ipynb.

# %% auto 0
__all__ = ['find_indexes', 'get_index', 'find_instruments']

# %% ../../notebooks/api/02c_pds.apps.ipynb 3
import pandas as pd
from ..config import config
from .indexes import Index

# %% ../../notebooks/api/02c_pds.apps.ipynb 4
def find_indexes(
        instrument: str,  # Dotted mission.instrument key, e.g. cassini.iss
) -> list:  # List of configured index names
    "Find existing indexes for an instrument."
    return config.list_indexes(instrument)

# %% ../../notebooks/api/02c_pds.apps.ipynb 7
def get_index(
        instr: str,  # Dotted instrument index, e.g. cassini.iss
        index_name: str = '',  # Index name, for exmample 'moon_summary. Optional'
        refresh: bool = False,  # switch to force a refresh of an index
        check_update: bool = True,  # switch off for faster return time.
) -> pd.DataFrame:  # The PDS index convert to pandas DataFrame
    """Example: get_index("cassini.iss", "index")"""
    # I need to add the check_update switch to the constructor b/c of dynamic url setting that always
    # wants to go online to find the latest volume URL.
    if not index_name:
        index = Index(instr, check_update=check_update)
    else:
        index = Index(instr + ".indexes." + index_name, check_update=check_update)
    if not index.local_table_path.exists() or refresh:
        index.download()
    if check_update and index.update_available:
        print("An updated index is available.")
        print("Call `get_index` with `refresh=True` to get the updated version.")
    if not index.local_parq_path.exists():
        index.convert_to_parquet()
    return index.parquet

# %% ../../notebooks/api/02c_pds.apps.ipynb 15
def find_instruments(
        mission: str,  # Mission string, e.g. "cassini"
) -> list:  # List of configured instrument names
    "Find existing instruments for a mission."
    return config.list_instruments(mission)
