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

HEADERS = ('cpu_time', 'position', 'f0')
FRAME_DUR = 0.005
FS = 48000
frame_points = int(round(FRAME_DUR*FS))


if __name__ == '__main__':
    argp = ap.ArgumentParser(description=globals()['__doc__'], formatter_class=ap.RawDescriptionHelpFormatter)
    argp.add_argument('-f', '--fname', required=True, metavar='FILE', help="Coordinate input file name")
    argp.add_argument('-p', '--plot_on', action='store_true', help="Turn on the plotting")
    argp.add_argument('-w', '--write_to_files', action='store_true', help="Coordinate input file")
    args = argp.parse_args()

    # Reshape according to the headers num and all row (-1)
    coord_np = np.genfromtxt(args.fname).reshape(-1, len(HEADERS))
    coord_df = pd.DataFrame(coord_np, columns=HEADERS)

    # Extract relative time from CPU time
    coord_time = coord_df['cpu_time'] - coord_df.iloc[0]['cpu_time']
    coord_df.insert(1, 'time', coord_time/1000)     # Insert in df after cpu_time column (and express in s (from ms))

    # Smooth time and f0 curves
    coord_df['time_smooth'] = savitzky_golay(np.array(coord_df['time']), window_size=21, order=2)
    coord_df['pos_smooth'] = savitzky_golay(np.array(coord_df['position']), window_size=21, order=2)
    coord_df['f0_smooth'] = savitzky_golay(np.array(coord_df['f0']), window_size=21, order=2)

    # Warp f0 values to the original wav file time (from STRAIGHT)
    posit_max = round(coord_df['pos_smooth'].iloc[-1] * 2, 2)/2   # round values to 0.005 (0.01/2)
    posit_np = np.arange(start=FRAME_DUR, stop=posit_max, step=FRAME_DUR)   # TODO 0 > FRAME_LEN, better solution?
    tck = interpolate.splrep(coord_df['pos_smooth'], coord_df['f0_smooth'], s=5)    # , s=10)
    f0_warp = interpolate.splev(posit_np, tck, der=0)

    # Interpolate the time array to a STRAIGHT time mapping format (imap = 1 : 1/frame_points : num_frames;)
    num_frames = len(coord_df['time_smooth'])
    time_max = coord_df['time_smooth'].max()
    imap_idx_np = np.arange(start=1/frame_points, stop=num_frames-1, step=1/frame_points)
    imap_time_np = imap_idx_np / (num_frames-1) * time_max
    interp_time_fct = interpolate.interp1d(coord_df['time_smooth'], coord_df['pos_smooth'], 'linear')
    time_map_np = interp_time_fct(imap_time_np)
    imap_np = time_map_np / time_max * num_frames                      # normalize max value to total number of frames

    if args.plot_on is True:

        # plt.plot(coord_df['time'], coord_df['f0'])
        # plt.plot(posit_np, f0_warp)
        # plt.plot(coord_df['time'], coord_df['position'])
        # plt.plot(coord_df['time_smooth'], coord_df['pos_smooth'])
        plt.plot(imap_time_np, imap_np)
        plt.show()

    if args.write_to_files is True:

        fbase = os.path.splitext(args.fname)[0]
        with open(fbase+'.newf0', 'w') as f_newf0:
            f0_warp.astype('float32').tofile(f_newf0)
        with open(fbase+'.newpos', 'w') as f_newpos:
            imap_np.astype('float32').tofile(f_newpos)
