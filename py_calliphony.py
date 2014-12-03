#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    argp.add_argument('-f', '--fpath', required=True, metavar='FILE', help="Coordinate input file name")
    argp.add_argument('-p', '--plot_on', action='store_true', help="Turn on the plotting")
    argp.add_argument('-w', '--write_to_files', action='store_true', help="Coordinate input file")
    args = argp.parse_args()

    # Reshape according to the headers num and all row (-1)
    coord_np = np.genfromtxt(args.fpath).reshape(-1, len(HEADERS))
    coord_df = pd.DataFrame(coord_np, columns=HEADERS)

    # Include the original f0 file to get the number of samples
    main_path, coord_fname = os.path.split(args.fpath)
    f0_fpath = os.path.join(main_path, '_'.join(coord_fname.split('_')[:4]) + '.f0')
    # noinspection PyNoneFunctionAssignment
    f0_orig_np = np.fromfile(f0_fpath, dtype='f4')
    f0_uv_idx = np.where(f0_orig_np == 0)[0]  # Unvoiced indexes

    # Extract relative time from CPU time
    coord_time = coord_df['cpu_time'] - coord_df.iloc[0]['cpu_time']
    coord_df.insert(1, 'time', coord_time/1000)     # Insert in df after cpu_time column (and express in s (from ms))

    # Smooth time and f0 curves
    coord_df['time_smooth'] = savitzky_golay(np.array(coord_df['time']), window_size=21, order=2)
    coord_df['pos_smooth'] = savitzky_golay(np.array(coord_df['position']), window_size=21, order=2)
    coord_df['f0_smooth'] = savitzky_golay(np.array(coord_df['f0']), window_size=21, order=2)

    # Warp f0 values to the original wav file time (from STRAIGHT)
    posit_max = round(coord_df['pos_smooth'].iloc[-1] * 2, 2)/2   # round values to 0.005 (0.01/2)
    posit = np.arange(start=FRAME_DUR, stop=posit_max, step=FRAME_DUR)   # TODO 0 > FRAME_LEN, better solution?
    tck = interpolate.splrep(coord_df['pos_smooth'], coord_df['f0_smooth'], s=5)    # , s=10)
    f0_warp = interpolate.splev(posit, tck, der=0)

    # Set zeros to unvoiced sections
    f0_uv_idx = [el for el in f0_uv_idx if el < len(f0_warp)]
    f0_warp[f0_uv_idx] = 0

    # Interpolate the time array to a STRAIGHT time mapping format (imap = 1 : 1/(frame_points) : num_frames;)
    # noinspection PyTypeChecker
    num_frames = len(f0_orig_np)
    time_max = coord_df['time_smooth'].max()
    pos_max = coord_df['pos_smooth'].max()

    target_frame_points_avg = round(frame_points * (time_max/pos_max))
    imap_idx = np.arange(start=1, stop=num_frames, step=1/target_frame_points_avg)
    imap_time = imap_idx / num_frames * time_max

    time_map = np.interp(x=imap_time, xp=coord_df['time_smooth'], fp=coord_df['pos_smooth'])
    imap = time_map * num_frames / pos_max                       # normalize max value to total number of frames

    if args.plot_on is True:

        f1, ax_arr = plt.subplots(2, sharey=True)
        ax_arr[0].plot(coord_df['time'], coord_df['f0'])
        ax_arr[0].legend(['f0'], loc='best')
        ax_arr[1].plot(posit, f0_warp)
        ax_arr[1].legend(['f0_warp'], loc='best')

        f2, ax2 = plt.subplots(111)
        ax2.legend(['imap'], loc='best')

        f1.show()
        f2.show()

    if args.write_to_files is True:

        fbase_path = os.path.splitext(args.fpath)[0]
        with open(fbase_path+'.newf0', 'w') as f_newf0:
            f0_warp.astype('float32').tofile(f_newf0)     # f0_warp DEBUG
        with open(fbase_path+'.newpos', 'w') as f_newpos:
            imap.astype('float32').tofile(f_newpos)
