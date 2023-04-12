#  ToDo: this should be a class method in the LotusVis module
# This is a sample Python script.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cmath
import os
from pathlib import Path
import numpy as np
from scipy import interpolate
from scipy.interpolate import splprep, splev
from skimage import measure
from skimage.measure import find_contours


# from lotusvis.plot_flow import Plots
from lotusvis.flow_field import ReadIn
from lotusvis.assign_props import AssignProps

from matplotlib import colors, pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable




def body_cont(cont=1.0):
    """
    Take in a contour and return the tuple to index the locations
    of the body boundary.
    :param cont: contour value
    :return: tuple of x and y locations
    """
    pressure = bsnap.p.mean(axis=2)
    contours = find_contours(pressure, cont)
    # Extract the outermost contour
    boundary_coords = contours[0]
    return boundary_coords


def body_coords(boundary_coords):
    # Find the contour location for the body boundary, don't know why splprep rejects this
    cont_coords = boundary_coords[:, 0].astype(int), boundary_coords[:, 1].astype(int)
    # xc, yc = (x[*cont_coords]), (y[*cont_coords])
    return cont_coords


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


def body_normal_vectors(boundary_coords, stretch=4):
    """
    Calculate the normal vectors to the body boundary.
    :param boundary_coords: tuple of x and y coordinates of the body boundary
    :param stretch: The grid refinement ratio in the y-direction.
    :return: tuple of x and y components of the normal vectors
    """
    # Get coordinates of the body boundary
    xc, yc = boundary_coords[:, 1].astype(float), boundary_coords[:, 0].astype(float)


    interp_x, interp_y = splineit(xc, yc, len(xc))

    ddx = np.gradient(interp_x)
    ddy = np.gradient(interp_y, stretch)
    mag = np.sqrt(ddx**2 + ddy**2)

    nx = -ddy / mag
    ny = ddx / mag

    return nx, ny


def plot_u_tau():
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.set_xlim(-0.25, 1.5)
    ax.set_ylim(-0.3, 0.3)

    boundary_coords = body_cont()
    cont_locs = body_coords(boundary_coords)
    norm_vecs = body_normal_vectors(boundary_coords)

    # Isolate the top half of the foil
    x, y = fsnap.X.mean(axis=2), fsnap.Y.mean(axis=2)
    top = norm_vecs[1] >= 0

    ax.contourf(
        x, y, body_mask(fsnap.vorticity_z.mean(axis=2)), levels=100, cmap="RdBu_r"
    )

    skip = (slice(None, None, 150))

    ax.quiver(
        x[*cont_locs][top][skip],
        y[*cont_locs][top][skip],
        norm_vecs[0][top][skip],
        norm_vecs[1][top][skip],
        color="red",
        # label="Top surface",
        # headwidth=1,
        scale=20,
        # headlength=4,
    )
    ax.set_aspect(1)
    ax.legend()
    plt.savefig(
        f"{Path.cwd()}/2d-extract-profiles/4096.png", dpi=1000, transparent=False
    )


def plot(snap, target, fn_save, **kwargs):
    fig, ax = plt.subplots(figsize=(7, 5))
    divider = make_axes_locatable(ax)
    x, y = snap.X.mean(axis=2), snap.Y.mean(axis=2)
    # Plot the window of interest
    ax.set_xlim(kwargs.get("xlim", (np.min(x), np.max(x))))
    ax.set_ylim(kwargs.get("ylim", (np.min(y), np.max(y))))

    lim = [0, np.max(target)]
    lim = kwargs.get("lims", lim)

    norm = colors.Normalize(vmin=lim[0], vmax=lim[1])
    levels = kwargs.get("levels", 101)
    step = kwargs.get("step", None)
    if step is not None:
        levels = np.arange(lim[0], lim[1] + step, step)
    else:
        levels = np.linspace(lim[0], lim[1], levels)

    _cmap = sns.color_palette("seismic", as_cmap=True)
    cs = ax.contourf(
        x,
        y,
        target,
        levels=levels,
        vmin=lim[0],
        vmax=lim[1],
        norm=norm,
        cmap=_cmap,
        extend="both",
    )
    ax_cb = divider.new_horizontal(size="5%", pad=0.05)
    fig.add_axes(ax_cb)
    plt.colorbar(cs, cax=ax_cb)
    ax_cb.yaxis.tick_right()
    ax_cb.yaxis.set_tick_params(labelright=True)
    # plt.setp(ax_cb.get_yticklabels()[::2], visible=False)
    ax.set_aspect(1)

    plt.savefig(fn_save, dpi=600, transparent=False)


def delta(profs):
    """
    Compute the mean positive and negative bl thickness.
    """

    # Unpack the profiles
    u, y = profs

    # Preallocate the arrays
    positive, negative = np.empty(len(u)), np.empty(len(u))

    # Loop through the profiles
    for idx in range(len(u)):
        u = profs[0][idx]
        y = profs[1][idx]

        # Find the indices where u>0
        pos = np.where(u > 0.0)[0]

        # Split the profiles at the indices where the difference between indices is not equal to 1
        # This identifies the body and splits either side
        yout = np.split(y[pos], np.where(np.diff(pos) != 1)[0] + 1)
        uout = np.split(u[pos], np.where(np.diff(pos) != 1)[0] + 1)

        bl = []
        for jdx in range(2):
            # Get the maximum and minimum values from each top and bottom half
            maxi, mini = np.max(uout[jdx]), np.min(uout[jdx])
            # Find the indices where the maximum and minimum values are
            pos_max, pos_min = (
                np.where(uout[jdx] == maxi)[0],
                np.where(uout[jdx] == mini)[0],
            )
            if pos_max.size > 1 or pos_min.size > 1:
                bls = abs(yout[jdx][pos_max] - yout[jdx][pos_min]).mean()
            else:
                bls = abs(yout[jdx][pos_max] - yout[jdx][pos_min])
            bl.append(bls)
        # print(bl, np.shape(bl))

        # Distinguish between pos and neg pressure gradients
        positive[idx] = min(bl)
        negative[idx] = max(bl)

    return positive, negative


def get_bl(profs):
    u, y = profs
    us, ys = [], []
    for idx in range(len(u)):
        u = profs[0][idx]
        y = profs[1][idx]

        pos = np.where(u > 0.0)[0]
        us.append(u[pos])
        ys.append(y[pos])
    return us, ys



if __name__ == "__main__":
    sim_dir = f"{Path.cwd()}/2d-extract-profiles/4096"
    sim = ReadIn(sim_dir, "body", 4096, ext="vti")
    snaps = sim.snaps()
    bsnap = AssignProps(snaps[0])
    sim = ReadIn(sim_dir, "fluid", 4096, ext="vti")
    snaps = sim.snaps()
    fsnap = AssignProps(snaps[0])
    # print((body_idx()))/
    plot_u_tau()
