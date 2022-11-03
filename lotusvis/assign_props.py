# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This is a class that assigns the main properties of the data to easily interface
              with other classes and packages.
@contact: jmom1n15@soton.ac.uk
"""
import numpy as np


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

