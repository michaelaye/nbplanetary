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

`tomlkit pandas pvl numpy python-dateutil tqdm lxml yarl hirise-tools kalasiris`


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

```python
from planetarypy.pds.apps import get_index
```

```python
ctrindex = get_index("mro.ctx.indexes.edr")
ctrindex.sample(5)
```




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
      <th>75900</th>
      <td>MROX_2455</td>
      <td>DATA/F20_043687_1325_XN_47S294W.IMG</td>
      <td>4A_04_10DC014000</td>
      <td>F20_043687_1325_XN_47S294W</td>
      <td>2015-11-21 14:14:36.567</td>
      <td>CTX</td>
      <td>NIFL</td>
      <td>5056</td>
      <td>24576</td>
      <td>1</td>
      <td>...</td>
      <td>24.04</td>
      <td>294.73</td>
      <td>-47.57</td>
      <td>249238218.9</td>
      <td>71.38</td>
      <td>15.21</td>
      <td>89.2</td>
      <td>Hellas Planitia</td>
      <td>OK</td>
      <td>43687</td>
    </tr>
    <tr>
      <th>40726</th>
      <td>MROX_1392</td>
      <td>DATA/G14_023794_1798_XN_00S092W.IMG</td>
      <td>4A_04_1076020900</td>
      <td>G14_023794_1798_XN_00S092W</td>
      <td>2011-08-24 13:13:49.110</td>
      <td>CTX</td>
      <td>NIFL</td>
      <td>5056</td>
      <td>43008</td>
      <td>1</td>
      <td>...</td>
      <td>-4.36</td>
      <td>91.79</td>
      <td>-0.23</td>
      <td>229203270.8</td>
      <td>349.83</td>
      <td>14.16</td>
      <td>90.4</td>
      <td>Terrain north of Tithonium Chasma</td>
      <td>OK</td>
      <td>23794</td>
    </tr>
    <tr>
      <th>5325</th>
      <td>MROX_0205</td>
      <td>DATA/P11_005346_1735_XI_06S063W.IMG</td>
      <td>4A_04_1019013500</td>
      <td>P11_005346_1735_XI_06S063W</td>
      <td>2007-09-17 00:20:29.319</td>
      <td>CTX</td>
      <td>ITL</td>
      <td>5056</td>
      <td>52224</td>
      <td>1</td>
      <td>...</td>
      <td>-17.67</td>
      <td>63.21</td>
      <td>-6.51</td>
      <td>217090580.2</td>
      <td>315.16</td>
      <td>14.26</td>
      <td>90.2</td>
      <td>West Juventae Chasma and Ophir Planum</td>
      <td>OK</td>
      <td>5346</td>
    </tr>
    <tr>
      <th>114845</th>
      <td>MROX_3635</td>
      <td>DATA/N05_064486_1481_XN_31S039W.IMG</td>
      <td>4A_04_1146024F00</td>
      <td>N05_064486_1481_XN_31S039W</td>
      <td>2020-04-29 06:06:04.787</td>
      <td>CTX</td>
      <td>NIFL</td>
      <td>3776</td>
      <td>8192</td>
      <td>1</td>
      <td>...</td>
      <td>-5.07</td>
      <td>39.72</td>
      <td>-32.00</td>
      <td>215654598.6</td>
      <td>191.85</td>
      <td>15.94</td>
      <td>90.1</td>
      <td>Crater north of Argyre</td>
      <td>OK</td>
      <td>64486</td>
    </tr>
    <tr>
      <th>44851</th>
      <td>MROX_1524</td>
      <td>DATA/G20_026030_1390_XN_41S290W.IMG</td>
      <td>4A_04_108201CF00</td>
      <td>G20_026030_1390_XN_41S290W</td>
      <td>2012-02-14 18:31:34.526</td>
      <td>CTX</td>
      <td>NIFL</td>
      <td>3776</td>
      <td>21504</td>
      <td>1</td>
      <td>...</td>
      <td>23.91</td>
      <td>290.76</td>
      <td>-41.05</td>
      <td>249226043.2</td>
      <td>70.55</td>
      <td>15.23</td>
      <td>90.2</td>
      <td>Hellas Planitia</td>
      <td>OK</td>
      <td>26030</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 51 columns</p>
</div>



