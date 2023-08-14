# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This script helps in reading and formatting data from outside the module
@contact: jmom1n15@soton.ac.uk
"""
from pathlib import Path
import warnings
from matplotlib import pyplot as plt

import numpy as np
import vtk


def read_vtr(fn):
    warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
    reader = vtk.vtkXMLPRectilinearGridReader()
    reader.SetFileName(fn)
    reader.Update()
    data = reader.GetOutput()
    pointData = data.GetPointData()
    sh = data.GetDimensions()[::-1]
    ndims = len(sh)

    # get vector field
    try:
        v = np.array(pointData.GetVectors("Velocity")).reshape(sh + (ndims,))
        vec = []
        for d in range(ndims):
            a = np.array(v[..., d])
            vec.append(a)
        vec = np.array(vec)
        # get scalar field
        sca = np.array(pointData.GetScalars('Pressure')).reshape(sh + (1,))

        # get grid
        x = np.array(data.GetXCoordinates())
        y = np.array(data.GetYCoordinates())
        z = np.array(data.GetZCoordinates())

        return np.array(np.transpose(vec, (0, 3, 2, 1)), np.transpose(sca, (0, 3, 2, 1)), np.array((x, y, z)))
    except ValueError:
        print('\n' + fn + ' corrupt, skipping for now')


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

# def vtr_format_2d(fn, length_scale, rotation=0):
#     """
#     Rotates and scales vtr file
#     Args:
#         fn: The path to the 'datp' folder
#         length_scale: length scale of the simulation
#         rotation: Rotate the grid. If you're running a simulation with
#                   an angle of attack, it's better to rotate the flow than
#                   the foil because of the meshing.

#     Returns: X, Y - coordinates (useful for indexing)
#              U, V - rotated velocity components
#              w    - un-rotated z velocity component
#              p    - pressure field

#     """
#     rot = rotation / 180 * np.pi
#     data = read_vtr(fn)
#     # Get the grid
#     x, y, z = data[2]
#     X, Y = np.meshgrid(x / length_scale, y / length_scale)
#     X = np.cos(rot) * X + np.sin(rot) * Y
#     Y = -np.sin(rot) * X + np.cos(rot) * Y

#     u, v, w = data[0]
#     U = np.cos(rot) * u + np.sin(rot) * v
#     V = -np.sin(rot) * u + np.cos(rot) * v
#     p = data[1]
#     p = np.reshape(p, [np.shape(p)[0], np.shape(p)[2], np.shape(p)[3]])
#     return X, Y, U, V, w, p

if __name__ =="__main__":
    sim_dir = f"{Path.cwd()}/pytests/test_data"
    