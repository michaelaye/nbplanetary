# AUTOGENERATED! DO NOT EDIT! File to edit: 00_config.ipynb (unless otherwise specified).

__all__ = ['Config', 'config']

# Cell
import os
import toml
from pathlib import Path

# Cell
class Config:
    """Manage config stuff.

    Attributes
    -------
    path: pathlib.Path

    The key, value pairs found in the config file become attributes of the
    class instance after initialization.
    At minimum, there should be the `archive_path` attribute for storing data
    for this package.
    """
    # This enables a config path location override using env PYCISS_CONFIG
    path = Path(os.getenv("PLANETARYPY_CONFIG", Path.home() / '.planetarypy.toml'))

    def __init__(self, other_config=None):
        "Switch to other config file location with `other_config`."
        if other_config is not None:
            self.path = Path(other_config)
        self.get_config()

    def get_config(self):
        "Read the configfile and store config dict."
        p = self.path
        if not p.exists():
            self.not_found()
        else:
            with open(p) as f:
                self.d = toml.load(f)
                if not self.d:
                    self.not_found()
                # all found key.value pairs become attributes
                for k, v in self.d.items():
                    setattr(self, k, v)

    def not_found(self):
        """Use input to ask user for the archive_path.

        The path will be stored in the config file `Class.path` (either default or as given
        during init.)
        """
        path = input("Provide path where all package data will be stored:")
        d = {}
        d["archive_path"] = path
        self.archive_path = path
        with self.path.open("w") as f:
            toml.dump(d, f)

# Cell
config = Config()