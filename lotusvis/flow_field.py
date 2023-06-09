# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This is a class that defines the useful quantities of flow field data.
@contact: jmom1n15@soton.ac.uk
"""

from genericpath import exists
from itertools import count
import os
import time
from tkinter import Tcl

import numpy as np
from tqdm import tqdm
import lotusvis.io as io
import lotusvis.snap_iterator as snap_iterator
from lotusvis.assign_props import AssignProps


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
    
    def snap_iterator(self):
        return snap_iterator.Fn(self.fns)

    def next_snap(self):
        """
        Iterator that gets the next timestep and returns a snap.
        """
        for n_fn in self.snap_iterator():
            snap = io.read_vti(os.path.join(self.datp_dir, n_fn), self.length_scale)
            yield snap.reshape(1, *np.shape(snap))

    def snaps(self, save=True, part=True, save_path=None):
        """
        This function reads in the data from the paraview files saves as an binary, and
        returns a numpy array of the data.
        :param save: If true, the data will be saved as a binary file.
        :param part: If true, only the first snapshot will be saved.
        :return: A numpy array of the data.
        """
        try:
            if part and exists(os.path.join(self.datp_dir, f'{self.fn_root}-part.npy')):
                snaps = np.load(os.path.join(self.datp_dir, f'{self.fn_root}-part.npy'))
            elif not part and exists(os.path.join(self.datp_dir, f'{self.fn_root}.npy')):
                snaps = np.load(os.path.join(self.datp_dir, f'{self.fn_root}.npy'))
            elif part:
                snap = io.read_vti(os.path.join(self.datp_dir, self.fns[0]), self.length_scale)
                snaps = snap.reshape(1, *np.shape(snap))
                if save:
                    np.save(os.path.join(self.datp_dir, f'{self.fn_root}-part.npy'), snaps)
            else:
                snaps = np.empty(self.init_snap_array())
                for idx, fn in tqdm(enumerate(self.fns)):
                    snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
                    snaps[idx] = np.array(snap)
                    del snap
                if save:
                    if save_path is not None:
                        np.save(os.path.join(save_path, f'{self.fn_root}.npy'), snaps)
                    else:
                        np.save(os.path.join(self.datp_dir, f'{self.fn_root}.npy'), snaps)
            return snaps
        except MemoryError:
            print('Not enough memory to load all the data, at once saving individual time steps as binary and trying again')
            try:
                for idx, fn in tqdm(enumerate(self.fns)):
                    snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
                    np.save(os.path.join(self.datp_dir, f'{self.fn_root}{idx}.npy'), snap)
                    del snap
            except MemoryError:
                print('Not enough memory to load a single time step. Bigger machine?')

    def save_vorticity_field(self, save_path="None"):
        """
        This function reads in the data from the paraview files saves as an binary, and
        returns a numpy array of just the vorticity field.
        :param save: If true, the data will be saved as a binary file.
        :param part: If true, only the first snapshot will be saved.
        :return: A numpy array of the data.
        """
        try:
            snaps = np.empty(self.init_snap_array())
            for idx, fn in tqdm(enumerate(self.fns)):
                snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
                snaps[idx] = np.array(snap)
                del snap
            snaps = AssignProps(snaps, self.length_scale).vorticity_z
            if save_path is not "":
                np.save(os.path.join(save_path, f'{self.fn_root}_vortz.npy'), snaps)
            else:
                np.save(os.path.join(self.datp_dir, f'{self.fn_root}_vortz.npy'), snaps)
            print('Vorticity field saved')
            return snaps
        except MemoryError:
            print('Not enough memory to load all the data, at once saving individual time steps as binary and trying again')
            try:
                self.vort_low_memory_saver(save_path)
            except MemoryError:
                print('Not enough memory to load a single time step. Bigger machine?')

    def vort_low_memory_saver(self, save_path=""):
        for idx, fn in tqdm(enumerate(self.fns)):
            snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
            snap = AssignProps(snap.reshape(1, *np.shape(snap)), self.length_scale).vorticity_z
            np.save(os.path.join(save_path, f'{self.fn_root}_vortz{idx}.npy'), snap)
            del snap

    def u_low_memory_saver(self, save_path=""):
        for idx, fn in tqdm(enumerate(self.fns)):
            snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
            snap = AssignProps(snap.reshape(1, *np.shape(snap)), self.length_scale).U
            np.save(os.path.join(save_path, f'{self.fn_root}_vortz{idx}.npy'), snap)
            del snap

    def v_low_memory_saver(self, save_path=""):
        for idx, fn in tqdm(enumerate(self.fns)):
            snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
            snap = AssignProps(snap.reshape(1, *np.shape(snap)), self.length_scale).V
            np.save(os.path.join(save_path, f'{self.fn_root}_vortz{idx}.npy'), snap)
            del snap

    def save_sdf(self, save_path=None):
        """
        This function reads in the data from the paraview files saves as an binary, and
        returns a numpy array of just the sdf field of the body.
        :param save: If true, the data will be saved as a binary file.
        :param part: If true, only the first snapshot will be saved.
        :return: A numpy array of the data.
        """
        try:
            snaps = np.empty(self.init_snap_array())
            for idx, fn in tqdm(enumerate(self.fns)):
                snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
                snaps[idx] = np.array(snap)
                del snap
            snaps = AssignProps(snaps, self.length_scale).p
            if save_path is not None:
                np.save(os.path.join(save_path, f'{self.fn_root}_p.npy'), snaps)
            else:
                np.save(os.path.join(self.datp_dir, f'{self.fn_root}_p.npy'), snaps)
            print('SDF/pressure field saved')
            return snaps
        except MemoryError:
            print('Not enough memory to load all the data, at once saving individual time steps as binary and trying again')
            try:
                for idx, fn in tqdm(enumerate(self.fns)):
                    snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
                    snap = AssignProps(snap, self.length_scale).p
                    np.save(os.path.join(self.datp_dir, f'{self.fn_root}_p{idx}.npy'), snap)
                    del snap
                return snap
            except MemoryError:
                print('Not enough memory to load a single time step. Bigger machine?')

    def save_sdf_low_memory(self, save_path=""):
        for idx, fn in tqdm(enumerate(self.fns)):
            snap = io.read_vti(os.path.join(self.datp_dir, fn), self.length_scale)
            snap = AssignProps(snap.reshape(1, *np.shape(snap)), self.length_scale).p
            np.save(os.path.join(save_path, f'{self.fn_root}_p{idx}.npy'), snap)
            del snap


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
