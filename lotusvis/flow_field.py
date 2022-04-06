# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This is a class that defines the useful quantities of flow field data.
@contact: jmom1n15@soton.ac.uk
"""

# Imports
import os
import time
import numpy as np
import lotusvis.io as io
from tkinter import Tcl


class FlowBase:
    """
    Class that holds all the functions to extract dat from a paraview fn,
    average and plot the contours and an animation.
    """

    def __init__(self, sim_dir, fn_root, length_scale, ext='vti', **kwargs):
        time_start = time.process_time()
        self.sim_dir = sim_dir
        self.datp_dir = os.path.join(sim_dir, 'datp')
        self.length_scale = length_scale

        print(f'Looking for .p{ext} files')
        time_read = time.process_time()
        fns = [fn for fn in os.listdir(self.datp_dir) if fn.startswith(fn_root) and fn.endswith(f'.p{ext}')]
        self.fns = Tcl().call('lsort', '-dict', fns)
        print(f'Found {len(self.fns)} instances in {time.process_time()-time_read:.3f}s, now extracting data and '
              f'assigning properties')

        self.X, self.Y, self.Z, self.U, self.V, self.Z, self.p = None, None, None, None, None, None, None
        t_avg = kwargs.get('t_avg', False)
        span_avg = kwargs.get('span_avg', False)

        time_prop = time.process_time()

        if len(fns) > 1:
            if t_avg:
                props = self.time_avg(ext)
            else:
                props = self.single_instance(ext)
        else:
            assert (len(fns) > 0), f"You don't have {fn_root}.p{ext} in your {self.datp_dir} folder"
            props = self.single_instance(ext)

        if span_avg:
            self.assign_spav(props)
        else:
            self.assign_props(props)

        print(f"Extracted data, and assigned properties in {time.process_time()-time_prop:.3f}s")
        print(f"Finished finding and extracting .p{ext} files in {time.process_time()-time_start:.3f}s")

    def assign_props(self, snap):
        self.X, self.Y = snap[0:2]
        u, v, z = snap[2:-1]
        self.U, self.V, self.Z = u, v, z
        self.p = snap[-1]
        del u, v, z, snap

    def assign_spav(self, snap):
        self.X, self.Y = snap[0:2]
        u, v, _ = snap[2:-1]
        self.U, self.V = np.mean(u, axis=2), np.mean(v, axis=2)
        self.p = np.mean(snap[-1], axis=0)
        del u, v, snap

    def single_instance(self, ext):
        if ext == 'vti':
            snap = io.vti_format_2d(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
        else:
            snap = io.vtr_format_2d(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
        snap = np.array(snap).T
        return snap

    def time_avg(self, ext):
        snaps = np.zeros(len(self.fns))
        for idx, fn in enumerate(self.fns):
            if ext == 'vti':
                snap = io.vti_format_2d(os.path.join(self.datp_dir, fn), self.length_scale)
            else:
                snap = io.vtr_format_2d(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
            snaps[idx] = snap
        del snap
        # Time average the flow field snaps
        mean_t = np.mean(np.array(snaps).T, axis=1)
        return mean_t

    def span_avg(self, snap):
        self.X, self.Y, self.Z = snap[0:2]
        u, v, z = snap[2:-1]
        self.U, self.V, self.Z = u, v, z
        self.p = np.mean(snap[-1], axis=0)
        del u, v, z, snap

    def rms(self):
        means = np.mean(np.array(self.snaps).T, axis=1)[2:-1]
        fluctuations = np.array(self.snaps)[:, 2:-1] - means
        del means
        rms = np.mean((fluctuations[:, 0] ** 2 + fluctuations[:, 1] ** 2 + fluctuations[:, 2] ** 2) ** (1 / 2))
        del fluctuations
        return np.mean(rms, axis=2)

    def rms_mag(self):
        mean = np.mean(np.array(self.snaps).T, axis=1)[2:-1]
        mean = np.sqrt(np.sum(mean ** 2))
        mag = np.array(self.snaps)[:, 2:-1] ** 2
        mag = np.sum(mag, axis=1) ** 0.5
        fluc = []
        for snap in mag:
            fluc.append(snap - mean)
        del mag, mean

        return np.mean(np.mean(fluc, axis=0), axis=2)

# TODO: add in POD modes
