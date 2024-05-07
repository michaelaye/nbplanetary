# AUTOGENERATED! DO NOT EDIT! File to edit: ../../notebooks/api/02g_pds.crism_index.ipynb.

# %% auto 0
__all__ = ['MTRDRIndex']

# %% ../../notebooks/api/02g_pds.crism_index.ipynb 2
from yarl import URL
from .indexes import Index

# %% ../../notebooks/api/02g_pds.crism_index.ipynb 4
class MTRDRIndex(Index):
    def __init__(self, url):
        super().__init__(key='mro.crism.mtrdr', url=url)