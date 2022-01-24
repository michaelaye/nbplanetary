# PlanetaryPy
> Beta release: This will become (part of) the core package of the <a href='https://planetarypy.org/'>PlanetaryPy</a> organisation.


Potential logo:![image.png](images/epilup_with_python_logo_with_axis.png)

## Install

```bash
pip install planetarypy
```

This will pull in these other dependencies and their dependencies:

`tomlkit pandas pvl numpy python-dateutil tqdm lxml yarl hirise-tools kalasiris`


## Suggested standard abbreviations: 
* Inside these docs the package will be called `PLPY` for brevity.
* A standard Python import could be: `plp` or `plpy`
  * because the last `p` in `plp` can be pronounced out, we consider these equivalent for human conversation and pronounce these "plippy".

## General scope

First and foremost this package should provide support in working with planetary science data.

With `working` we mean:

* locating
* retrieving
* reading
* further processing

of data.

### Locating
This library manages, via its `PDS tools`, multiple PDS3 index files per instrument that can be used for identifying data of interest.
These index files are automatically downloaded and converted to the very performant (and cloud-ready) [parquet](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_parquet.html) file format.
> Parquet is able to store advanced datatypes like nan-capable integer and full datetime objects, as opposed to HDF5.

### Retrieving

The interface to getting data is via a path-retrieving function based on a PDS product-id.
If that product-id is available locally, the path will be returned.
If it is not, it will previously be downloaded, stored in a systematic fashion organized by mission and instrument, and then the local path will be returned.

### Reading
For now, the library only returns the path to the object and the user needs to sort out the reading process.
A recently funded NASA project `Planetary Data Reader` will be integrated here, so that basic reading into memory can be provided.

As such, we anticipate two classes of reading support:1. basic reading into numpy and/or xarray1. added reader functionality like basic plots and basic geospatial processing, as supported by interested parties

There will exist larger other packages that focus on working with a given instrument's data, in which case that package could become an affiliated package with the `planetarypy` GitHub organization, if so desired.

### Further processing
In the future, additional frequently used procedures will be added to this library, e.g.
* frequently used GDAL/rasterio procedures
* frequently used SPICE operations
  * like surface illumination on a given body

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
More indexes of other instruments can be easily added by following the existing structure of what has been copied into your config at `~/.planetarypy_config.toml`.

Please consider submitting a pull request for adding further PDS index files into the config file at its source: https://github.com/michaelaye/nbplanetary/blob/master/planetarypy/data/planetarypy_config.toml

## Utils
Find something in `Utils` for working with NASA timestamps and a well working URL download function `url_retrieve`, among other stuff.

## Experiment/Instrument Specific

So far, `planetarypy` supports CTX EDR and HiRISE RGB.NOMAP data.
Look at the `CTX` and `HiRISE` pages for descriptions of classes for working with these data.

## Bug reports

Please submit bug reports at https://github.com/michaelaye/nbplanetary/issues

## How to use

### Indexes

See [PDS apps](02c_pds.apps.ipynb) for more details.

```python
from planetarypy.pds.apps import get_index
```

