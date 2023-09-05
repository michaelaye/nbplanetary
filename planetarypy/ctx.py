# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/api/03_ctx.ipynb.

# %% auto 0
__all__ = ['baseurl', 'storage_root', 'cache', 'get_edr_index', 'CTXEDR', 'CTX', 'CTXCollection', 'ctx_calib']

# %% ../notebooks/api/03_ctx.ipynb 3
import warnings
from itertools import repeat
from multiprocessing import Pool
from pathlib import Path

import rasterio
import rioxarray as rxr
from tqdm.auto import tqdm
from tqdm.contrib.concurrent import process_map
from yarl import URL

import hvplot.xarray  # noqa
from fastcore.basics import store_attr
from fastcore.script import call_parse
from .config import config
from .pds.apps import get_index
from .utils import catch_isis_error, file_variations, url_retrieve

try:
    from kalasiris.pysis import (
        ProcessError,
        ctxcal,
        ctxevenodd,
        getkey,
        mroctx2isis,
        spiceinit,
        cam2map,
    )
except KeyError:
    warnings.warn("kalasiris has a problem initializing ISIS")

# %% ../notebooks/api/03_ctx.ipynb 4
warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)
baseurl = URL(config.get_value("mro.ctx.datalevels.edr.url"))

# %% ../notebooks/api/03_ctx.ipynb 5
storage_root = config.storage_root / "missions/mro/ctx"
cache = dict()

# %% ../notebooks/api/03_ctx.ipynb 7
def get_edr_index(refresh=False):
    if 'edrindex' in cache:
        return cache['edrindex']
    else:
        edrindex = get_index("mro.ctx", "edr", refresh=refresh)
        edrindex["short_pid"] = edrindex.PRODUCT_ID.map(lambda x: x[:15])
        edrindex["month_col"] = edrindex.PRODUCT_ID.map(lambda x: x[:3])
        edrindex.LINE_SAMPLES = edrindex.LINE_SAMPLES.astype(int)
        cache['edrindex'] = edrindex
        return edrindex

# %% ../notebooks/api/03_ctx.ipynb 8
class CTXEDR:
    """Manage access to EDR data"""

    root = config.get_value("mro.ctx.datalevels.edr.root") or storage_root / "edr"
    with_pid_folder = config.get_value("mro.ctx.datalevels.edr.with_pid_folder")
    with_volume = config.get_value("mro.ctx.datalevels.edr.with_volume")

    def __init__(
            self,
            pid: str,  # CTX product id (pid)
            root: str = "",  # alternative root folder for EDR data
            with_volume=None,  # does the storage path include the volume folder
            with_pid_folder=None,  # control if stuff is stored inside PID folders
            refresh_index=False
    ):
        self.pid = pid
        self.root = Path(root) if root else Path(self.root)
        self.with_volume = with_volume if with_volume is not None else self.with_volume
        self.with_pid_folder = (with_pid_folder if with_pid_folder is not None else self.with_pid_folder)
        self.refresh_index = refresh_index
        self.edrindex = None

    @property
    def pid(self):
        "Return product_id"
        return self._pid

    @pid.setter
    def pid(self, value):
        if len(value) == 15:
            self.edrindex = get_edr_index()
            value = self.edrindex.query(f"short_pid=='{value}'").PRODUCT_ID.iloc[0]
        self._pid = value

    @property
    def short_pid(self):
        return self.pid[:15]

    @property
    def meta(self):
        "get the metadata from the index table"
        edrindex = get_edr_index(refresh=self.refresh_index)
        s = edrindex.query("PRODUCT_ID == @self.pid").squeeze()
        s.index = s.index.str.lower()
        return s

    @property
    def volume(self):
        "get the PDS volume number for the current product id"
        return self.meta.volume_id.lower()

    @property
    def source_folder(self):
        """Calculate the source folder based on storage options `with_pid_folder` and `with_volume`."""
        base = self.root
        if self.with_volume:
            base = self.root / self.volume
        if self.with_pid_folder:
            base = base / self.pid
        return base

    @property
    def source_path(self):
        """Combine `source_folder` with `pid` into full path."""
        return self.source_folder / f"{self.pid}.IMG"

    @property
    def url(self):
        "Calculate URL from input dataframe row."
        url = baseurl / self.meta.volume_id.lower() / "data" / (self.pid + ".IMG")
        return url

    def download(self, overwrite=False):  # use `overwrite` to download in all cases.
        "Download and store correctly the EDR data, if not locally available."
        if self.source_path.exists() and not overwrite:
            print("File exists. Use `overwrite=True` to download fresh.")
            return
        self.source_folder.mkdir(parents=True, exist_ok=True)
        url_retrieve(self.url, self.source_path)

    def __str__(self):
        "Show some info about yourself when returned in a REPL (like ipython/jupyter)."
        s = f"PRODUCT_ID: {self.pid}\n"
        s += f"URL: {self.url}\n"
        s += f"source_path: {self.source_path}\n"
        return s

    def __repr__(self):
        return self.__str__()

