#! /usr/bin/env bash

CELL_NAME=challenge
GDS_FILE=challenge.gds
LVS_FILE=challenge.spice
RC_FILE=$PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc
OUT_DIR=./ext/

rm $OUT_DIR -rf
mkdir $OUT_DIR

magic -dnull -noconsole -rcfile $RC_FILE << EOF
gds read $GDS_FILE
load $CELL_NAME

cd $OUT_DIR
extract do local
extract all
ext2spice lvs
ext2spice subcircuits off
ext2spice -o $LVS_FILE

quit -noprompt
EOF
