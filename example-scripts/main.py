# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from lotusvis.plot_flow import *
from lotusvis.flow_field import *


def fluid_vis(length_scale):
    sim_dir = os.getcwd()
    os.chdir(sim_dir)
    os.system('mkdir -p vis_dump')
    try:
        plot = Plots(sim_dir, 'fluid', length_scale=length_scale)
        # plot.plot_vort(os.path.join(sim_dir, 'vis_dump/vort.png'))
        plot.plot_mag(os.path.join(sim_dir, 'vis_dump/mag.png'))
        # plot.plot_pressure(os.path.join(sim_dir, 'vis_dump/pressure.png'))
    except FileNotFoundError:
        print('Simulation probably failed')


if __name__ == "__main__":
    c = 256
    fluid_vis(c)

