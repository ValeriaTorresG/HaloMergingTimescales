import sys
sys.path.append('/net/hypernova/data2/BOOMPJE/code/ic_generation/')
import numpy as np
import read_tipsy
import os
from sphviewer.tools import QuickView

import matplotlib.pyplot as plt
from matplotlib import animation, rc
import matplotlib
plt.rcParams['figure.dpi'] = 360
matplotlib.rcParams['animation.embed_limit'] = 2**128
matplotlib.rcParams['text.usetex'] = True
rc("animation", html = "jshtml")


#!find path given a simulation id

path = input()
print(path)


#! load simulation data from tipsy file
def load_data(directory):
    files = [f for f in os.listdir(directory) if f.startswith('evolution')]
    files.sort()
    num_files = len(files)
    pos, time, vel, par, ids = [], np.empty(num_files), [], [], []
    time = np.empty(num_files)
    
    for i, file in enumerate(files):
        full_path = os.path.join(directory, file)
        time[i] = float(file[10:-2])
        h, m, x, y, z, vx, vy, vz, id = read_tipsy.read_file(full_path)
        par.append([h, m, id])
        vel.append([vx, vy, vz])
        pos.append(np.column_stack((x, y, z)))
        ids.append(id)
    return pos, 15*time, vel, par, ids

#! load parameters from stacked objects
def read_parameters(path):
    log = {}
    with open(f'/net/hypernova/data2/BOOMPJE/{path}/parameters.log') as f:
        f = f.readlines()
        for line in f:
            key, value = line.strip().split(':')
            try:
                log[key.strip()] = float(value.strip())
            except:
                log[key.strip()] = value.strip()
    return log


#! get and format data and parameters
print(path)
pos, time, _, _, _ = load_data(f'/net/hypernova/data2/BOOMPJE/{path}')
param = read_parameters(path)
m_r = r'$M_{s}/M_{c}$ = ' + f'${round(param["mass_ratio"], 4)}$'
c_con = r'$c_{cen}$ = ' + f'${round(param["cen_concentration"], 4)}$'
s_con = r'$c_{sat}$ = ' + f'${round(param["sat_concentration"], 4)}$'
cen_slope = r'$\alpha_{cen}$ = ' + f'${round(param["cen_inner_slope"], 4)}$'
sat_slope = r'$\alpha_{sat}$ = ' + f'${round(param["sat_inner_slope"], 4)}$'
per_d = r'$r_{p}$ = ' + f'${round(param["pericentre_distance"], 4)}$'
e = r'$e$ = ' + f'${round(param["eccentricity"], 4)}$'


#! plot animation
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(7, 7))

def init():
    return ax,

def update(frame):
    positions = pos[frame]
    qv = QuickView(positions, extent=[-3, 3, -3, 3], r='infinity', plot=False)  # ! optimize
    ax.cla()
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
    ax.set_aspect('equal')
    ax.set_title(f'Simulation {int(param["simulation_id"])}' + '\n' + fr'$\tau$ = {np.around(time[frame], decimals=4)} ' + r'$H_{0}^{-1}$', y=1.03)
    img = qv.get_image()
    ax.imshow(img, extent=qv.get_extent(), origin='lower', cmap='gist_heat')
    ax.text(2.6, 2.6, f'{m_r}\n{c_con}\n{s_con}\n{cen_slope}\n{sat_slope}\n{per_d}\n{e}', ha='right', va='top')
    return ax,

ani = animation.FuncAnimation(fig, update, frames=len(pos), init_func=init, blit=False)
ani.save(f'../anim/simulation_{int(param["simulation_id"])}.mp4', fps=120)