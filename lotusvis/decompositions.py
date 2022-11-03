# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This class provides some decompositions like time, phase average.
              Eventually I hope to integrate this with some DMD and POD decompositions.
@contact: jmom1n15@soton.ac.uk
"""
import os

import numpy as np

import lotusvis.io as io
from lotusvis.flow_field import ReadIn
from tqdm import tqdm


class Decompositions(ReadIn):
    def __init__(self, sim_dir, fn_root, length_scale, ext='vti', **kwargs):
        super().__init__(sim_dir, fn_root, length_scale, ext)

    def phase_average(self, t):
        """
        The first dimension will be the number of snapshots. We need
        to know how many phases we've averaged over as the data doesn't
        contain any time info
        :param t: Number of convection cycles
        :return: phase average with n/
        """
        # self.fns = self.fns[len(self.fns)//2:]
        n_phase_snaps = len(self.fns) // t
        # Get the shape to initialise the array (important for efficiency)
        phase_average = np.zeros(self.init_phase_average_array(t))
        for idx, fn in tqdm(enumerate(self.fns), total=len(self.fns)):
            # TODO: Make the vti vtr distinction
            snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
            # Start with zeros and build up the cumulative sum
            phase_average[int(idx % n_phase_snaps)] = phase_average[int(idx % n_phase_snaps)] + snap
        phase_average = phase_average/t
        return phase_average

    def init_phase_average_array(self, t):
        n_phase_snaps = len(self.fns) // t
        snapshot_shape = np.shape(io.read_vti(os.path.join(self.datp_dir, self.fns[0]), self.length_scale))
        return (n_phase_snaps,) + snapshot_shape

    # TODO: There's some array mismatch bug in time_avg, probably to do with the fact vti_format doesn't exist :/
    def time_average(self):
        snaps = np.array([])
        for idx, fn in enumerate(self.fns):
            if self.ext == 'vti':
                print(fn)
                snap = io.vti_format(os.path.join(self.datp_dir, fn), self.length_scale)
            else:
                snap = io.vtr_format_2d(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
            snaps = np.append(snaps, snap)
        del snap
        # Time average the flow field snaps
        print(np.shape(snaps))
        t_mean = np.mean(snaps, axis=0)
        return t_mean
