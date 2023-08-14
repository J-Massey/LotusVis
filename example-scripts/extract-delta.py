
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from matplotlib.lines import Line2D
import numpy as np


from lotusvis.plot_flow import Plots
from lotusvis.flow_field import ReadIn
from lotusvis.assign_props import AssignProps

from matplotlib import pyplot as plt
import seaborn as sns
import scienceplots
plt.style.use(["science"])
plt.rcParams["font.size"] = "10.5"



def extract_delta(re):
    # Extract the delta profiles for a given Reynolds number
    sim_dir = f"{os.getcwd()}/analysis/visualise-outer-scale/{re}k/0-2d"
    vel = ReadIn(sim_dir, 'fluid', 1024, ext='vti')
    profiles = np.zeros((np.shape(vel.snaps)[0], np.shape(vel.snaps)[2]))
    ys = np.zeros((np.shape(vel.snaps)[0], np.shape(vel.snaps)[2])) 
    for idx, s in enumerate(vel.snaps):
        snap = AssignProps(s)
        index = np.argmin(abs(np.mean(snap.X, axis=2)-1))
        profiles[idx] = np.ravel(np.mean(snap.U, axis=2)[:, index])
        ys[idx] = np.ravel(np.mean(snap.Y, axis=2)[:, index])
    return profiles, ys


def delta(profs):
    '''
    Compute the mean positive and negative bl thickness.
    '''

    # Unpack the profiles
    u, y = profs

    # Preallocate the arrays
    positive, negative = np.empty(len(u)), np.empty(len(u))

    # Loop through the profiles
    for idx in range(len(u)):
        u = profs[0][idx]
        y = profs[1][idx]

        # Find the indices where u>0
        pos = np.where(u>0.)[0]

        # Split the profiles at the indices where the difference between indices is not equal to 1
        yout = np.split(y[pos],np.where(np.diff(pos)!=1)[0]+1)
        uout = np.split(u[pos],np.where(np.diff(pos)!=1)[0]+1)

        bl = []
        for jdx in range(2):
            maxi, mini = np.max(uout[jdx]), np.min(uout[jdx])
            pos_max, pos_min = np.where(uout[jdx]==maxi)[0], np.where(uout[jdx]==mini)[0]
            bls = abs(yout[jdx][pos_max]-yout[jdx][pos_min])
            bl.append(bls)

        # Distinguish between pos and neg pressure gradients
        positive[idx] = min(bl)
        negative[idx] = max(bl)

    return np.mean(positive), np.mean(negative)


def get_bl(profs):
    u, y = profs
    us, ys = [], []
    for idx in range(len(u)):
        u = profs[0][idx]
        y = profs[1][idx]

        pos = np.where(u>0.)[0]
        us.append(u[pos])
        ys.append(y[pos])
    return us, ys


def plot_re(ax, col, re):
    us, ys = get_bl(extract_delta(re))

    for idx in range(0, len(us)//2, 2):
        ax.plot(
            us[idx], ys[idx],
            color=col,
            ls='-.',
            alpha=0.7,
        )


def re_legend():
    legend_elements = [
        Line2D(
            [0],
            [0],
            ls="-.",
            label=r"$Re=6,000$",
            c=sns.color_palette('colorblind')[1],
            # marker="^",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="-.",
            label=r"$Re=12,000$",
            c=sns.color_palette('colorblind')[0],
            # marker="P",
            markerfacecolor="none",
        ),
        Line2D(
            [0],
            [0],
            ls="-.",
            label=r"$Re=24,000$",
            c=sns.color_palette('colorblind')[2],
            # marker="o",
            markerfacecolor="none",
        ),
    ]
    return legend_elements

        
def plot_bl_ontop():
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlabel(r"$u$")
    ax.set_ylabel(r"$y$")

    plot_re(ax, sns.color_palette('colorblind')[1], 6)
    plot_re(ax, sns.color_palette('colorblind')[0], 12)
    plot_re(ax, sns.color_palette('colorblind')[2], 24)

    ax.legend(handles=re_legend(), loc=2)
    
    plt.savefig(f"{os.getcwd()}/analysis/figures/bl-on-top.pdf", dpi=200, transparent=True)


def plot_bl_seperated():
    fig, ax = plt.subplots(3, figsize=(4,4))
    ax[2].set_xlabel(r"$u$")
    ax[1].set_ylabel(r"$y$")
    [ax.set_xticks([]) for ax in ax[:-1]]

    plot_re(ax[0], sns.color_palette('colorblind')[1], 6)
    plot_re(ax[1], sns.color_palette('colorblind')[0], 12)
    plot_re(ax[2], sns.color_palette('colorblind')[2], 24)

    for idx, ax in enumerate(ax):
        l2 = ax.legend(labels=[f"$\delta={delta(extract_delta(res[idx]))[0]:.3f}$"], loc=4)
        l1 = ax.legend(handles=[re_legend()[idx]], loc=2)
        ax.add_artist(l2)

    
    plt.savefig(f"{os.getcwd()}/analysis/figures/bl.pdf", dpi=200, transparent=True)


if __name__ == "__main__":
    res = [6, 12, 24]
    plot_bl_seperated()
    plot_bl_ontop()
    print(delta(extract_delta(12)))