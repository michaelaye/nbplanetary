# PlanetaryPy
> This will become (part of) the core package of the <a href='https://planetarypy.org/'>PlanetaryPy</a> organisation.


## Current focus

* Enable finding PDS data by downloading and managing PDS3 index files
  * Conversion of these index files to `pandas.DataFrames` for search and filtering
* Downloading and local management of PDS3 data as identified via the index files or directly via data/product IDs.
* CTX and HiRISE specific tools

## Install

`pip install planetarypy`

This will pull in these other dependencies and their dependencies:

`strictyaml pandas pvl numpy python-dateutil tqdm lxml yarl hirise-tools kalasiris`


## PDS tools

Look at the `Apps` docs to see what `pds.apps` exist for easily getting PDS indexes.

## Utils
Find something in `Utils` for working with NASA timestamps and a well working URL download function `url_retrieve`, among other stuff.

## Experiment/Instrument Specific

So war, `planetarypy` supports CTX EDR and HiRISE RGB.NOMAP data.
Look at the `CTX` and `HiRISE` pages for descriptions of classes for working with these data.