```python
hirise_rdr = get_index("mro.hirise.indexes.rdr")
hirise_rdr.sample(5)
```




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
      <th>124314</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_062500_062599/ESP_062586_1840/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_062586_1840</td>
      <td>ESP_062586_1840_RED</td>
      <td>1</td>
      <td>MARS</td>
      <td>62586</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>493636.5</td>
      <td>-20081462.0</td>
      <td>3.9142</td>
      <td>349.5270</td>
      <td>3.9017</td>
      <td>349.4270</td>
      <td>4.1513</td>
      <td>349.3930</td>
      <td>4.1640</td>
      <td>349.4940</td>
    </tr>
    <tr>
      <th>112358</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_056900_056999/ESP_056945_1090/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_056945_1090</td>
      <td>ESP_056945_1090_COLOR</td>
      <td>1</td>
      <td>MARS</td>
      <td>56945</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>405073.5</td>
      <td>2258479.5</td>
      <td>-71.0468</td>
      <td>280.3410</td>
      <td>-71.0497</td>
      <td>280.2890</td>
      <td>-70.7174</td>
      <td>280.1170</td>
      <td>-70.7146</td>
      <td>280.1680</td>
    </tr>
    <tr>
      <th>23249</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_015900_015999/ESP_015916_1640/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_015916_1640</td>
      <td>ESP_015916_1640_RED</td>
      <td>1</td>
      <td>MARS</td>
      <td>15916</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>-3691490.0</td>
      <td>24911000.0</td>
      <td>-15.9461</td>
      <td>71.3223</td>
      <td>-15.9568</td>
      <td>71.2317</td>
      <td>-15.5863</td>
      <td>71.1847</td>
      <td>-15.5756</td>
      <td>71.2753</td>
    </tr>
    <tr>
      <th>126778</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_064500_064599/ESP_064551_1745/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_064551_1745</td>
      <td>ESP_064551_1745_RED</td>
      <td>1</td>
      <td>MARS</td>
      <td>64551</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>-1267461.5</td>
      <td>-38647224.0</td>
      <td>-5.4864</td>
      <td>343.7370</td>
      <td>-5.4974</td>
      <td>343.6490</td>
      <td>-5.3569</td>
      <td>343.6310</td>
      <td>-5.3460</td>
      <td>343.7190</td>
    </tr>
    <tr>
      <th>27793</th>
      <td>MROHR_0001</td>
      <td>RDR/ESP/ORB_017100_017199/ESP_017182_1380/ESP_...</td>
      <td>MRO</td>
      <td>HIRISE</td>
      <td>ESP_017182_1380</td>
      <td>ESP_017182_1380_COLOR</td>
      <td>1</td>
      <td>MARS</td>
      <td>17182</td>
      <td>Extended Science Phase</td>
      <td>...</td>
      <td>-4928590.0</td>
      <td>9843080.0</td>
      <td>-42.0208</td>
      <td>71.4254</td>
      <td>-42.0228</td>
      <td>71.4017</td>
      <td>-41.6764</td>
      <td>71.3470</td>
      <td>-41.6743</td>
      <td>71.3705</td>
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




    'P15_007095_2017_XI_21N299W'



```python
ctxedr = CTXEDR(pid)
```

```python
ctxedr.local_path
```




    PosixPath('/home/maye/big_drive/planetary_data/mro/ctx/edr/MROX_0403/P15_007095_2017_XI_21N299W/P15_007095_2017_XI_21N299W.IMG')



```python
ctxedr
```




    PRODUCT_ID: P15_007095_2017_XI_21N299W
    URL: https://pds-imaging.jpl.nasa.gov/data/mro/mars_reconnaissance_orbiter/ctx/mrox_0403/data/P15_007095_2017_XI_21N299W.IMG
    Local: /home/maye/big_drive/planetary_data/mro/ctx/edr/MROX_0403/P15_007095_2017_XI_21N299W/P15_007095_2017_XI_21N299W.IMG
    Not downloaded yet.



```python
ctxedr.download()
```

```python
ctxedr
```




    PRODUCT_ID: P15_007095_2017_XI_21N299W
    URL: https://pds-imaging.jpl.nasa.gov/data/mro/mars_reconnaissance_orbiter/ctx/mrox_0403/data/P15_007095_2017_XI_21N299W.IMG
    Local: /home/maye/big_drive/planetary_data/mro/ctx/edr/MROX_0403/P15_007095_2017_XI_21N299W/P15_007095_2017_XI_21N299W.IMG
    Shape: (1, 35840, 5056)


