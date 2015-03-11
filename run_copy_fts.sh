#!/usr/bin/env bash
#
#	Usage:	/Volumes/Python/pyCalliphony/run_copy_fts.sh ~/Desktop/__IS2015__/DATA/MEV
#	From:	~/Desktop/Desktop/__IS2015__/DATA/SDZ
#
#   for d in */; do cd ${d}; /Volumes/Python/pyCalliphony/run_copy_fts.sh ~/Desktop/__IS2015__/DATA/MEV; echo "${d} done."; cd -; done

orig_path=${1}
expr=${PWD##*/}

for fname in *.wav
do
    baseperf=${fname%.*}
    basename=${fname%_perf_*}
    cp ${orig_path}/${expr}/${basename}.f0 .
    cp ${orig_path}/${expr}/${basename}.sp .
    cp ${orig_path}/${expr}/${basename}.ap .
done