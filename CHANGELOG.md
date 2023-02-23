# Release notes

<!-- do not remove -->

## 0.25.0

### New Features

- Add generic SPICE kernel management ([#34](https://github.com/michaelaye/nbplanetary/issues/34))

- Add functionalities to CTXCollection ([#33](https://github.com/michaelaye/nbplanetary/issues/33))
  - CTXCollection should be able to use metadata from the index to:

    from the list of product_ids which is the essential attribute of a CTXCollection:

    - filter out corrupted data
    - filter for full width data of the sensor (important for flatfield calculations and mosaicking)
    - get the list of image times
    - get a dataframe of metadata filtered for the current list of product_ids.

- copy new config file to package data ([#32](https://github.com/michaelaye/nbplanetary/issues/32))

- Add dart to supported SPICE kernel archives ([#31](https://github.com/michaelaye/nbplanetary/issues/31))

- make storage more flexible ([#30](https://github.com/michaelaye/nbplanetary/issues/30))
  - sometimes there is a server with raw/edr data locally available.
But then processed data cannot be stored on that.
And sometimes this is true for one instrument or mission, but not the next.
add missions.<mission>.<instrument>.datapaths section to config file to manage this.
Also add DBManager class as general interface to all data storage things.

- add progress bar to fix_hirise_edr ([#25](https://github.com/michaelaye/nbplanetary/issues/25))

- add label downloader for HiRISE products ([#24](https://github.com/michaelaye/nbplanetary/issues/24))

- Run fix_hirise_edr automatically ([#23](https://github.com/michaelaye/nbplanetary/issues/23))
  - The `fix_hirise_edr` pds.index util exists but is not automatically called upon when
downloading the EDR index for MRO HiRISE

- Improve API for get_index() ([#22](https://github.com/michaelaye/nbplanetary/issues/22))
  - Index can read a shortened index key (without '.indexes.') so no need to make the user to know that.

- add read_index_data ([#21](https://github.com/michaelaye/nbplanetary/issues/21))

## 0.21.8

### New Features

- add stitched_cube_path to SOURCE_PRODUCT ([#20](https://github.com/michaelaye/nbplanetary/issues/20))



## 0.21.7


### Bugs Squashed

- url attribute was not working ([#19](https://github.com/michaelaye/nbplanetary/issues/19))


## 0.21.6

### New Features

- Consolidate classes better ([#18](https://github.com/michaelaye/nbplanetary/issues/18))
  - RGB_NOMAP had code that should be a base class
  - SOURCE_PRODUCT has some similarities to BASE_PRODUCT but not close enough to be derived
  - SOURCE_PRODUCT gets its own local_path/remote_path/url/download code segment
  - other products can inherit from SOURCE_PRODUCT and initialize it with the correct PRODUCT_ID string.﻿



## 0.21.5


### Bugs Squashed

- SOURCE_PRODUCT downloader was still old code ([#17](https://github.com/michaelaye/nbplanetary/issues/17))


## 0.21.4


### Bugs Squashed

- new product classes not exported to lib ([#16](https://github.com/michaelaye/nbplanetary/issues/16))


## 0.21.3

### New Features

- Add flag to not have URLs checked, for performance ([#15](https://github.com/michaelaye/nbplanetary/issues/15))

- Move check_url_exists to utils ([#13](https://github.com/michaelaye/nbplanetary/issues/13))

- Make sure get_index downloads and converts intelligently ([#12](https://github.com/michaelaye/nbplanetary/issues/12))

- Add SOURCE_PRODUCT, RED_PRODUCT, IR_PRODUCT to hirise module ([#11](https://github.com/michaelaye/nbplanetary/issues/11))

- Remove old HiRISE code ([#3](https://github.com/michaelaye/nbplanetary/issues/3))
  - The dependency on the old HiRISE package blocks creation of a conda package. 
  - Clean up old HiRISE code and add here.



## 0.21.2


### Bugs Squashed

- Missing dependency fastcore ([#10](https://github.com/michaelaye/nbplanetary/issues/10))


## 0.21.1


### Bugs Squashed

- User functions not exported to library ([#8](https://github.com/michaelaye/nbplanetary/issues/8))
  - I forgot the #export line in the cells with the user functions.



## 0.21.0

### New Features

- add user functions to spice.kernels ([#7](https://github.com/michaelaye/nbplanetary/issues/7))


## 0.20.0

### New Features

- Improve (date)time converters to be auto-matching ([#5](https://github.com/michaelaye/nbplanetary/issues/5))
  - Having to know the correct converter function to convert either just dates or full datetimes is annoying.

Improve the functionality so that only one function per direction is required:

* nasa_time_to_iso
* iso_time_to_nasa

- Add SPICE kernel retriever ([#4](https://github.com/michaelaye/nbplanetary/issues/4))
  - SPICE kernel management is an arduous task.

I have identified a way to wrap the NAIF Perl script for retrieving SPICE kernel lists and URLs for a given mission and start/stop times.

To be added within a new sub-module `spice.kernels`.



