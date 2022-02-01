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

    def __init__(self, sim_dir, fn_root, length_scale, **kwargs):
        self.sim_dir = sim_dir
        datp_dir = os.path.join(sim_dir, 'datp')
        rot = kwargs.get('rotation', 0)
        self.rot = rot / 180 * np.pi
        self.length_scale = length_scale
        # Find what you're looking for
        fns = [fn for fn in os.listdir(datp_dir) if fn.startswith(fn_root) and fn.endswith('.pvtr')]
        # Sort files
        fns = Tcl().call('lsort', '-dict', fns)

        if len(fns) > 1:
            print("More than one fn with this name. Taking time average.")
            # Store snapshots of field
            self.snaps = []
            for fn in fns:
                snap = io.format_2d(os.path.join(datp_dir, fn), self.length_scale, rotation=rot)
                self.snaps.append(snap)
            del snap
            # Time average the flow field snaps
            mean_t = np.mean(np.array(self.snaps).T, axis=1)
            self.X, self.Y = mean_t[0:2]
            self.u, self.v, self.w = mean_t[2:-1]
            self.U, self.V = np.mean(self.u, axis=2), np.mean(self.v, axis=2)
            self.p = np.mean(mean_t[-1], axis=0)
            del mean_t
        else:
            assert (len(fns) > 0), 'You dont have ' + fn_root + '.pvtr in your datp folder'
            self.X, self.Y, self.U, self.V, self.W, self.p = io.format_2d(os.path.join(datp_dir, fns[0]),
                                                                                     self.length_scale, rotation=rot)
            self.U, self.V = np.squeeze(self.U), np.squeeze(self.V)
            self.p = np.squeeze(self.p)
        self.z = np.ones(np.shape(self.X))

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

    def vort_mag(self):
        return io.vort(self.U, self.V, self.W, x=self.X, y=self.Y, z=self.z)

    def down_sample(self, skip=1):
        self.X, self.Y, self.U, self.V, self.p = np.mean(np.array(self.snaps[::(skip + 1)]).T, axis=1)
