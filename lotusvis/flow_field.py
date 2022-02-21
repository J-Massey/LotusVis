# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This is a class that defines the useful quantities of flow field data.
@contact: jmom1n15@soton.ac.uk
"""

# Imports
import os
import numpy as np
import lotusvis.io as io
from tkinter import Tcl


class FlowBase:
    """
    Class that holds all the functions to extract dat from a paraview fn,
    average and plot the contours and an animation.
    """

    def __init__(self, sim_dir, fn_root, length_scale, ext='vti', **kwargs):
        self.sim_dir = sim_dir
        self.datp_dir = os.path.join(sim_dir, 'datp')
        self.length_scale = length_scale

        print(f'Looking for .p{ext} files')
        fns = [fn for fn in os.listdir(self.datp_dir) if fn.startswith(fn_root) and fn.endswith(f'.p{ext}')]
        self.fns = Tcl().call('lsort', '-dict', fns)

        self.X, self.Y, self.U, self.V, self.p = None, None, None, None, None
        t_avg = kwargs.get('t_avg', False)

        if len(fns) > 1:
            if t_avg:
                props = self.time_avg(ext)
            else:
                props = self.single_instance(ext)
        else:
            assert (len(fns) > 0), f'You dont have {fn_root}.p{ext} in your {self.datp_dir} folder'
            props = self.single_instance(ext)

        self.assign_props(props)

    def assign_props(self, snap):
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
        snaps = []
        for fn in self.fns:
            if ext == 'vti':
                snap = io.vti_format_2d(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
            else:
                snap = io.vtr_format_2d(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
            snaps.append(snap)
        del snap
        # Time average the flow field snaps
        mean_t = np.mean(np.array(snaps).T, axis=1)
        return mean_t

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


class LoadVTR:
    """
    Class that holds all the functions to extract dat from a paraview fn,
    average and plot the contours and an animation.
    """

    def __init__(self, sim_dir, fn_root, length_scale, vti=True, **kwargs):
        self.sim_dir = sim_dir
        self.datp_dir = os.path.join(sim_dir, 'datp')
        self.length_scale = length_scale

        if vti:
            fns = [fn for fn in os.listdir(self.datp_dir) if fn.startswith(fn_root) and fn.endswith('.pvti')]
        else:
            fns = [fn for fn in os.listdir(self.datp_dir) if fn.startswith(fn_root) and fn.endswith('.pvtr')]
        self.fns = Tcl().call('lsort', '-dict', fns)

        self.X, self.Y, self.U, self.V, self.p = None, None, None, None, None
        t_avg = kwargs.get('t_avg', False)

        if len(fns) > 1:
            if t_avg:
                props = self.time_avg()
            else:
                props = self.single_instance()
        else:
            assert (len(fns) > 0), f'You dont have {fn_root}.pvtr in your {self.datp_dir} folder'
            props = self.single_instance()

        self.assign_props(props)

    def assign_props(self, snap):
        self.X, self.Y = snap[0:2]
        u, v, _ = snap[2:-1]
        self.U, self.V = np.mean(u, axis=2), np.mean(v, axis=2)
        self.p = np.mean(snap[-1], axis=0)
        del u, v, snap

    def single_instance(self):
        snap = io.vti_format_2d(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
        snap = np.array(snap).T
        return snap

    def time_avg(self):
        snaps = []
        for fn in self.fns:
            snap = io.vti_format_2d(os.path.join(self.datp_dir, fn), self.length_scale)
            snaps.append(snap)
        del snap
        # Time average the flow field snaps
        mean_t = np.mean(np.array(snaps).T, axis=1)
        return mean_t

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
