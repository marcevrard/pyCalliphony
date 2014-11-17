#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
SYNOPSIS

    py_calliphony [-h,--help] [-f ]

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
from scipy import interpolate
import argparse as ap
from savitzki_golay import savitzky_golay
import os.path

# FNAME = 'yves_montand_1_3_coord.txt'
HEADERS = ('cpu_time', 'position', 'f0')
FRAME_LEN = 0.005


if __name__ == '__main__':
    argp = ap.ArgumentParser(description=globals()['__doc__'], formatter_class=ap.RawDescriptionHelpFormatter)
    argp.add_argument('-f', '--fname', required=True, metavar='FILE', help="Coordinate input file name")
    argp.add_argument('-p', '--plot_on', action='store_true', help="Turn on the plotting")
    argp.add_argument('-w', '--write_to_files', action='store_true', help="Coordinate input file")
    args = argp.parse_args()

    # Reshape according to the headers num and all row (-1)
    val_np = np.genfromtxt(args.fname).reshape(-1, len(HEADERS))
    val_df = pd.DataFrame(val_np, columns=HEADERS)

    # Substract the start cpu_time from the time serie; express in s
    val_time = val_df['cpu_time'] - val_df.iloc[0]['cpu_time']
    # Insert in the df after the cpu_time column (and express in s from ms)
    val_df.insert(1, 'time', val_time/1000)

    # Smooth time and f0 curves
    f0_smooth = savitzky_golay(np.array(val_df['f0']), window_size=21, order=2)

    # Warp f0 values to the original wav file time (from STRAIGHT)
    # interp_fct = interpolate.interp1d(val_df['position'], val_df['f0'], 'linear')
    tck = interpolate.splrep(val_df['position'], f0_smooth, s=10)     # , s=0)

    posit_max = round(val_df['position'].iloc[-1] * 2, 2)/2     # round values to 0.005 (0.01/2)
    posit_np = np.arange(FRAME_LEN, posit_max, FRAME_LEN)   # FIXME 0 > FRAME_LEN, better solution?
    # f0_warp = interp_fct(posit_np)
    f0_warp = interpolate.splev(posit_np, tck, der=0)

    if args.plot_on is True:

        plt.plot(val_df['time'], val_df['f0'], 'b-', posit_np, f0_warp, 'r-')
        plt.show()

    if args.write_to_files is True:

        fbase = os.path.splitext(args.fname)[0]
        with open(fbase+'.newf0', 'w') as f_newf0:
            f0_warp.astype('float32').tofile(f_newf0)
        with open(fbase+'.newtime', 'w') as f_newtime:
            # noinspection PyTypeChecker
            np.array(val_df['time'], dtype='float32').tofile(f_newtime)
