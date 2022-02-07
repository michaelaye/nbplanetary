# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/10_spice.kernels.ipynb (unless otherwise specified).

__all__ = ['kernel_storage', 'dataset_ids', 'df', 'df2', 'df2', 'df2', 'df', 'datasets', 'base_url', 'Subsetter']

# Cell
import zipfile
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests
from fastcore.utils import store_attr
from tqdm.auto import tqdm
from yarl import URL

from ..config import config
from ..utils import url_retrieve

# Cell
kernel_storage = config.storage_root / "spice_kernels"
kernel_storage.mkdir(exist_ok=True, parents=True)

# Cell
dataset_ids = {
    "cassini": "co-s_j_e_v-spice-6-v1.0/cosp_1000",
    "clementine": "clem1-l-spice-6-v1.0/clsp_1000",
    "dawn": "dawn-m_a-spice-6-v1.0/dawnsp_1000",
    "di": "di-c-spice-6-v1.0/disp_1000",
    "ds1": "ds1-a_c-spice-6-v1.0/ds1sp_1000",
    "epoxi": "dif-c_e_x-spice-6-v1.0/epxsp_1000",
    "em16": "em16/em16_spice",
    "grail": "grail-l-spice-6-v1.0/grlsp_1000",
    "hayabusa": "hay-a-spice-6-v1.0/haysp_1000",
    "insight": "insight/insight_spice",
    "juno": "jno-j_e_ss-spice-6-v1.0/jnosp_1000",
    "ladee": "ladee/ladee_spice",
    "lro": "lro-l-spice-6-v1.0/lrosp_1000",
    "maven": "maven/maven_spice",
    "opportunity": "mer1-m-spice-6-v1.0/mer1sp_1000",
    "spirit": "mer2-m-spice-6-v1.0/mer2sp_1000",
    "messenger": "mess-e_v_h-spice-6-v1.0/messsp_1000",
    "mars2020": "mars2020/mars2020_spice",
    "mex": "mex-e_m-spice-6-v2.0/mexsp_2000",
    "mgs": "mgs-m-spice-6-v1.0/mgsp_1000",
    "ody": "ody-m-spice-6-v1.0/odsp_1000",
    "mro": "mro-m-spice-6-v1.0/mrosp_1000",
    "msl": "msl-m-spice-6-v1.0/mslsp_1000",
    "near": "near-a-spice-6-v1.0/nearsp_1000",
    "nh": "nh-j_p_ss-spice-6-v1.0/nhsp_1000",
    "orex": "orex/orex_spice",
    "rosetta": "ro_rl-e_m_a_c-spice-6-v1.0/rossp_1000",
    "stardust": "sdu-c-spice-6-v1.0/sdsp_1000",
    "venus_climate_orbiter": "vco-v-spice-6-v1.0/vcosp_1000",
    "vex": "vex-e_v-spice-6-v2.0/vexsp_2000",
    "vo": "vo1_vo2-m-spice-6-v1.0/vosp_1000",
}

df = pd.DataFrame({"shorthand": dataset_ids.keys(), "path": dataset_ids.values()})

df2 = pd.read_html("http://naif.jpl.nasa.gov/naif/data_archived.html")[6]
df2.columns = df2.iloc[0]
df2 = df2.drop(0).reset_index(drop=True)
df2 = df2.drop(["Archive Readme", "Archive Link", "Subset Link"], axis=1)
df = df.join(df2)
datasets = df.set_index("shorthand")

# Cell
base_url = URL("https://naif.jpl.nasa.gov/cgi-bin/subsetds.pl")

# Cell
class Subsetter:
    """Class to manage retrieving subset SPICE kernel lists

    Attributes
    ----------
    kernel_names: List of
    """

    def __init__(self, mission, start, stop):
        store_attr()
        payload = {
            "dataset": dataset_ids[mission],
            "start": start,
            "stop": stop,
            "action": "Subset",
        }
        r = requests.get(base_url, params=payload, stream=True)
        if r.ok:
            z = zipfile.ZipFile(BytesIO(r.content))
        else:
            raise IOError("SPICE Server request returned status code: {r.status_code}")
        self.z = z
        self.urls_file = [name for name in z.namelist() if name.startswith("urls_")][0]
        self.metakernel_file = [name for name in z.namelist() if name.endswith(".tm")][
            0
        ]
        with self.z.open(self.urls_file) as f:
            self.kernel_urls = f.read().decode().split()

    @property
    def kernel_names(self):
        return [Path(URL(url).parent.name) / URL(url).name for url in self.kernel_urls]

    def download_kernels(self, overwrite=False):
        for url in tqdm(self.kernel_urls, desc="Kernels downloaded"):
            u = URL(url)
            local_path = kernel_storage / self.mission / u.parent.name / u.name
            if local_path.exists() and not overwrite:
                print(local_path.parent.name, local_path.name, "locally available.")
                continue
            local_path.parent.mkdir(exist_ok=True, parents=True)
            url_retrieve(url, local_path)

    def get_metakernel(self):
        savepath = kernel_storage / self.mission / self.metakernel_file
        with open(savepath, "w") as outfile, self.z.open(
            self.metakernel_file
        ) as infile:
            for line in infile:
                linestr = line.decode()
                if "'./data'" in linestr:
                    linestr = linestr.replace("'./data'", f"'{savepath.parent}'")
                outfile.write(linestr)
        return savepath