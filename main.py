# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from lotusvis.plot_flow import *
from lotusvis.flow_field import *


def fluid_vis(sim_dir, length_scale):
    os.chdir(sim_dir)
    print(os.getcwd(), length_scale)
    os.system('mkdir -p vis_dump')
    plot = Plots(data_root, 'fluid', length_scale=length_scale)
    plot.plot_vort(os.path.join(data_root, 'vis_dump/vort.png'))
    plot.plot_mag(os.path.join(data_root, 'vis_dump/mag.png'))
    plot.plot_pressure(os.path.join(data_root, 'vis_dump/pressure.png'))


if __name__ == "__main__":
    plt.style.use(['science', 'grid'])
    data_root = '/run/user/1000/gvfs/sftp:host=iridis5_d.soton.ac.uk,user=jmom1n15/' \
                'scratch/jmom1n15/Lotus/swimming_plate/rough/res_test/batch0/512'
    fluid_vis(data_root, 512)

