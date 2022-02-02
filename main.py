# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

from lotusvis.plot_flow import *
from lotusvis.flow_field import *


# def fluid_vis(sim_dir, length_scale):
#     os.chdir(sim_dir)
#     print(os.getcwd(), length_scale)
#     os.system('mkdir -p vis_dump')
#     snap = base.FileHandler(os.path.join(sim_dir), 'fluid', length_scale)
#     flow = base.FlowBase(snap.snap, slice=True)
#     print(np.shape(flow.x), np.shape(flow.u))
#     save_figure_to = os.path.join(sim_dir, 'vis_dump/test.png')
#     plotter.plot_fill(flow.x, flow.y, flow.x, save_figure_to,
#                       title='Test new plot method', lims=[0, 1.4], levels=101)


if __name__ == "__main__":
    plt.style.use(['science', 'grid'])
    data_root = '/run/user/1000/gvfs/sftp:host=ssh.soton.ac.uk,user=jmom1n15/research/sharkdata/' \
                'research_filesystem/flat_plate/AoA_8/smooth/res_test/batch1/192'
    # data_root = sys.argv[1]
    # length_scale = sys.argv[2]
    plot = Plots(data_root, 'fluid', length_scale=192)
    plot.plot_vort(os.path.join(data_root, 'vis_dump/vort.png'))
    plot.plot_mag(os.path.join(data_root, 'vis_dump/mag.png'))
    plot.plot_pressure(os.path.join(data_root, 'vis_dump/pressure.png'))
