#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SYNOPSIS

    py_calliphony [-h,--help] -f fpath [-p] [-w]

DESCRIPTION

    **TODO**

EXAMPLES

    %run /Volumes/Python/pyCalliphony/py_calliphony.py -f limsi_fr_tat_0002_perf_01.txt -w -p

EXIT STATUS

    **TODO**

AUTHORS

    Marc Evrard             <marc.evrard@limsi.fr>

LICENSE

    **TODO**

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
FRAME_PTS = int(round(FRAME_DUR*FS))


class CalliStraightConv:
    """
    Class to convert calliphony tablette coordinates to straight
    """
    def __init__(self, coord_fpath):
        """Import and format in DataFrame the raw input coordinated"""
        self.coord_fpath = coord_fpath
        self.main_path, self.coord_fname = os.path.split(coord_fpath)
        self.fbase_path = os.path.splitext(coord_fpath)[0]
        # Reshape according to the headers num and all row (-1)
        self.coord_arr = np.genfromtxt(coord_fpath).reshape(-1, len(HEADERS))
        self.coord_df = pd.DataFrame(self.coord_arr, columns=HEADERS)

        self.f0_orig_arr = np.array([])
        self.f0_uv_idx = np.array([])
        self.f0_warp_arr = np.array([])
        self.posit_arr = np.array([])
        self.imap_arr = np.array([])

    def import_f0(self):
        """Import f0 from STRAIGHT"""
        f0_fpath = os.path.join(self.main_path, '_'.join(self.coord_fname.split('_')[:4]) + '.f0')
        # noinspection PyNoneFunctionAssignment
        self.f0_orig_arr = np.fromfile(f0_fpath, dtype='f4')
        self.f0_uv_idx = np.where(self.f0_orig_arr == 0)[0]  # Unvoiced indexes

    def extract_time(self):
        """Extract relative time from CPU time"""
        coord_time = self.coord_df['cpu_time'] - self.coord_df.iloc[0]['cpu_time']
        # Insert in df after cpu_time column (and express in s (from ms))
        self.coord_df.insert(1, 'time', coord_time/1000)

    def smooth_curves(self):
        """Smooth time and f0 curves"""
        self.coord_df['time_smooth'] = savitzky_golay(np.array(self.coord_df['time']), window_size=21, order=2)
        self.coord_df['pos_smooth'] = savitzky_golay(np.array(self.coord_df['position']), window_size=21, order=2)
        self.coord_df['f0_smooth'] = savitzky_golay(np.array(self.coord_df['f0']), window_size=21, order=2)

    def warp_f0(self):
        """Warp f0 values to the original wav file time (from STRAIGHT)"""
        posit_max = round(self.coord_df['pos_smooth'].iloc[-1] * 2, 2)/2     # round values to 0.005 (0.01/2)
        self.posit_arr = np.arange(start=FRAME_DUR, stop=posit_max, step=FRAME_DUR)  # TODO 0 > FRAME_LEN, better solut?
        tck = interpolate.splrep(self.coord_df['pos_smooth'], self.coord_df['f0_smooth'], s=5)    # , s=10)
        self.f0_warp_arr = interpolate.splev(self.posit_arr, tck, der=0)

    def set_unvoiced_f0(self):
        """Set zeros to unvoiced sections"""
        self.f0_uv_idx = [el for el in self.f0_uv_idx if el < len(self.f0_warp_arr)]
        self.f0_warp_arr[self.f0_uv_idx] = 0

    def interp_time(self):
        """
        Interpolate the time array to a STRAIGHT time mapping format
        (imap = 1 : 1/(FRAME_PTS) : num_frames;)
        """
        # noinspection PyTypeChecker
        num_frames = len(self.f0_orig_arr)
        time_max = self.coord_df['time_smooth'].max()
        pos_max = self.coord_df['pos_smooth'].max()

        target_frame_points_avg = round(FRAME_PTS * (time_max/pos_max))
        imap_idx = np.arange(start=1, stop=num_frames, step=1/target_frame_points_avg)
        imap_time = imap_idx / num_frames * time_max

        time_map = np.interp(x=imap_time, xp=self.coord_df['time_smooth'], fp=self.coord_df['pos_smooth'])
        self.imap_arr = time_map * num_frames / pos_max                 # normalize max value to total number of frames

    def write_to_files(self):
        """Write to binary file"""
        with open(self.fbase_path+'.newf0', 'w') as f_newf0:
            self.f0_warp_arr.astype('float32').tofile(f_newf0)
        with open(self.fbase_path+'.newpos', 'w') as f_newpos:
            self.imap_arr.astype('float32').tofile(f_newpos)

# ==================================================================================================================== #
    def process_conv(self):
        """
        Process the complete conversion
        """
        self.import_f0()
        self.extract_time()
        self.smooth_curves()    # optional DEBUG
        self.warp_f0()
        self.set_unvoiced_f0()
        self.interp_time()

# ==================================================================================================================== #
    def plot_f0(self):
        # print('f0_uv_idx:', f0_uv_idx)
        plt.plot(self.f0_orig_arr)
        plt.legend(['f0_orig_np'], loc='best')
        plt.show()

    def plot_time(self):
        plt.plot(self.coord_df['time'])
        plt.plot(self.coord_df['position'])
        plt.legend(['time', 'position'], loc='best')
        plt.show()

    def plot_smoothed_curves(self):
        # plt.plot(coord_df['time'], coord_df['position'], coord_df['time_smooth'], coord_df['pos_smooth'])
        # plt.legend(['position', 'position_smooth'], loc='best')
        plt.plot(self.coord_df['time'], self.coord_df['f0'], self.coord_df['time_smooth'], self.coord_df['f0_smooth'])
        plt.legend(['f0', 'f0_smooth'], loc='best')
        plt.show()

    def plot_warped_f0(self):
        f1, ax_arr = plt.subplots(2, sharey=True)
        ax_arr[0].plot(self.coord_df['time'], self.coord_df['f0'])
        ax_arr[0].legend(['f0'], loc='best')
        ax_arr[1].plot(self.posit_arr, self.f0_warp_arr)
        ax_arr[1].legend(['f0_warp'], loc='best')
        f1.show()

    def plot_interp_time(self):
        plt.figure(2)
        plt.plot(self.imap_arr)
        plt.legend(['imap'], loc='best')
        plt.show()

if __name__ == '__main__':
    argp = ap.ArgumentParser(description=globals()['__doc__'], formatter_class=ap.RawDescriptionHelpFormatter)
    argp.add_argument('-f', '--fpath', required=True, metavar='FILE', help="Coordinate input file name")
    argp.add_argument('-p', '--plot_on', action='store_true', help="Turn on the plotting")
    argp.add_argument('-w', '--write_to_files', action='store_true', help="Coordinate input file")
    args = argp.parse_args()

    calli_straight_conv_obj = CalliStraightConv(args.fpath)

    calli_straight_conv_obj.process_conv()

    if args.plot_on is True:

        calli_straight_conv_obj.plot_warped_f0()
        calli_straight_conv_obj.plot_interp_time()

    if args.write_to_files is True:
        calli_straight_conv_obj.write_to_files()