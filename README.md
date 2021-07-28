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
The `find_index` app is specifically useful when you don't know what index files exist.

So far, the following indexes are supported (but not necessarily all tested within PLPY):

* Cassini
  * ISS (all)
  * UVIS (all)
* MRO
  * CTX
      EDR
  * HiRISE
    * EDR, RDR, DTM
      * EDR index has a bug (as delivered by the team, reported), where I need to activate an existing fix for it.
* LRO
  * Diviner (DLRE)
    * EDR, RDR
  * LOLA
    * EDR, RDR
    
### More indexes
More indexes of other instruments can be easily added by following the existing structure of what has been copied into your config at `~/.planetarypy_config.yaml`.

Please consider submitting a pull request for adding further PDS index files into the config file at its source: https://github.com/michaelaye/nbplanetary/blob/master/planetarypy/data/planetarypy_config.yaml

## Utils
Find something in `Utils` for working with NASA timestamps and a well working URL download function `url_retrieve`, among other stuff.

## Experiment/Instrument Specific

So far, `planetarypy` supports CTX EDR and HiRISE RGB.NOMAP data.
Look at the `CTX` and `HiRISE` pages for descriptions of classes for working with these data.

## Bug reports

Please submit bug reports at https://github.com/michaelaye/nbplanetary/issues