```python
ctrindex = get_index("mro.ctx", "edr")
ctrindex.sample(5, random_state=42)  # setting random_state to always get same files for docs
```

    Stored index is up-to-date.





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>VOLUME_ID</th>
      <th>FILE_SPECIFICATION_NAME</th>
      <th>ORIGINAL_PRODUCT_ID</th>
      <th>PRODUCT_ID</th>
      <th>IMAGE_TIME</th>
      <th>INSTRUMENT_ID</th>
      <th>INSTRUMENT_MODE_ID</th>
      <th>LINE_SAMPLES</th>
      <th>LINES</th>
      <th>SPATIAL_SUMMING</th>
      <th>...</th>
      <th>SUB_SOLAR_LATITUDE</th>
      <th>SUB_SPACECRAFT_LONGITUDE</th>
      <th>SUB_SPACECRAFT_LATITUDE</th>
      <th>SOLAR_DISTANCE</th>
      <th>SOLAR_LONGITUDE</th>
      <th>LOCAL_TIME</th>
      <th>IMAGE_SKEW_ANGLE</th>
      <th>RATIONALE_DESC</th>
      <th>DATA_QUALITY_DESC</th>
      <th>ORBIT_NUMBER</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>26491</th>
      <td>MROX_0964</td>
      <td>DATA/B17_016473_1740_XN_06S018W.IMG</td>
      <td>4A_04_1050062800</td>
      <td>B17_016473_1740_XN_06S018W</td>
      <td>2010-01-31 02:01:44.947</td>
      <td>CTX</td>
      <td>NIFL</td>
      <td>5056</td>
      <td>52224</td>
      <td>1</td>
      <td>...</td>
      <td>17.77</td>
      <td>16.8</td>
      <td>-5.91</td>
      <td>246673937.3</td>
      <td>45.19</td>
      <td>14.83</td>
      <td>89.6</td>
      <td>Ride-along with HiRISE</td>
      <td>OK</td>
      <td>16473</td>
    </tr>
    <tr>
      <th>63218</th>
      <td>MROX_2077</td>
      <td>DATA/F01_036289_1668_XN_13S296W.IMG</td>
      <td>4A_04_10B603B000</td>
      <td>F01_036289_1668_XN_13S296W</td>
      <td>2014-04-24 04:14:02.581</td>
      <td>CTX</td>
      <td>NIFL</td>
      <td>5056</td>
      <td>9216</td>
      <td>1</td>
      <td>...</td>
      <td>21.67</td>
      <td>296.3</td>
      <td>-13.17</td>
      <td>240471585.2</td>
      <td>120.81</td>
      <td>15.5</td>
      <td>90.2</td>
      <td>Ride-along with HiRISE</td>
      <td>OK</td>
      <td>36289</td>
    </tr>
    <tr>
      <th>108231</th>
      <td>MROX_3472</td>
      <td>DATA/K15_059422_2018_XN_21N035W.IMG</td>
      <td>4A_04_112C030F00</td>
      <td>K15_059422_2018_XN_21N035W</td>
      <td>2019-03-31 15:54:32.383</td>
      <td>CTX</td>
      <td>NIFL</td>
      <td>5056</td>
      <td>7168</td>
      <td>1</td>
      <td>...</td>
      <td>1.75</td>
      <td>34.46</td>
      <td>21.99</td>
      <td>234469987.0</td>
      <td>4.06</td>
      <td>14.08</td>
      <td>90.1</td>
      <td>Ride-along with HiRISE</td>
      <td>OK</td>
      <td>59422</td>
    </tr>
    <tr>
      <th>70723</th>
      <td>MROX_2321</td>
      <td>DATA/F09_039344_1423_XN_37S165W.IMG</td>
      <td>4A_04_10C6018D00</td>
      <td>F09_039344_1423_XN_37S165W</td>
      <td>2014-12-18 04:29:08.464</td>
      <td>CTX</td>
      <td>NIFL</td>
      <td>3776</td>
      <td>8192</td>
      <td>1</td>
      <td>...</td>
      <td>-24.5</td>
      <td>165.27</td>
      <td>-37.76</td>
      <td>206661098.9</td>
      <td>254.74</td>
      <td>15.34</td>
      <td>90.1</td>
      <td>Terra Sirenum</td>
      <td>OK</td>
      <td>39344</td>
    </tr>
    <tr>
      <th>28889</th>
      <td>MROX_1056</td>
      <td>DATA/B19_017097_1318_XN_48S126W.IMG</td>
      <td>4A_04_1054040700</td>
      <td>B19_017097_1318_XN_48S126W</td>
      <td>2010-03-20 16:44:39.958</td>
      <td>CTX</td>
      <td>NIFL</td>
      <td>5056</td>
      <td>52224</td>
      <td>1</td>
      <td>...</td>
      <td>23.24</td>
      <td>126.77</td>
      <td>-48.24</td>
      <td>249141981.2</td>
      <td>66.58</td>
      <td>15.32</td>
      <td>90.4</td>
      <td>Terra Sirenum</td>
      <td>OK</td>
      <td>17097</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 51 columns</p>
</div>



