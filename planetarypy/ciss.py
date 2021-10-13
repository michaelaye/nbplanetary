# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/06_cassini_iss.ipynb (unless otherwise specified).

__all__ = ['storage_root', 'opus_keys', 'ISSOpus']

# Cell
from .pds.opusapi import OPUS
from .utils import url_retrieve, have_internet
from .config import config
from fastcore.utils import Path
from yarl import URL

# Cell
storage_root = config.storage_root / "missions/cassini/iss"
opus_keys = [
    "coiss_raw",
    "coiss_calib",
    "coiss_thumb",
    "coiss_medium",
    "coiss_full",
    "rms_index",
    "inventory",
    "planet_geometry",
    "ring_geometry",
    "browse_thumb",
    "browse_small",
    "browse_medium",
    "browse_full",
]

# Cell


class ISSOpus:
    def __init__(self, pid):
        self.pid = pid
        if have_internet():
            self.query_pid(pid)

    def query_pid(self, pid):
        opus = OPUS()
        self.query_result = opus.query_image_id(pid)[0]
        self.id = self.query_result[0]
        self.dict = self.query_result[1]
        for k, v in self.dict.items():
            if isinstance(v, list) and len(v) == 1:
                setattr(self, k, v[0])
            else:
                setattr(self, k, v)

    @property
    def raw_data_url(self):
        return URL(self.coiss_raw[0])

    @property
    def raw_label_url(self):
        return URL(self.coiss_raw[1])

    @property
    def raw_prefix_fmt_url(self):
        return URL(self.coiss_raw[2])

    @property
    def raw_tlmtab_url(self):
        return URL(self.coiss_raw[3])

    @property
    def calib_data_url(self):
        return URL(self.coiss_calib[0])

    @property
    def calib_label_url(self):
        return URL(self.coiss_calib[1])

    @property
    def volume(self):
        return self.raw_data_url.parts[4]

    @property
    def local_folder(self):
        return storage_root / self.pid.upper()

    @property
    def local_data_path(self):
        return self.local_folder / self.raw_data_url.name

    @property
    def local_calib_path(self):
        return self.local_folder / self.calib_data_url.name

    @property
    def local_label_path(self):
        return self.local_data_path.with_suffix(".LBL")

    @property
    def local_calib_label_path(self):
        return self.local_calib_path.with_suffix(".LBL")

    def download_raw(self, overwrite=False):
        self.local_data_path.parent.mkdir(parents=True, exist_ok=True)
        if self.local_data_path.exists() and not overwrite:
            print("File exists. Use `overwrite=True` to download fresh.")
            return
        url_retrieve(self.raw_data_url, self.local_data_path)
        url_retrieve(self.raw_label_url, self.local_label_path)

    def download_calib(self):
        self.local_calib_path.parent.mkdir(parents=True, exist_ok=True)
        url_retrieve(self.calib_data_url, self.local_calib_path)

    def __repr__(self):
        s = f"Product ID:\n{self.id}\n\n"
        for k, v in self.query_result[1].items():
            s += f"Key: {k},\nValue(s):\n{v}\n\n"
        return s