#!/bin/bash


POKY_DIR="/home/smith/projects/poky"
REPO_DIR="/home/smith/projects/ellida"

if [ $(hostname) == starlight ] ; then
    echo "Startlight!"

elif [ $(hostname) == starship ] ; then
    echo "Starship!"
else
    echo "Unknown host!"
fi
