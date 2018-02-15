import numpy as np
import matplotlib.pyplot as plt
cmap = ['b', 'm', 'c', 'g', 'y', 'r', 'k']


def plot_orbit(ax, system, i_planet):
    x = system.cartesian[i_planet][:, 0]
    y = system.cartesian[i_planet][:, 1]
    plot = plt.plot(x, y, color=cmap[i_planet])
    return plot


def plot_position(ax, system, i_planet,
                  t_res=100, t_max=1000, t_min=0):
    x = system.cartesian[i_planet][t_min:t_max:t_res, 0]
    y = system.cartesian[i_planet][t_min:t_max:t_res, 1]
    plot = plt.scatter(x, y, color=cmap[i_planet])
    ax.add_artist(plot)
    return plot


def plot_observation(ax, system, i_planet=1, i_reference=0,
                     t_res=100, t_max=1000, t_min=0):
    style = 'dotted'
    x0 = np.zeros(len(system.cartesian[i_planet][t_min:t_max:t_res, 0]))
    y0 = np.zeros(len(system.cartesian[i_planet][t_min:t_max:t_res, 0]))
    x1 = system.cartesian[i_planet][t_min:t_max:t_res, 0]
    y1 = system.cartesian[i_planet][t_min:t_max:t_res, 1]
    if(i_reference >= 0):
        style = 'solid'
        x0 = system.cartesian[i_reference][t_min:t_max:t_res, 0]
        y0 = system.cartesian[i_reference][t_min:t_max:t_res, 1]

    for i, t in enumerate(x1):
        x = np.array([x0[i], x1[i]])
        y = np.array([y0[i], y1[i]])
        plot = plt.Line2D(x, y, color='k', linewidth=0.5, linestyle=style)
        ax.add_artist(plot)
