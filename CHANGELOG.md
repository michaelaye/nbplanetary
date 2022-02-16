# Release notes

<!-- do not remove -->

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



