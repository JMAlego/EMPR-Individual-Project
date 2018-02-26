# EMPR Individual Project (IC2)

_By Jacob Allen_

## Overview

An implementation of the "Individual Component 2" specification from the EMPR (Embedded Systems Project) module from Computer Science at the University of York.

The specification is as follows:
```
A PC-based GUI Visualiser: The MBED MONITOR Board will send effects data to the PC.

This will then be used to display a configurable lighting stage where lights are displayed graphically and may have their addresses assigned by the user. This will allow the user to see specific lights being altered by the DMX data stream.

There are two modes – Snapshot-mode a snapshot of the whole data packet (display at least 8 light channels). And real-time node, where a single light is updated as fast as the PC-USB link allows.
```


## Installation

1) Clone this repository

```sh
git clone git@github.com:JMAlego/EMPR-Individual-Project.git
```

2) Initialise the virtual environment

```sh
cd EMPR-Individual-Project
./init_venv.sh
```

3) Configure by editing config file

## Running

Use the `run.sh` script to run the program.