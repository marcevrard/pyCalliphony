#!/bin/bash
#
#	Usage:	/Volumes/Python/pyCalliphony/run_move_txt_copy_fts.sh
#	From:	~/Desktop/__IS2015__/__IS2015__/DATA/STIMULI_OP/colere
#

for fname in *.wav
do
    baseperf=${fname%.*}
    basename=${fname%_perf_*}
    mv ${basename}/${baseperf}.txt .
#    cp ${basename}/${basename}.f0 .
#    cp ${basename}/${basename}.sp .
#    cp ${basename}/${basename}.ap .
done