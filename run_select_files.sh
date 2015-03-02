#!/bin/bash
#
#	Usage:	/Volumes/Python/pyCalliphony/run_select_files.sh 0006 0009 0011 0100 0121
#	From:	~/Documents/at_LIMSI_BIG/HTS/DEMO/HTS-demo-ADAPT-joie-tst
#

SAT_DEC="0"
#SAT_DEC="qst001/ver1/SAT+dec_feat3/0"
#SAT_DEC="gen/qst001/ver1/SAT+dec_feat3/0"

OUT_PATH="gen/selected"

for var in "$@"
do
    for fpath in ${SAT_DEC}/*_${var}*.wav
    do
        base_path=${fpath%.wav}
        base_name=${base_path##*/}

        mkdir -p ${OUT_PATH}/${base_name}

        cp ${base_path}.wav ${OUT_PATH}/${base_name}
        cp ${base_path}.f0 ${OUT_PATH}/${base_name}
        cp ${base_path}.sp ${OUT_PATH}/${base_name}
        cp ${base_path}.ap ${OUT_PATH}/${base_name}
    done
done
