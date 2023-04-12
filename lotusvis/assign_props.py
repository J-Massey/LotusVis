# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This is a class that assigns the main properties of the data to easily interface
              with other classes and packages.
@contact: jmom1n15@soton.ac.uk
"""
import numpy as np
from skimage.measure import find_contours
from scipy import interpolate


class AssignProps:
    """
    Read in a snapshot of a data field and output the main properties.
    """
    def __init__(self, snap):
        self.snap = snap
        del snap
        self.X, self.Y, self.Z = self.snap[0:3]
        u, v, w = self.snap[3:-1]
        self.U, self.V, self.W = u, v, w
        self.p = self.snap[-1]
        del u, v, w, self.snap
    
    @property
    def magnitude(self):
        return np.sqrt(self.Z ** 2 + self.V ** 2 + self.U ** 2)

    @property
    def vorticity_z(self):
        dv_dx = np.gradient(self.V, axis=0, edge_order=2)
        du_dy = np.gradient(self.U, axis=1, edge_order=2)
        return dv_dx - du_dy

    @property
    def vorticity_x(self):
        dv_dz = np.gradient(self.V, axis=2, edge_order=2)
        dw_dy = np.gradient(self.W, axis=1, edge_order=2)
        return dv_dz - dw_dy

    @property
    def vorticity_y(self):
        du_dz = np.gradient(self.U, axis=2, edge_order=2)
        dw_dx = np.gradient(self.W, axis=0, edge_order=2)
        return du_dz - dw_dx
    
    def spline_cont(self, contour=1, stretch=4.):
        """
        This only works for 2-D at the moment.
        Only works for single stretch.
        """
        contours = find_contours(self.p, contour)
        # Extract the outermost contour
        boundary_coords = contours[0]
        
        xc, yc = boundary_coords[:, 1].astype(float), boundary_coords[:, 0].astype(float)


        interp_x, interp_y = splineit(xc, yc, len(xc))

        ddx = np.gradient(interp_x)
        ddy = np.gradient(interp_y, stretch)
        mag = np.sqrt(ddx**2 + ddy**2)

        nx = -ddy / mag
        ny = ddx / mag
        return nx, ny


def splineit(x, y, n):
    # get the cumulative distance along the contour
    dist = np.sqrt((x[:-1] - x[1:])**2 + (y[:-1] - y[1:])**2)
    dist_along = np.concatenate(([0], dist.cumsum()))

    # build a spline representation of the contour
    spline, u = interpolate.splprep([x, y], u=dist_along, s=0)

    # resample it at smaller distance intervals to take gradient
    interp_d = np.linspace(dist_along[0], dist_along[-1], n)
    interp_x, interp_y = interpolate.splev(interp_d, spline)
    return (interp_x, interp_y)

