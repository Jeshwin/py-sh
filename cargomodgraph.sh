#!/usr/bin/bash

folder=${PWD##*/}
folder=${folder%}
echo $folder

cargo modules generate graph --with-types --with-tests --with-orphans | dot -Tsvg > $folder.svg 
