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
        dv_dx = np.gradient(self.V, axis=1, edge_order=2)
        du_dy = np.gradient(self.U, axis=0, edge_order=2)
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
    
    def boundary_coords(self, contour=1.):
        """
        Takes in the contour level, which is a contour of the distance function.
        Returns the y and x coordinates of this boundary.
        """
        dis = self.p.mean(axis=2)
        contours = find_contours(dis, contour)

        # Extract the outermost contour positions
        boundary_coords = contours[0]
        return boundary_coords
    
    def norm_vecs(self, contour=1., stretch=4.):
        """
        This only works for 2-D at the moment.
        """
        # Get distance function
        
        yc, xc = self.boundary_coords(contour).T.astype(float)
        interp_x, interp_y = splineit(xc, yc, len(xc))
        
        # get gradients
        ddx = np.gradient(interp_x)
        ddy = np.gradient(interp_y, stretch)

        # normal and normalise
        mag = np.sqrt(ddx**2 + ddy**2)
        nx = -ddy / mag
        ny = ddx / mag
        return nx, ny
    
    def body_contour_idx(self, contour=1.):
        # get index positions of the vectors
        cont_coords = self.boundary_coords(contour).T.astype(int)
        return cont_coords
    
    def tang_vecs(self, contour=1., stretch=4.):
        t1, t2 = self.norm_vecs(contour, stretch)
        return t2, -t1

    def scaled_body_contour_idx(self, contour=1., SF=1):
        # Flag: untested
        # get index positions of the vectors
        cont_coords = self.boundary_coords(contour).T.astype(int)
        original_origin = cont_coords[0].mean(), cont_coords[1].mean()

        scale_coords = self.boundary_coords(contour) * SF
        scale_coords = scale_coords.T.astype(int)
        scaled_origin = cont_coords[0].mean(), cont_coords[1].mean()
        return scale_coords - original_origin + scaled_origin


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

