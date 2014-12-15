#!/bin/bash
#
#	Usage:	/Volumes/Python/pyCalliphony/run_calli_straight_conv.sh
#	From:	~/Desktop/Calliphony_SD/matlab/corpus_marc
#

#MATLAB=/Applications/MATLAB_R2012a.app/bin/matlab
MATLAB="matlab"
STRAIGHT="/Volumes/Projet/STRAIGHT/straight-v40-007-d"

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" 	# Get this file path


for fname in *_perf_*.txt
do
    basename=${fname%_perf_*}    # Trim the shortest match from _perf to the end (www.tldp.org/LDP/LG/issue18/bash.html)
    baseperf=${fname%.*}
    perf_id=${baseperf#*_perf_}
    python3 ${THISDIR}/py_calliphony.py -f ${basename}_perf_${perf_id}.txt -w

    cd ${STRAIGHT}
    ${MATLAB} -nodisplay -nosplash -nojvm -r "RUN_synth_fct ${basename} _perf_${perf_id}; exit" >/dev/null
    cd - >/dev/null

    echo "${basename}_perf_${perf_id} file processing done."
done
