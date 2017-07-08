#!/bin/bash

SRC=/home/smith/Dropbox/ellida/
DEST=/home/smith/projects/poky/meta-ellida/recipes-ellida/ellida-daemon/ellida-daemon-0.1/ellidadaemon

cp $SRC/engine/ellida_daemon.py $DEST/daemon.py
cp -r $SRC/providers/ $DEST/providers
