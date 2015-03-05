#!/usr/bin/env bash
#
#	Usage:	/Volumes/Python/pyCalliphony/run_straight_conv.sh limsi_fr_tat_0006_perf_00
#	From:	~/Desktop/__IS2015__/__IS2015__/DATA/STIMULI_OP/colere_tst44k
#

#MATLAB=/Applications/MATLAB_R2012a.app/bin/matlab
MATLAB="matlab"
STRAIGHT="/Volumes/Projet/STRAIGHT/straight-v40-007-d"

fname=$1

DATA_PATH=$(pwd)
basename=${fname%_perf_*}    # Trim the shortest match from _perf to the end (www.tldp.org/LDP/LG/issue18/bash.html)
perf_id=${fname#*_perf_}

cd ${STRAIGHT}
${MATLAB} -nodisplay -nosplash -nojvm -r "RUN_synth_fct ${DATA_PATH}/${basename} _perf_${perf_id}; exit" >/dev/null
cd - >/dev/null