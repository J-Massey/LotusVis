# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This is a class that defines the useful quantities of flow field data.
@contact: jmom1n15@soton.ac.uk
"""

import os
import time
from tkinter import Tcl

import numpy as np
from tqdm import tqdm
import lotusvis.io as io


class ReadIn:
    """
    Class that holds all the functions to extract datp from a paraview fn.
    """
    def __init__(self, sim_dir, fn_root, length_scale, ext='vti', **kwargs):
        self.fn_root = fn_root
        self.sim_dir = sim_dir
        self.datp_dir = os.path.join(sim_dir, 'datp')
        self.length_scale = length_scale
        self.ext = ext

    @property
    def fns(self):
        fns = [fn for fn in os.listdir(self.datp_dir) if fn.startswith(self.fn_root) and fn.endswith(f'.p{self.ext}')]
        fns = Tcl().call('lsort', '-dict', fns)
        return fns

    @fns.setter
    def fns(self, value):
        self.fns = value

    @property
    def snaps(self):
        # This is only possible when working with small datasets or on iridis
        # because of the memory it takes
        snaps = np.empty(self.init_snap_array())
        for idx, fn in tqdm(enumerate(self.fns)):
            # TODO: Make the vti vtr distinction
            snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
            snaps[idx] = snap
            del snap
        return snaps

    def init_snap_array(self):
        n_snaps = len(self.fns)
        snapshot_shape = np.shape(io.read_vti(os.path.join(self.datp_dir, self.fns[0]), self.length_scale))
        return (n_snaps,) + snapshot_shape

    def init_flow(self, ext, fn_root, kwargs):
        t_avg = kwargs.get('t_avg', False)
        span_avg = kwargs.get('span_avg', False)
        time_prop = time.process_time()
        props = self.get_props(ext, fn_root, t_avg)
        if span_avg:
            self.spav_props(props)
        else:
            self.props(props)
        print(f"Extracted data, and assigned properties in {time.process_time() - time_prop:.3f}s")

    def get_props(self, ext, fn_root, t_avg):
        if len(self.fns) > 1:
            if t_avg:
                props = self.time_avg(ext)
            else:
                props = self.single_instance(ext)
        else:
            assert (len(self.fns) > 0), f"You don't have {fn_root}.p{ext} in your {self.datp_dir} folder"
            props = self.single_instance(ext)
        return props

    def props(self, snap):
        self.X, self.Y, self.Z = snap[0:3]
        u, v, w = snap[3:-1]
        self.U, self.V, self.W = u, v, w
        self.p = snap[-1]
        del u, v, w, snap

    def spav_props(self, snap):
        self.X, self.Y, _ = snap[0:3]
        self.X, self.Y = np.mean(self.X, axis=2), np.mean(self.Y, axis=2)
        u, v, _ = snap[3:-1]
        self.U, self.V = np.mean(u, axis=2), np.mean(v, axis=2)
        self.p = np.mean(snap[-1], axis=0)
        del u, v, snap

    def single_instance(self, ext):
        if ext == 'vti':
            snap = io.read_vti(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
        else:
            snap = io.read_vti(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
        # snap = np.array(snap).T
        return snap

    # TODO: There's some array mismatch bug in time_avg
    def time_avg(self, ext):
        snaps = np.array([])
        for idx, fn in enumerate(self.fns):
            if ext == 'vti':
                print(fn)
                snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
            else:
                snap = io.vtr_format_2d(os.path.join(self.datp_dir, self.fns[-1]), self.length_scale)
            snaps = np.append(snaps, snap)
        del snap
        # Time average the flow field snaps
        print(np.shape(snaps))
        t_mean = np.mean(snaps, axis=0)
        return t_mean

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

# TODO: add in POD modes using Mauliks PyParSVD
# TODO: add in phase average
