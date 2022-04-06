# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This script helps in reading and formatting data from outside the module
@contact: jmom1n15@soton.ac.uk
"""
import numpy as np
import vtk
import warnings


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

        return np.transpose(vec, (0, 3, 2, 1)), np.transpose(sca, (0, 3, 2, 1)), np.array((x, y, z))
    except ValueError:
        print('\n' + fn + ' corrupt, skipping for now')


def read_vti(file):
    warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
    reader = vtk.vtkXMLPImageDataReader()
    reader.SetFileName(file)
    reader.Update()
    data = reader.GetOutput()
    pointData = data.GetPointData()

    sh = data.GetDimensions()[::-1]
    ndims = len(sh)

    # get vector field
    v = np.array(pointData.GetVectors("Velocity")).reshape(sh + (ndims,))
    vec = []
    for d in range(ndims):
        a = v[..., d]
        vec.append(a)
    # get scalar field
    sca = np.array(pointData.GetScalars('Pressure')).reshape(sh + (1,))

    # Format values
    U, V, W = np.transpose(np.array(vec), (0, 3, 2, 1))
    p = np.transpose(sca, (0, 3, 2, 1))
    p = np.reshape(p, [np.shape(p)[0], np.shape(p)[2], np.shape(p)[3]])

    grid = generate_grid(np.shape(U), data)

    return (U, V, W), p, grid


def generate_grid(shape, data):
    # Generate grid
    # nPoints = dat.GetNumberOfPoints()
    xmin, xmax, ymin, ymax, zmin, zmax = data.GetBounds()
    # grid3D = np.mgrid[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1]
    gridx = np.linspace(xmin, xmax, shape[0])
    gridy = np.linspace(ymin, ymax, shape[1])
    gridz = np.linspace(zmin, zmax, shape[2])
    grid = np.array((gridx, gridy, gridz))
    return grid


# TODO: Get rid of the format crap
def vti_format(fn, length_scale):
    """
    Rotates and scales vti file
    Args:
        fn: The path to the 'datp' folder
        length_scale: length scale of the simulation

    Returns: X, Y - coordinates (useful for indexing)
             U, V - rotated velocity components
             w    - un-rotated z velocity component
             p    - pressure field

    """
    data = read_vti(fn)
    # Get the grid
    x, y, z = data[2]
    X, Y, Z = np.meshgrid(x / length_scale, y / length_scale, z/length_scale)
    U, V, W = data[0]
    p = data[1]
    return X, Y, Z, U, V, W, p


def vtr_format_2d(fn, length_scale, rotation=0):
    """
    Rotates and scales vtr file
    Args:
        fn: The path to the 'datp' folder
        length_scale: length scale of the simulation
        rotation: Rotate the grid. If you're running a simulation with
                  an angle of attack, it's better to rotate the flow than
                  the foil because of the meshing.

    Returns: X, Y - coordinates (useful for indexing)
             U, V - rotated velocity components
             w    - un-rotated z velocity component
             p    - pressure field

    """
    rot = rotation / 180 * np.pi
    data = read_vtr(fn)
    # Get the grid
    x, y, z = data[2]
    X, Y = np.meshgrid(x / length_scale, y / length_scale)
    X = np.cos(rot) * X + np.sin(rot) * Y
    Y = -np.sin(rot) * X + np.cos(rot) * Y

    u, v, w = data[0]
    U = np.cos(rot) * u + np.sin(rot) * v
    V = -np.sin(rot) * u + np.cos(rot) * v
    p = data[1]
    p = np.reshape(p, [np.shape(p)[0], np.shape(p)[2], np.shape(p)[3]])
    return X, Y, U, V, w, p