```python
hirise_rdr = get_index("mro.hirise", "rdr")
hirise_rdr.sample(5, random_state=42)
```

    Stored index is up-to-date.





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>VOLUME_ID</th>
      <th>FILE_NAME_SPECIFICATION</th>
      <th>INSTRUMENT_HOST_ID</th>
      <th>INSTRUMENT_ID</th>
      <th>OBSERVATION_ID</th>
      <th>PRODUCT_ID</th>
      <th>PRODUCT_VERSION_ID</th>
      <th>TARGET_NAME</th>
      <th>ORBIT_NUMBER</th>
      <th>MISSION_PHASE_NAME</th>
      <th>...</th>
      <th>LINE_PROJECTION_OFFSET</th>
      <th>SAMPLE_PROJECTION_OFFSET</th>
      <th>CORNER1_LATITUDE</th>
      <th>CORNER1_LONGITUDE</th>
      <th>CORNER2_LATITUDE</th>
      <th>CORNER2_LONGITUDE</th>
      <th>CORNER3_LATITUDE</th>
      <th>CORNER3_LONGITUDE</th>
      <th>CORNER4_LATITUDE</th>
      <th>CORNER4_LONGITUDE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>68663</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_036800_036899/ESP_036809_2640/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_036809_2640</td>
      <td>ESP_036809_2640_COLOR</td>
      <td>1</td>
      <td>MARS</td>
      <td>36809</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>801810.0</td>
      <td>1260530.0</td>
      <td>83.6808</td>
      <td>237.701</td>
      <td>83.6727</td>
      <td>237.516</td>
      <td>83.9234</td>
      <td>236.565</td>
      <td>83.9318</td>
      <td>236.757</td>
    </tr>
    <tr>
      <th>56127</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_030800_030899/ESP_030831_1335/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_030831_1335</td>
      <td>ESP_030831_1335_RED</td>
      <td>1</td>
      <td>MARS</td>
      <td>30831</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>-5451830.0</td>
      <td>11875900.0</td>
      <td>-46.3981</td>
      <td>38.0734</td>
      <td>-46.406</td>
      <td>37.9435</td>
      <td>-46.1322</td>
      <td>37.9086</td>
      <td>-46.1242</td>
      <td>38.0378</td>
    </tr>
    <tr>
      <th>18294</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_011400_011499/ESP_011400_1680/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_011400_1680</td>
      <td>ESP_011400_1680_COLOR</td>
      <td>2</td>
      <td>MARS</td>
      <td>11400</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>-1402640.0</td>
      <td>-7165880.0</td>
      <td>-12.0828</td>
      <td>241.439</td>
      <td>-12.0848</td>
      <td>241.421</td>
      <td>-11.8342</td>
      <td>241.39</td>
      <td>-11.8321</td>
      <td>241.407</td>
    </tr>
    <tr>
      <th>96217</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_049600_049699/ESP_049673_1000/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_049673_1000</td>
      <td>ESP_049673_1000_COLOR</td>
      <td>1</td>
      <td>MARS</td>
      <td>49673</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>-247898.5</td>
      <td>-2325763.5</td>
      <td>-80.0898</td>
      <td>96.4902</td>
      <td>-80.0948</td>
      <td>96.3953</td>
      <td>-79.8123</td>
      <td>95.909</td>
      <td>-79.8074</td>
      <td>96.0015</td>
    </tr>
    <tr>
      <th>30823</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_018300_018399/ESP_018301_2505/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_018301_2505</td>
      <td>ESP_018301_2505_COLOR</td>
      <td>1</td>
      <td>MARS</td>
      <td>18301</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>1078760.0</td>
      <td>-4561720.0</td>
      <td>70.0663</td>
      <td>103.136</td>
      <td>70.0631</td>
      <td>103.073</td>
      <td>70.3287</td>
      <td>102.954</td>
      <td>70.332</td>
      <td>103.018</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 54 columns</p>
</div>



## Instrument tools

### CTX

```python
from planetarypy.ctx import CTXEDR
```

```python
pid = ctrindex.sample().squeeze().PRODUCT_ID
pid
```




    'B09_013187_1492_XN_30S303W'



```python
ctxedr = CTXEDR(pid)
```

```python
ctxedr.local_path
```




    Path('/home/maye/big_drive/planetary_data/missions/mro/ctx/edr/B09_013187_1492_XN_30S303W/B09_013187_1492_XN_30S303W.IMG')



```python
ctxedr
```




    PRODUCT_ID: B09_013187_1492_XN_30S303W
    URL: https://pds-imaging.jpl.nasa.gov/data/mro/mars_reconnaissance_orbiter/ctx/mrox_0817/data/B09_013187_1492_XN_30S303W.IMG
    Local: /home/maye/big_drive/planetary_data/missions/mro/ctx/edr/B09_013187_1492_XN_30S303W/B09_013187_1492_XN_30S303W.IMG
    Not downloaded yet.



```python
ctxedr.download()
```

```python
ctxedr
```




    PRODUCT_ID: B09_013187_1492_XN_30S303W
    URL: https://pds-imaging.jpl.nasa.gov/data/mro/mars_reconnaissance_orbiter/ctx/mrox_0817/data/B09_013187_1492_XN_30S303W.IMG
    Local: /home/maye/big_drive/planetary_data/missions/mro/ctx/edr/B09_013187_1492_XN_30S303W/B09_013187_1492_XN_30S303W.IMG
    Shape: (1, 7168, 5056)