# %% ../notebooks/api/03_ctx.ipynb 30
class CTX:
    """Class to manage dealing with CTX data.

    HAS a CTXEDR attribute as defined above.
    Attributes from CTXEDR are availalbe via __getattr__()
    """
    proc_root = storage_root / "edr"
    preproc_root = Path(config.get_value("mro.ctx.preproc_root"))
    preproc_calib_extension = config.get_value("mro.ctx.calib_extension")
    preproc_with_pid_folder = config.get_value("mro.ctx.preproc_with_pid_folder")
    preproc_with_volume = config.get_value("mro.ctx.preproc_with_volume")
    proc_with_pid_folder = config.get_value("mro.ctx.proc_with_pid_folder")
    proc_with_volume = config.get_value("mro.ctx.proc_with_volume")

    def __init__(
            self,
            id_: str,  # CTX product id
            source_dir: str = "",  # where the raw EDR data is stored, if not coming from plpy
            proc_root: str = "",  # where to store processed, if not plpy
            with_volume=None,  # store with extra volume subfolder?
            with_pid_folder=None,  # store with extra product_id subfolder?
    ):
        self.edr = CTXEDR(id_, root=source_dir, with_volume=with_volume)
        self.proc_root = Path(proc_root) if proc_root else self.proc_root
        self.with_volume = with_volume if with_volume else self.proc_with_volume
        self.with_pid_folder = with_pid_folder if with_pid_folder else self.proc_with_pid_folder
        (self.cub_name, self.cal_name,
         self.destripe_name, self.map_name) = file_variations(self.edr.source_path.name,
                                               [".cub", ".cal.cub", ".dst.cal.cub", ".lev2.cub"])

        # status flags for caching
        self.is_read = False
        self.is_calib_read = False
        self.checked_destripe = False

    def __getattr__(self, attr):
        return getattr(self.edr, attr)

    @property
    def proc_folder(self) -> Path:
        "the folder for foreign processed data, like pre-processed calibrated data, e.g."
        path = self.proc_root
        if self.proc_with_volume:
            path = path / self.volume
        if self.proc_with_pid_folder:
            path = path / self.pid
        return path

    @property
    def preproc_folder(self) -> Path:
        "the folder for foreign processed data, like pre-processed calibrated data, e.g."
        path = self.preproc_root
        if self.preproc_with_volume:
            path = path / self.volume
        if self.preproc_with_pid_folder:
            path = path / self.pid
        return path

    @property
    def cub_path(self) -> Path:
        "Path to cube after import to ISIS."
        return self.proc_folder / self.cub_name

    @property
    def cal_path(self) -> Path:
        "Path to calibrated cube file. Also destriped files get this name."
        return self.proc_folder / self.cal_name

    @property
    def preproc_cal_path(self) -> Path:
        "Path to a preprocessend calibrated file"
        cal_name = file_variations(self.edr.source_path.name, [self.preproc_calib_extension])[0]
        return self.preproc_folder / cal_name

    @property
    def destripe_path(self) -> Path:
        "One can keep destriped cubes as extra files, but it increases path management complexity."
        return self.proc_folder / self.destripe_name

    @property
    def map_path(self) -> Path:
        return self.proc_folder / self.map_name

    @catch_isis_error
    def isis_import(self) -> None:
        "Import EDR data into ISIS cube."
        self.cub_path.parent.mkdir(exist_ok=True, parents=True)
        mroctx2isis(from_=self.source_path, to=self.cub_path)

    @catch_isis_error
    def spice_init(self, web="yes") -> None:
        "Perform `spiceinit.`"
        spiceinit(from_=self.cub_path, web=web)

    @catch_isis_error
    def calibrate(self) -> None:
        "Do ISIS `ctxcal`."
        ctxcal(from_=self.cub_path, to=self.cal_path)
        self.is_calib_read = False

    @catch_isis_error
    def destripe(self, do_rename=True) -> None:
        "Do destriping via `ctxevenodd` if allowed by summing status."
        if self.spatial_summing != 2:
            ctxevenodd(from_=self.cal_path, to=self.destripe_path)
            if do_rename:
                self.destripe_path.rename(self.cal_path)

    @catch_isis_error
    def map_project(self, mpp=6.25) -> None:
        "Perform map projection."        
        cam2map(from_=self.cal_path, to=self.map_path, pixres='mpp', resolution=mpp)

    @property
    def spatial_summing(self) -> int:
        "Get the spatial summing value from the index file."
        return self.meta["spatial_summing"]

    @property
    def data_quality(self) -> str:
        "Return the index file content for the DATA_QUALITY_DESC flag."
        return self.meta.data_quality_desc

    def calib_pipeline(self, overwrite=False) -> None:
        "Execute the whole ISIS pipeline for CTX EDR data."
        if self.cal_path.exists() and not overwrite:
            return
        pbar = tqdm("isis_import spice_init calibrate destripe".split())
        for name in pbar:
            pbar.set_description(name)
            getattr(self, name)()
        pbar.set_description("Done.")

    @property
    def edr_da(self):
        """Read EDR into xr.DataArray. Drop superfluous band dimension.

        If it was read before, use stored object for speed-up.
        'da' stands for data-array.
        """
        if not self.is_read:
            if not self.source_path.exists():
                # Doing this by hand because rasterio doesn't throw exception when path is missing.
                raise FileNotFoundError("EDR not downloaded yet.")
            self._edr_da = rxr.open_rasterio(self.source_path).sel(band=1, drop=True)
            self._edr_da.name = f"{self.short_pid} EDR"
            self.is_read = True
        return self._edr_da.drop_vars("spatial_ref")

    @property
    def edr_shape(self):
        return self.edr_da.shape

    @property
    def cal_da(self):
        """Read calibrated ISIS cube into xarray.DataArray using rioxarray.

        Drop superfluous `band` dimension.
        If it was read before, use stored object for speed-up.
        'da' stands for data-array.
        """
        if not self.is_calib_read:
            self._cal_da = rxr.open_rasterio(self.cal_path, masked=True).sel(band=1, drop=True)
            self._cal_da.name = f"{self.short_pid} calibrated"
            self.is_calibd_read = True
        return self._cal_da.drop_vars("spatial_ref")

    @property
    def cal_shape(self):
        return self.cal_da.shape

    def plot_da(self, data):
        """Use hvplot to plot the xarray. Used by plot_calibrated to plot the calibrated array."""
        return data.hvplot(
            x="y",
            y="x",
            rasterize=True,
            cmap="gray",
            width=1000,
            height=400,
            title=self.pid[:15],
        )

    def plot_edr(self):
        "Plot EDR xarray using hvplot."
        return self.plot_da(self.edr_da)

    def plot_calibrated(self):
        "Plot the calibrated xarray using hvplot."
        return self.plot_da(self.cal_da)

    def __str__(self):
        "Print out some infos about yourself."
        s = self.edr.__str__()
        try:
            s += f"Shape: {self.edr_da.shape}"
        except FileNotFoundError:
            s += f"Not downloaded yet."
        return s

    def __repr__(self):
        return self.__str__()

