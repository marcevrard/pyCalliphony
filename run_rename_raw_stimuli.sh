#!/usr/bin/env bash

for d_expr in */
do
    expr=${d_expr/\/}
    cd ${d_expr}
    for d_sent in */
    do
        cd ${d_sent}
        for f in *_${expr}.wav
        do
            mv ${f} ../../${f/_${expr}.wav/_perf_xx_raw_NAT_${expr}.wav}
        done
        cd ..
    done
    cd ..
done

# limsi_fr_tat_0006_perf_00_new_MEV_surprise

for d_expr in */
do
    expr=${d_expr/\/}
    cd ${d_expr}
    for d_sent in */
    do
        cd ${d_sent}
        for f in *.wav
        do
            mv ${f} ../../${f/.wav/_perf_xx_raw_SYNTH_${expr}.wav}
        done
        cd ..
    done
    cd ..
done