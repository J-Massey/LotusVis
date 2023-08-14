# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This script helps in reading and formatting data from outside the module
@contact: jmom1n15@soton.ac.uk
"""
import os
import warnings
from matplotlib import pyplot as plt

import numpy as np
import vtk


def read_vti(file, length_scale):
    warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
    reader = vtk.vtkXMLPImageDataReader()
    reader.SetFileName(file)
    reader.Update()
    data = reader.GetOutput()
    point_data = data.GetPointData()

    sh = data.GetDimensions()[::-1]

    velocity = np.array(point_data.GetVectors("Velocity")).reshape(sh + (len(sh),))
    u, v, w = np.einsum('ijkl -> ljki', velocity)

    p = np.array(point_data.GetScalars('Pressure')).reshape(sh)
    p = np.einsum('ijk -> jki', p)

    return np.array((u, v, w, p))


def generate_grid(sh, bounds, length_scale):
    xmin, xmax, ymin, ymax, zmin, zmax = bounds
    grid_x = np.linspace(xmin, xmax, sh[0])
    grid_y = np.linspace(ymin, ymax, sh[1])
    grid_z = np.linspace(zmin, zmax, sh[2])
    x, y, z = np.meshgrid(grid_x, grid_y, grid_z, indexing='xy')
    return x/length_scale, y/length_scale, z/length_scale


def sparse_vti_grid(sh, bounds, length_scale):
    xmin, xmax, ymin, ymax, zmin, zmax = bounds
    grid_x = np.linspace(xmin, xmax, sh[0])/length_scale
    grid_y = np.linspace(ymin, ymax, sh[1])/length_scale
    grid_z = np.linspace(zmin, zmax, sh[2])/length_scale
    return grid_x, grid_y, grid_z


if __name__ =="__main__":
    sim_dir = f"{os.getcwd()}/pytests/test_data"
    