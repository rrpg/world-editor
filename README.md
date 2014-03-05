# rRpg World Editor

Program to create and edit worlds for my game (https://github.com/rrpg/engine).

## Requirements

* Python 2.7 or above
* PyQt4
* Gettext

## Setup

This program uses submodules. First thing to do is to compile the map generator:
```bash
make
cd externals/map-generator
make
cd ../..
```

Then, run the editor:
```
# Will run the editor with the system locale
./editor

# Will run the editor in french
./editor-francais

# Will run the editor in english
./editor-english
```
