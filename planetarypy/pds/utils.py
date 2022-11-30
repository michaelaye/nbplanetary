# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/02f_pds.utils.ipynb.

# %% auto 0
__all__ = ['IndexLabel', 'index_to_df', 'PVLColumn', 'decode_line', 'find_mixed_type_cols', 'fix_hirise_edrcumindex']

# %% ../../notebooks/02f_pds.utils.ipynb 3
from typing import Union
from tqdm.auto import tqdm
from fastcore.utils import Path
import warnings

import pandas as pd
import pvl
from .. import utils

# %% ../../notebooks/02f_pds.utils.ipynb 4
class IndexLabel:
    "Support working with label files of PDS Index tables."

    def __init__(
        self,
        # Path to the labelfile for a PDS Indexfile.
        # The actual table should reside in the same folder to be automatically parsed
        # when calling the `read_index_data` method.
        labelpath: Union[str, Path],
    ):
        self.path = Path(labelpath)
        "search for table name pointer and store key and fpath."
        tuple = [i for i in self.pvl_lbl if i[0].startswith("^")][0]
        self.tablename = tuple[0][1:]
        self.index_name = tuple[1]

    @property
    def index_path(self):
        p = self.path.parent / self.index_name
        if not p.exists():
            # Fudging path name to lower case, opposing label value. (PDS data inconsistency)"
            p = self.path.parent / self.index_name.lower()
        if not p.exists():
            warnings.warn("`index_path` still doesn't exist.")
        return p

    @property
    def pvl_lbl(self):
        return pvl.load(str(self.path))

    @property
    def table(self):
        return self.pvl_lbl[self.tablename]

    @property
    def pvl_columns(self):
        return self.table.getlist("COLUMN")

    @property
    def columns_dic(self):
        return {col["NAME"]: col for col in self.pvl_columns}

    @property
    def colnames(self):
        """Read the columns in an PDS index label file.

        The label file for the PDS indices describes the content
        of the index files.
        """
        colnames = []
        for col in self.pvl_columns:
            colnames.extend(PVLColumn(col).name_as_list)
        return colnames

    @property
    def colspecs(self):
        colspecs = []
        columns = self.table.getlist("COLUMN")
        for column in columns:
            pvlcol = PVLColumn(column)
            if pvlcol.items is None:
                colspecs.append(pvlcol.colspecs)
            else:
                colspecs.extend(pvlcol.colspecs)
        return colspecs

    def read_index_data(self, convert_times=True):
        return index_to_df(self.index_path, self, convert_times=convert_times)

# %% ../../notebooks/02f_pds.utils.ipynb 5
def index_to_df(
    # Path to the index TAB file
    indexpath: Union[str, Path],
    # Label object that has both the column names and the columns widths as attributes
    # 'colnames' and 'colspecs'
    label: IndexLabel,
    # Switch to control if to convert columns with "TIME" in name (unless COUNT is as well in name) to datetime
    convert_times=True,
):
    """The main reader function for PDS Indexfiles.

    In conjunction with an IndexLabel object that figures out the column widths,
    this reader should work for all PDS TAB files.
    """
    indexpath = Path(indexpath)
    df = pd.read_fwf(
        indexpath, header=None, names=label.colnames, colspecs=label.colspecs
    )
    if convert_times:
        for column in [col for col in df.columns if "TIME" in col]:
            if column in ["LOCAL_TIME", "DWELL_TIME"]:
                continue
            try:
                df[column] = pd.to_datetime(df[column])
            except ValueError:
                df[column] = pd.to_datetime(
                    df[column], format=utils.nasa_dt_format_with_ms, errors="coerce"
                )
            except KeyError:
                raise KeyError(f"{column} not in {df.columns}")
        print("Done.")
    return df

# %% ../../notebooks/02f_pds.utils.ipynb 6
class PVLColumn:
    "Manages just one of the columns in a table that is described via PVL."

    def __init__(self, pvlobj):
        self.pvlobj = pvlobj

    @property
    def name(self):
        return self.pvlobj["NAME"]

    @property
    def name_as_list(self):
        "needs to return a list for consistency for cases when it's an array."
        if self.items is None:
            return [self.name]
        else:
            return [self.name + "_" + str(i + 1) for i in range(self.items)]

    @property
    def start(self):
        "Decrease by one as Python is 0-indexed."
        return self.pvlobj["START_BYTE"] - 1

    @property
    def stop(self):
        return self.start + self.pvlobj["BYTES"]

    @property
    def items(self):
        return self.pvlobj.get("ITEMS")

    @property
    def item_bytes(self):
        return self.pvlobj.get("ITEM_BYTES")

    @property
    def item_offset(self):
        return self.pvlobj.get("ITEM_OFFSET")

    @property
    def colspecs(self):
        if self.items is None:
            return (self.start, self.stop)
        else:
            i = 0
            bucket = []
            for _ in range(self.items):
                off = self.start + self.item_offset * i
                bucket.append((off, off + self.item_bytes))
                i += 1
            return bucket

    def decode(self, linedata):
        if self.items is None:
            start, stop = self.colspecs
            return linedata[start:stop]
        else:
            bucket = []
            for (start, stop) in self.colspecs:
                bucket.append(linedata[start:stop])
            return bucket

    def __repr__(self):
        return self.pvlobj.__repr__()

# %% ../../notebooks/02f_pds.utils.ipynb 7
def decode_line(
    linedata: str,  # One line of a .tab data file
    labelpath: Union[
        str, Path
    ],  # Path to the appropriate label that describes the data.
):
    "Decode one line of tabbed data with the appropriate label file."
    label = IndexLabel(labelpath)
    for column in label.pvl_columns:
        pvlcol = PVLColumn(column)
        print(pvlcol.name, pvlcol.decode(linedata))

# %% ../../notebooks/02f_pds.utils.ipynb 8
def find_mixed_type_cols(
    # Dataframe to be searched for mixed data-types
    df: pd.DataFrame,
    # Switch to control if NaN values in these problem columns should be replaced by the string 'UNKNOWN'
    fix: bool = True,
) -> list:  # List of column names that have data type changes within themselves.
    """For a given dataframe, find the columns that are of mixed type.

    Tool to help with the performance warning when trying to save a pandas DataFrame as a HDF.
    When a column changes datatype somewhere, pickling occurs, slowing down the reading process of the HDF file.
    """
    result = []
    for col in df.columns:
        weird = (df[[col]].applymap(type) != df[[col]].iloc[0].apply(type)).any(axis=1)
        if len(df[weird]) > 0:
            print(col)
            result.append(col)
    if fix is True:
        for col in result:
            df[col].fillna("UNKNOWN", inplace=True)
    return result

# %% ../../notebooks/02f_pds.utils.ipynb 9
def fix_hirise_edrcumindex(
    infname: Union[str, Path],  # Path to broken EDRCUMINDEX.TAB
    outfname: Union[str, Path],  # Path where to store the fixed TAB file
):
    """Fix HiRISE EDRCUMINDEX.

    The HiRISE EDRCUMINDEX has some broken lines where the SCAN_EXPOSURE_DURATION is of format
    F10.4 instead of the defined F9.4.
    This function simply replaces those incidences with one less decimal fraction, so 20000.0000
    becomes 20000.000.
    """
    with Path(infname).open() as f:
        with Path(outfname).open("w") as newf:
            for line in tqdm(f):
                exp = line.split(",")[21]
                if float(exp) > 9999.999:
                    # catching the return of write into dummy variable
                    _ = newf.write(line.replace(exp, exp[:9]))
                else:
                    _ = newf.write(line)
