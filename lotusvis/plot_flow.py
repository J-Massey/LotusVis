# # -*- coding: utf-8 -*-
# """
# @author: Jonathan Massey
# @description: Unpack flow field and plot the contours
# @contact: jmom1n15@soton.ac.uk
# """
#
# import matplotlib.colors as colors
# import matplotlib.patches as patches
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
# from mpl_toolkits.axes_grid1 import make_axes_locatable
#
# from lotusvis.flow_field import ReadIn
#
#
# def _rec(theta):
#     grey_color = '#dedede'
#     return patches.Rectangle((0, -1 / 91.42), 1., 1 / 45.71, -theta, linewidth=0.2, edgecolor='red',
#                              facecolor='red')
#
#
# class Plots(ReadIn):
#     def __init__(self, sim_dir, fn_root, length_scale, cmap=None):
#         super().__init__(sim_dir, fn_root, length_scale, span_avg=True)
#         self.cmap = cmap
#         self.mag = np.sqrt(self.V ** 2 + self.U ** 2)
#
#     @property
#     def vort(self):
#         dv_dx = np.gradient(self.V, axis=0, edge_order=2)
#         du_dy = np.gradient(self.U, axis=1, edge_order=2)
#         return dv_dx - du_dy
#
#     def plot_mag(self, fn_save, **kwargs):
#         plt.style.use(['science', 'grid'])
#         fig, ax = plt.subplots(figsize=(7, 5))
#         divider = make_axes_locatable(ax)
#         # Plot the window of interest
#         ax.set_xlim(kwargs.get('xlim', (np.min(self.X), np.max(self.X))))
#         ax.set_ylim(kwargs.get('ylim', (np.min(self.Y), np.max(self.Y))))
#
#         lim = [0, np.max(self.mag)]
#         lim = kwargs.get('lims', lim)
#
#         norm = colors.Normalize(vmin=lim[0], vmax=lim[1])
#         levels = kwargs.get('levels', 101)
#         step = kwargs.get('step', None)
#         if step is not None:
#             levels = np.arange(lim[0], lim[1] + step, step)
#         else:
#             levels = np.linspace(lim[0], lim[1], levels)
#
#         if not self.cmap:
#             _cmap = sns.color_palette("icefire", as_cmap=True)
#         else:
#             _cmap = self.cmap
#
#         cs = ax.contourf(self.X, self.Y, self.mag,
#                          levels=levels, vmin=lim[0], vmax=lim[1],
#                          norm=norm, cmap=_cmap, extend='both')
#         ax_cb = divider.new_horizontal(size="5%", pad=0.05)
#         fig.add_axes(ax_cb)
#         plt.colorbar(cs, cax=ax_cb)
#         ax_cb.yaxis.tick_right()
#         ax_cb.yaxis.set_tick_params(labelright=True)
#         # plt.setp(ax_cb.get_yticklabels()[::2], visible=False)
#         ax.set_aspect(1)
#
#         plt.savefig(fn_save, dpi=300, transparent=True)
#         plt.show()
#
#     def plot_vort(self, fn_save, **kwargs):
#         plt.style.use(['science', 'grid'])
#         fig, ax = plt.subplots(figsize=(7, 5))
#         divider = make_axes_locatable(ax)
#         # Plot the window of interest
#         ax.set_xlim(kwargs.get('xlim', (np.min(self.X), np.max(self.X))))
#         ax.set_ylim(kwargs.get('ylim', (np.min(self.Y), np.max(self.Y))))
#
#         bounds = np.max(np.array((abs(np.min(self.vort)), np.max(self.vort))))
#         lim = [-bounds, bounds]
#         lim = kwargs.get('lims', lim)
#
#         norm = colors.Normalize(vmin=lim[0], vmax=lim[1])
#         levels = kwargs.get('levels', 101)
#         step = kwargs.get('step', None)
#         if step is not None:
#             levels = np.arange(lim[0], lim[1] + step, step)
#         else:
#             levels = np.linspace(lim[0], lim[1], levels)
#
#         if not self.cmap:
#             _cmap = sns.color_palette("seismic", as_cmap=True)
#         else:
#             _cmap = self.cmap
#
#         cs = ax.contourf(self.X, self.Y, self.vort,
#                          levels=levels, vmin=lim[0], vmax=lim[1],
#                          norm=norm, cmap=_cmap, extend='both')
#         ax_cb = divider.new_horizontal(size="5%", pad=0.05)
#         fig.add_axes(ax_cb)
#         plt.colorbar(cs, cax=ax_cb)
#         ax_cb.yaxis.tick_right()
#         ax_cb.yaxis.set_tick_params(labelright=True)
#         # plt.setp(ax_cb.get_yticklabels()[::2], visible=False)
#         ax.set_aspect(1)
#
#         plt.savefig(fn_save, dpi=300, transparent=True)
#         plt.close()
#
#     def plot_pressure(self, fn_save, **kwargs):
#         plt.style.use(['science', 'grid'])
#         fig, ax = plt.subplots(figsize=(7, 5))
#         divider = make_axes_locatable(ax)
#         # Plot the window of interest
#         ax.set_xlim(kwargs.get('xlim', (np.min(self.X), np.max(self.X))))
#         ax.set_ylim(kwargs.get('ylim', (np.min(self.Y), np.max(self.Y))))
#
#         bounds = np.max(np.array((abs(np.min(self.p)), np.max(self.p))))
#         lim = [-bounds, bounds]
#         lim = kwargs.get('lims', lim)
#
#         norm = colors.Normalize(vmin=lim[0], vmax=lim[1])
#         levels = kwargs.get('levels', 101)
#         step = kwargs.get('step', None)
#         if step is not None:
#             levels = np.arange(lim[0], lim[1] + step, step)
#         else:
#             levels = np.linspace(lim[0], lim[1], levels)
#
#         if not self.cmap:
#             _cmap = sns.color_palette("seismic", as_cmap=True)
#         else:
#             _cmap = self.cmap
#
#         cs = ax.contourf(self.X, self.Y, self.p,
#                          levels=levels, vmin=lim[0], vmax=lim[1],
#                          norm=norm, cmap=_cmap, extend='both')
#         ax_cb = divider.new_horizontal(size="5%", pad=0.05)
#         fig.add_axes(ax_cb)
#         plt.colorbar(cs, cax=ax_cb)
#         ax_cb.yaxis.tick_right()
#         ax_cb.yaxis.set_tick_params(labelright=True)
#         # plt.setp(ax_cb.get_yticklabels()[::2], visible=False)
#         ax.set_aspect(1)
#
#         plt.savefig(fn_save, dpi=300, transparent=True)
#         plt.close()
#
#     # def plot_line(self, fn_save, **kwargs):
#     #     plt.style.use(['science', 'grid'])
#     #     fig, ax = plt.subplots(figsize=(8.5, 6))
#     #     plt.title(self.title)
#     #     divider = make_axes_locatable(ax)
#     #     # Plot the window of interest
#     #     ax.set_xlim(kwargs.get('xlim', (-0.2, 2.3)))
#     #     ax.set_ylimNone
#     #
#     #     if kwargs.get('rec', False):
#     #         rec = _rec(theta=12)
#     #         ax.add_patch(rec)
#     #
#     #     lim = [np.min(self.vals), np.max(self.vals)]
#     #     lim = kwargs.get('lims', lim)
#     #     # Put limits consistent with experimental data
#     #     norm = colors.Normalize(vmin=lim[0], vmax=lim[1])
#     #     levels = kwargs.get('levels', 6)
#     #     step = kwargs.get('step', None)
#     #     if step is not None:
#     #         lvls = np.arange(lim[0], lim[1] + step, step)
#     #     else:
#     #         lvls = np.linspace(lim[0], lim[1], levels)
#     #
#     #     cs = ax.contour(self.X, self.Y, (self.vals),
#     #                     levels=levels, vmin=lim[0], vmax=lim[1],
#     #                     norm=norm, colors=kwargs.get('colors', sns.color_palette("tab10")))
#     #     ax.clabel(cs, cs.levels[2::2], inline_spacing=1, inline=1, fontsize=12, fmt='%1.2f')
#     #     del self.X, self.Y, self.vals
#     #     ax.set_aspect(1)
#     #
#     #     plt.savefig(fn_save, dpi=300, transparent=True)
#     #     # plt.close()
#     #
#     # def plot_grid(self, fn_save):
#     #     plt.style.use(['science'])
#     #     fig, ax = plt.subplots(figsize=(7, 5))
#     #     ax.set_xlim((-4, 6))
#     #     ax.set_ylim((-2.5, 2.5))
#     #
#     #     ax.set_xlabel(r'$x/c$')
#     #     ax.set_ylabel(r'$y/c$')
#     #
#     #     ax.plot(self.X, self.Y, c='k', linewidth=0.2)
#     #     ax.plot((self.X), (self.Y), c='k', linewidth=0.2)
#     #
#     #     rec = _rec(theta=0)
#     #     ax.add_patch(rec)
#     #     # ax.set_xticks()
#     #
#     #     del self.X, self.Y, self.vals
#     #     ax.set_aspect(1)
#     #     ax.grid(False)
#     #
#     #     plt.savefig(fn_save, dpi=800, transparent=True)
#     #     plt.show()
#
#     def stack_contours(self, interesting_contour):
#         """
#         Stack contours from two different flow fields on top of each other for a good comparison.
#         Returns: A contour plot
#
#         """
