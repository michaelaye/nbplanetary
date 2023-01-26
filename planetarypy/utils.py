# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/api/01_utils.ipynb.

# %% auto 0
__all__ = ['logger', 'nasa_date_format', 'nasa_dt_format', 'nasa_dt_format_with_ms', 'iso_date_format', 'iso_dt_format',
           'iso_dt_format_with_ms', 'nasa_time_to_datetime', 'nasa_time_to_iso', 'iso_to_nasa_time',
           'iso_to_nasa_datetime', 'replace_all_nasa_times', 'parse_http_date', 'get_remote_timestamp',
           'check_url_exists', 'url_retrieve', 'have_internet', 'height_from_shadow', 'get_gdal_center_coords',
           'file_variations', 'catch_isis_error']

# %% ../notebooks/api/01_utils.ipynb 3
import datetime as dt
import email.utils as eut
import http.client as httplib
import logging
from math import radians, tan
from pathlib import Path
from typing import Tuple, Union
from urllib.request import urlopen

import pandas as pd
import requests
from astropy.time import Time as ASTROTIME
from kalasiris.pysis import ProcessError
from requests.auth import HTTPBasicAuth
from tqdm.auto import tqdm

try:
    from osgeo import gdal
except ImportError:
    GDAL_INSTALLED = False
else:
    GDAL_INSTALLED = True

# %% ../notebooks/api/01_utils.ipynb 4
logger = logging.getLogger(__name__)

if not GDAL_INSTALLED:
    logger.warning(
        "No GDAL found. Some planetary.utils functions not working, but okay."
    )

# %% ../notebooks/api/01_utils.ipynb 6
nasa_date_format = "%Y-%j"
nasa_dt_format = nasa_date_format + "T%H:%M:%S"
nasa_dt_format_with_ms = nasa_dt_format + ".%f"
iso_date_format = "%Y-%m-%d"
iso_dt_format = iso_date_format + "T%H:%M:%S"
iso_dt_format_with_ms = iso_dt_format + ".%f"

# %% ../notebooks/api/01_utils.ipynb 8
def _nasa_date_to_datetime(
    datestr: str,  # Date string of the form Y-j
) -> dt.datetime:
    "Convert date string to datetime."
    return dt.datetime.strptime(datestr, nasa_date_format)


def _nasa_datetime_to_datetime(
    datetimestr: str,  # datetime string of the form Y-jTH:M:S
) -> dt.datetime:
    "Convert datetime up to seconds to datetime."
    return dt.datetime.strptime(datetimestr, nasa_dt_format)


def _nasa_datetimems_to_datetime(
    datetimestr: str,  # datetime string of the form Y-jTH:M:S.xxx
) -> dt.datetime:
    "Convert date with millisec to datetime."
    return dt.datetime.strptime(datetimestr, nasa_dt_format_with_ms)

# %% ../notebooks/api/01_utils.ipynb 9
def nasa_time_to_datetime(
    inputstr,  # inputstr of format YYYY-jjj, YYYY-jjjTHH:MM:SS or YYYY-jjjTHH:MM:SS.ffffff
) -> dt.datetime:
    "User function to convert all kinds of NASA PDS datestrings with day_of_year into datetimes."
    try:
        return _nasa_datetime_to_datetime(inputstr)
    except ValueError:
        try:
            return _nasa_date_to_datetime(inputstr)
        except ValueError:
            return _nasa_datetimems_to_datetime(inputstr)

# %% ../notebooks/api/01_utils.ipynb 15
def nasa_time_to_iso(
    inputstr: str,
    with_hours: bool = False,  # Switch if return is wanted with hours (i.e. isoformat)
) -> str:  # Datestring in ISO-format.
    """Convert the day-number based NASA datetime format to ISO"""
    has_hours = False
    # check if input has hours
    try:
        res = _nasa_date_to_datetime(inputstr)
    except ValueError:
        has_hours = True
    time = nasa_time_to_datetime(inputstr)
    if has_hours or with_hours is True:
        return time.isoformat()
    else:
        return time.strftime(iso_date_format)

# %% ../notebooks/api/01_utils.ipynb 22
def iso_to_nasa_time(
    inputstr: str,  # Date string of the form Y-m-d
) -> str:  # Datestring in NASA standard yyyy-jjj
    "Convert iso date to day-number based NASA date."
    try:
        date = dt.datetime.strptime(inputstr, iso_date_format)
    except ValueError:
        try:
            date = dt.datetime.strptime(inputstr, iso_dt_format)
        except ValueError:
            date = dt.datetime.strptime(inputstr, iso_dt_format_with_ms)
            return date.strftime(nasa_dt_format_with_ms)
        else:
            return date.strftime(nasa_dt_format)
    else:
        return date.strftime(nasa_date_format)

