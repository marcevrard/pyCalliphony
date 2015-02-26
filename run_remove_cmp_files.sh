#!/bin/bash
#
#	Usage:	/Volumes/Python/pyCalliphony/run_remove_cmp_files.sh 0006 0009 0011 0100 0121
#	From:	~/Documents/at_LIMSI_BIG/HTS/DEMO/HTS-demo-ADAPT-joie-tst
#

SAT_DEC="data/cmp"
OUT_PATH="removed"

for var in "$@"
do
    for style in "colere" "joie" "neutre" "peur" "sensuel" "surprise" "tristesse"
    do
        mkdir -p ${OUT_PATH}/${style}
        for fpath in ${SAT_DEC}/${style}/*_${var}*.cmp
        do
            mv ${fpath} ${OUT_PATH}/${style}
        done
    done
done