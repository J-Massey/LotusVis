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
from lotusvis.flow_field import FlowBase


class Calculations(FlowBase):
    @property
    def snaps(self):
        return self._snaps

    def __init__(self, sim_dir, fn_root, length_scale, ext='vti', **kwargs):
        super().__init__(sim_dir, fn_root, length_scale, ext)

    def phase_average(self, t):
        """
        The first dimension will be the number of snapshots. We need
        to know how many phases we've averaged over as the data doesn't
        contain any time info
        t: Number of convection cycles
        :return:
        """
        # First check that we have an integer division of snapshots into convection cycles
        n_snaps = np.shape(self.snaps)[0]
        if n_snaps % t != 0:
            self.snaps = self.snaps[:-1]

        snaps_per_cycle = n_snaps//t
        phase_average = np.empty(n_snaps)
        for loop in range(n_snaps):
            phase_average[loop] = np.mean(self.snaps[loop::snaps_per_cycle], axis=0)
        return phase_average


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

    @snaps.setter
    def snaps(self, value):
        self._snaps = value
