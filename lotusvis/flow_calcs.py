# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This class builds on the base class to calculate useful quantities
@contact: jmom1n15@soton.ac.uk
"""
import numpy as np

from lotusvis.flow_field import FlowBase


class Calculations(FlowBase):
    def __init__(self, sim_dir, fn_root, length_scale, ext='vti', **kwargs):
        super().__init__(sim_dir, fn_root, length_scale, ext, kwargs)

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


