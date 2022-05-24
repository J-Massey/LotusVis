# -*- coding: utf-8 -*-
"""
@author: Jonathan Massey
@description: This is a class that assigns the main properties of the data to easily interface
              with other classes and packages.
@contact: jmom1n15@soton.ac.uk
"""


class AssignProps:
    """
    Read in a snapshot of a data field and output the main properties.
    """
    def __init__(self, snap):
        self.snap = snap
        del snap

        self.X, self.Y, self.Z, self.U, self.V, self.W, self.p = None, None, None, None, None, None, None
        self.props()

    def props(self):
        self.X, self.Y, self.Z = self.snap[0:3]
        u, v, w = self.snap[3:-1]
        self.U, self.V, self.W = u, v, w
        self.p = self.snap[-1]
        del u, v, w, self.snap