# %% ../notebooks/api/03_ctx.ipynb 60
class CTXCollection:
    """Class with several helpful methods to work with a set of CTX images.

    We identify the images via a list of product_ids.
    Several methods manipulate this list based on the requested constraint.
    """

    @classmethod
    def by_volume(cls, vol_id, **kwargs):
        """Create a CTXCollection from the PDS volume number."""
        if not str(vol_id).startswith("MROX_"):
            vol_id = "MROX_" + str(vol_id)
        query = f"VOLUME_ID=='{vol_id}'"
        edrindex = get_edr_index()
        return cls(edrindex.query(query).PRODUCT_ID.values, edrindex=edrindex, **kwargs)

    @classmethod
    def by_month(cls, month_letters, nth_volume=None, **kwargs):
        """Create a CTXCollection based on the first 3 letters of the product_id (a.k.a. "month")"""
        edrindex = get_edr_index()
        df = edrindex[edrindex.PRODUCT_ID.str.startswith(month_letters)]
        obj = cls(df.PRODUCT_ID.values, **kwargs)
        if nth_volume is not None:
            return cls.by_volume(obj.volumes_in_pids[nth_volume], edrindex=edrindex, **kwargs)
        else:
            return obj

    @classmethod
    def volume_from_pid(cls, pid, **kwargs):
        """Get a CTXCollection of the volume for a given image (product_id)."""
        edrindex = get_edr_index()
        vol = edrindex.query(f"PRODUCT_ID=='{pid}'").VOLUME_ID.iat[0]
        return cls.by_volume(vol, **kwargs)

    def __init__(self, product_ids, full_width=False, filter_error=False, edrindex=None):
        self.product_ids = product_ids
        self.full_width = full_width  # i.e. LINE_SAMPLES==5056
        self.filter_error = filter_error
        self.edrindex = get_edr_index() if edrindex is None else edrindex

    @property
    def pids(self):
        "Alias on product_id"
        return self.product_ids

    @property
    def product_ids(self):
        new_pids = self._product_ids
        ind = self.edrindex[self.edrindex.PRODUCT_ID.isin(new_pids)]
        queries = []
        if self.full_width:
            queries.append('LINE_SAMPLES == 5056')
            # new_pids = [pid for pid in new_pids if CTX(pid).meta.line_samples == 5056]
        if self.filter_error:
            queries.append("DATA_QUALITY_DESC != 'ERROR'")
            # new_pids = [pid for pid in new_pids if CTX(pid).data_quality != 'ERROR']
        if queries:
            return ind.query(" and ".join(queries)).PRODUCT_ID.values
        else:
            return ind.PRODUCT_ID.values

    @product_ids.setter
    def product_ids(self, val):
        self._product_ids = val

    def get_urls(self):
        """Get URLs for list of product_ids.

        Returns
        -------
        List[yarl.URL]
            List of URL objects with the respective PDS URL for download.
        """
        urls = []
        for p_id in self.product_ids:
            ctx = CTXEDR(p_id)
            urls.append(ctx.url)
        self.urls = urls
        return urls

    def _do_download(self, args):
        pid, overwrite = args
        ctx = CTX(pid)
        ctx.download(overwrite=overwrite)

    def download_collection(self, overwrite=False):
        "download the images in parallel using tqdm wrapper around concurrent.future"
        print("Downloading collection...")
        args = zip(self.product_ids, repeat(overwrite))
        r = process_map(self._do_download, args, max_workers=6)

    def _do_calib(self, args):
        pid, overwrite = args
        ctx = CTX(pid)
        ctx.calib_pipeline(overwrite=overwrite)

    def calibrate_collection(self, overwrite=False):
        "Calibrate all images in collection using tqdm wrapper around concurrent.future"
        print("Launching parallel calibration...")
        args = zip(self.product_ids, repeat(overwrite))
        process_map(self._do_calib, args, max_workers=6)

    def edr_exist_check(self):
        "Check if all source_paths exists, i.e. all EDR images are available."
        return [(p_id, CTX(p_id).source_path.exists()) for p_id in self.product_ids]

    def calib_exist_check(self):
        "Check if all cal_paths exist. (i.e. all calibrated ISIS cubes are available."
        return [(p_id, CTX(p_id).cal_path.exists()) for p_id in self.product_ids]

    def only_full_width(self):
        "Constrain the list of product_ids to those that have full width (i.e. line_samples == 5056)"

    def get_ctx_n(self, n):
        "Get CTX object for n-th product_id"
        return CTX(self.product_ids[n])

    def get_pid_n(self, n):
        "Get pid for n-th entry in product_ids."
        return self.product_ids[n]

    @property
    def n_items(self):
        "Return length of product_ids list."
        return len(self.pids)

    @property
    def meta(self):
        "Return the index file filtered for the given product_ids."
        return self.edrindex[self.edrindex.PRODUCT_ID.isin(self.pids)]

    @property
    def image_times(self):
        "Return the image observation times."
        return self.meta.IMAGE_TIME

    def get_corrupted(self):
        "Return the product_ids where the PDS index file has an 'ERROR' flag for the `DATA_QUALITY_DESC` field."
        return [pid for pid in self.pids if CTX(pid).data_quality == "ERROR"]

    def filter_error(self):
        "Filter the product_ids for the error flag from the PDS index."
        self.product_ids = [pid for pid in self.pids if CTX(pid).data_quality != "ERROR"]

    @property
    def volumes_in_pids(self):
        return self.edrindex[self.edrindex.PRODUCT_ID.isin(self.product_ids)].VOLUME_ID.unique()

    @property
    def count_per_volume(self):
        g = self.edrindex.groupby("VOLUME_ID")
        return g.size()[self.volumes_in_pids]

    def sample(self, n):
        "Return random sample of product_ids, size `n`."
        return list(pd.Series(self.product_ids).sample(n))

    def __str__(self):
        s = f"# of product IDs: {self.n_items}\n"
        s += "Volumes contained in list of product_ids:\n"
        s += f"{self.volumes_in_pids}\n"
        return s

    def __repr__(self):
        return self.__str__()

# %% ../notebooks/api/03_ctx.ipynb 103
@call_parse
def ctx_calib(
        pid: str,  # CTX product_id
        source: str = "",  # path to where EDRs are stored if not from plpy
        proc_root: str = "",  # path to where processed data is to be stored
        overwrite: bool = False,  # overwrite processed data
):
    ctx = CTX(pid, source_dir=source, proc_root=proc_root)
    ctx.calib_pipeline(overwrite=overwrite)
    print("Produced\n", ctx.cal_path)
