# Release notes

<!-- do not remove -->

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



