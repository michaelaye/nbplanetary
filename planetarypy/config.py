# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/00_config.ipynb (unless otherwise specified).

__all__ = ['Config', 'config']

# Cell
import os
import shutil
from functools import reduce
from importlib.resources import path as resource_path
from fastcore.utils import Path

import strictyaml as yaml

# Cell
class Config:
    """Manage config stuff.

    Attributes
    -------
    path: pathlib.Path

    The key, value pairs found in the config file become attributes of the
    class instance after initialization.
    At minimum, there should be the `storage_root` attribute for storing data
    for this package.
    """

    # This part enables a config path location override using env PYCISS_CONFIG
    fname = "planetarypy_config.yaml"
    # separating fname from fpath so that resource_path below is correct.
    path = Path(os.getenv("PLANETARYPY_CONFIG", Path.home() / f".{fname}"))

    def __init__(self, config_path=None):
        "Switch to other config file location with `config_path`."
        if config_path is not None:
            self.path = Path(config_path)
        if not self.path.exists():
            with resource_path("planetarypy.data", self.fname) as p:
                shutil.copy(p, self.path)
        self.read_config()

    def read_config(self):
        """Read the configfile and store config dict.

        If found, load config via `yaml` and store YAML dict as `d`.
        `storage_root` will be stored as attribute.
        """
        self.yamldic = yaml.load(self.path.read_text())
        if not self.yamldic["storage_root"].data:
            self.ask_storage_root()
        else:
            self.storage_root = Path(self.yamldic["storage_root"].data)

    @property
    def d(self):
        "get the Python dic from YAML dict."
        return self.yamldic.data

    def get_value(self, key):
        """Get sub-dictionary by nested key.

        Parameters
        ----------
        nested_key: str
            A nested key in dotted format, e.g. cassini.uvis.indexes
        """
        return reduce(lambda c, k: c[k], key.split("."), self.d)

    def set_value(self, nested_key, value, save=True):
        """Set sub-dic using dotted key.

        Parameters
        ----------
        key: str
            A nested key in dotted format, e.g. cassini.uvis.ring_summary
        value: convertable to string
            Value for the given key to be stored.
        """
        dic = self.yamldic
        keys = nested_key.split(".")
        for key in keys[:-1]:
            dic = dic[key]
        dic[keys[-1]] = value
        if save:
            self.save()

    def save(self):
        "Write the YAML dict to file."
        self.path.write_text(self.yamldic.as_yaml())

    def ask_storage_root(self):
        """Use input() to ask user for the storage_root path.

        The path will be stored in the YAML-dict and saved into existing config file
        at `Class.path`, either default or as given during init.
        `storage_root` attribute is set as well.
        """
        path = input(
            "Provide the root storage path where all downloaded and produced data will be stored:"
        )
        self.yamldic["storage_root"] = path
        self.storage_root = Path(path)
        self.save()

    def list_missions(self):
        return list(self.d["missions"].keys())

    def list_instruments(self, mission):
        if not mission.startswith("missions"):
            mission = "missions." + mission
        instruments = self.get_value(mission)
        return list(instruments.keys())

    def list_indexes(self, instrument):
        "instrument key needs to be <mission>.<instrument>"
        if not instrument.startswith("missions"):
            instrument = "missions." + instrument
        indexes = self.get_value(instrument + ".indexes")
        return list(indexes)

    def get_clean_copy(self, new_path):
        "Create a clean copy without timestamps for repo upload."
        dic = self.yamldic.copy()
        missions = dic['missions']
        for mission in missions.keys():
            mdict = missions[mission]
            for instr in mdict.keys():
                instrdict = mdict[instr]
                for index in instrdict['indexes']:
                    instrdict['indexes'][index]['timestamp']=''
        Path(new_path).write_text(dic.as_yaml())
        return Config(config_path=new_path)

# Cell
config = Config()