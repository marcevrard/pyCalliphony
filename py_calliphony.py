#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
SYNOPSIS

    py_calliphony [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    **TODO** This describes how to use this script. This docstring
        will be printed by the script if there is an error or
        if the user requests help (-h or --help).

EXAMPLES

    %run /Volumes/Python/pyCalliphony/py_calliphony.py

EXIT STATUS

    **TODO** List exit codes

AUTHORS

    Marc Evrard             <marc.evrard@limsi.fr>

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    $Id$
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

FNAME = 'yves_montand_1_1_coord_.txt'
HEADERS = ('cpu_time', 'position', 'f0')
FRAME_LEN = 0.005


if __name__ == '__main__':

    val_np = np.genfromtxt(FNAME).reshape(-1, 3)
    val_df = pd.DataFrame(val_np, columns=HEADERS)

    # Substract the start cpu_time from the time serie; express in s
    val_time = val_df['cpu_time'] - val_df.iloc[0]['cpu_time']
    # Insert in the df after the cpu_time column (and express in s from ms)
    val_df.insert(1, 'time', val_time/1000)

    # Warp f0 values to the original wav file time (from STRAIGHT)
    interp_fct = interp1d(val_df['position'], val_df['f0'], 'linear')

    posit_max = round(val_df['position'].iloc[-1] * 2, 2)/2
    posit_np = np.arange(0, posit_max, FRAME_LEN)
    f0_warp = interp_fct(posit_np)

    plt.plot(val_df['time'], val_df['f0'], 'b-', posit_np, f0_warp, 'r-')
    # val_df.drop('cpu_time', 1).drop('f0', 1).plot()
    # plt.plot(val_df['time'], val_df['f0'], '.')
    plt.show()