# %% ../notebooks/api/01_utils.ipynb 23
def iso_to_nasa_datetime(
    dtimestr: str,  # Datetime string of the form yyyy-mm-ddTHH-MM-SS
):  # Datestring in NASA standard yyyy-jjjTHH-MM-SS
    "Convert iso datetime to day-number based NASA datetime."
    try:
        dtimestr.split(".")[1]
    except IndexError:
        source_format = iso_dt_format
        target_format = nasa_dt_format
    else:
        source_format = iso_dt_format_with_ms
        target_format = nasa_dt_format_with_ms
    date = dt.datetime.strptime(dtimestr, source_format)
    return date.strftime(target_format)

# %% ../notebooks/api/01_utils.ipynb 28
def replace_all_nasa_times(
    df: pd.DataFrame,  # DataFrame with NASA time columns
):
    """Find all NASA times in dataframe and replace with ISO.

    Changes will be implemented on incoming dataframe!

    This will be done for all columns with the word TIME in the column name.
    """
    for col in [col for col in df.columns if "TIME" in col]:
        if "T" in df[col].iloc[0]:
            df[col] = pd.to_datetime(df[col].map(nasa_time_to_iso))

# %% ../notebooks/api/01_utils.ipynb 30
def parse_http_date(
    text: str,  # datestring from urllib.request
) -> dt.datetime:  # dt.datetime object from given datetime string
    "Parse date string retrieved via urllib.request."
    return dt.datetime(*eut.parsedate(text)[:6])


def get_remote_timestamp(
    url: str,  # URL to check timestamp for
) -> dt.datetime:
    """Get the timestamp of a remote file.

    Useful for checking if there's an updated file available.
    """
    with urlopen(url, timeout=10) as conn:
        t = parse_http_date(conn.headers["last-modified"])
    return t


def check_url_exists(url):
    response = requests.head(url)
    if response.status_code < 400:
        return True
    else:
        return False


def url_retrieve(
    url: str,  # The URL to download
    outfile: str,  # The path where to store the downloaded file.
    # The size of the chunk for the request.iter_content call. Default: 128
    chunk_size: int = 128,
    user: str = None,  # if provided, create HTTPBasicAuth object
    passwd: str = None,  # if provided, create HTTPBasicAuth object
):
    """Improved urlretrieve with progressbar, timeout and chunker.

    This downloader has built-in progress bar using tqdm and using the `requests`
    package it improves standard `urllib` behavior by adding time-out capability.

    I tested different chunk_sizes and most of the time 128 was actually fastest, YMMV.

    Inspired by https://stackoverflow.com/a/61575758/680232
    """
    if user:
        auth = HTTPBasicAuth(user, passwd)
    else:
        auth = None
    R = requests.get(url, stream=True, allow_redirects=True, auth=auth)
    if R.status_code != 200:
        raise ConnectionError(f"Could not download {url}\nError code: {R.status_code}")
    with tqdm.wrapattr(
        open(outfile, "wb"),
        "write",
        miniters=1,
        total=int(R.headers.get("content-length", 0)),
        desc=str(Path(outfile).name) + "\n",
    ) as fd:
        for chunk in R.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def have_internet():
    """Fastest way to check for active internet connection.

    From https://stackoverflow.com/a/29854274/680232
    """
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

# %% ../notebooks/api/01_utils.ipynb 32
def height_from_shadow(
    shadow_in_pixels: float,  # Measured length of shadow in pixels
    sun_elev: float,  # Ange of sun over horizon in degrees
) -> float:  # Height [meter]
    """Calculate height of an object from its shadow length.

    Note, that your image might have been binned.
    You need to correct `shadow_in_pixels` for that.
    """
    return tan(radians(sun_elev)) * shadow_in_pixels


def get_gdal_center_coords(
    imgpath: Union[str, Path],  # Path to raster image that is readable by GDLA
) -> Tuple[int, int]:  # center row/col coordinates.
    """Get center rows/cols pixel coordinate for GDAL-readable dataset.

    Check CLI `gdalinfo --formats` to see all formats that GDAL can open.
    """
    if not GDAL_INSTALLED:
        logger.error("GDAL not installed. Returning")
        return
    ds = gdal.Open(str(imgpath))
    xmean = ds.RasterXSize // 2
    ymean = ds.RasterYSize // 2
    return xmean, ymean


def file_variations(
    filename: Union[str, Path],  # The original filename to use as a base.
    extensions: list,
) -> list:  # list of Paths
    """Create a variation of file names.

    Generate a list of variations on a filename by replacing the extension with
    the provided list.

    Adapted from T. Olsens `file_variations of the pysis module for using pathlib.
    """
    return [Path(filename).with_suffix(extension) for extension in extensions]

# %% ../notebooks/api/01_utils.ipynb 38
def catch_isis_error(func):
    """can be used as decorator for any ISIS function"""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ProcessError as err:
            print("Had ISIS error:")
            print(" ".join(err.cmd))
            print(err.stdout)
            print(err.stderr)

    return inner
