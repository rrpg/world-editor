# RPG World Editor

Program to create and edit worlds for my game (https://github.com/padawin/Rpg).
Uses a map generator to create the world (https://github.com/padawin/map-generator-simplex)

## Requirements

* Python 2.7 or above
* PyQt4

## Setup

This program uses submodules. First thing to do is to compile the map generator:

```
git submodule init
git submodule update

cd externals/map-generator
make

cd ..
```

Then, run the editor:

```
./main.py
```
