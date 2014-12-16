#!/bin/bash
#
#	Usage:	/Volumes/Python/pyCalliphony/run_straight_gci_extr.sh
#	From:	~/Desktop/Calliphony_SD/matlab/corpus_marc
#

#MATLAB=/Applications/MATLAB_R2012a.app/bin/matlab
MATLAB="matlab"
STRAIGHT="/Volumes/Projet/STRAIGHT/straight-v40-007-d"

THISDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" 	# Get this file path
DATA_PATH=$(pwd)


for fname in *.f0
do
    cd ${STRAIGHT}
    ${MATLAB} -nodisplay -nosplash -nojvm -r "RUN_extr_gcis_fct ${DATA_PATH}/${fname}; exit" >/dev/null
    cd - >/dev/null

    echo "${fname} GCI extracted."
done
