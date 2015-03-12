#!/usr/bin/env bash
#
#	Usage:	/Volumes/Python/pyCalliphony/run_rename_file_tree.sh
#	From:	~/Desktop/Desktop/__IS2015__/DATA/MEV
#

#../../limsi_fr_tat_0006_perf_12_MEV_colere/.wav

person=${PWD##*/}

for expr in */
do
    cd ${expr}
    for f in *_new.wav
    do
        cp ${f} ../${f/.wav/_${person}_${expr/\/}.wav}
    done
    cd - >/dev/null
done
