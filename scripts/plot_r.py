import sys
sys.path.append('/net/hypernova/data2/BOOMPJE/code/ic_generation/')
import numpy as np
import read_tipsy
import os
from sphviewer.tools import QuickView
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams['figure.dpi'] = 360
matplotlib.rcParams['text.usetex'] = True


#!find path given a simulation id
sim_id = input('Simulation id: ')
path = [f for f in os.listdir('/net/hypernova/data2/BOOMPJE/') if f.startswith(f'merging_{sim_id}_')][0]


def separate_ids(sim_path):
    _, m, _, _, _, _, _, _, ids = read_tipsy.read_file(f'/net/hypernova/data2/BOOMPJE/{sim_path[:19]}/stacked_objects')
    ids.sort()
    cen_ids = ids[:int(1e6)]
    return cen_ids

def separate_halos(cen_ids, sim_path):
    _, m, x, y, z, vx, vy, vz, ids = read_tipsy.read_file(f'/net/hypernova/data2/BOOMPJE/{sim_path}')
    mask = np.isin(ids, cen_ids)
    halos = {
        'cen': {
            'pos': np.column_stack((x[mask], y[mask], z[mask])),
            'vel': np.column_stack((vx[mask], vy[mask], vz[mask])),
            'm': m[mask]},
        'sat': {
            'pos': np.column_stack((x[~mask], y[~mask], z[~mask])),
            'vel': np.column_stack((vx[~mask], vy[~mask], vz[~mask])),
            'm': m[~mask]}}
    return halos

def load_data(directory):
    direc = f'/net/hypernova/data2/BOOMPJE/{directory}'
    files = [f for f in os.listdir(direc) if f.startswith('evolution')]
    files.sort()
    time = []
    for file in files:
        time.append(float(file[10:-2]))
    return 15*np.array(time), files


sim_path = 'merging_0_1072098'
params = read_parameters(sim_path)
ids = separate_ids(sim_path)
time, files = load_data(sim_path)
dist, cm = [], []

for f in files:
    try:
        halos = separate_halos(ids, f'{sim_path}/{f}')
        cm_cen = np.sum(halos['cen']['m']*halos['cen']['pos'].T, axis=1)/np.sum(halos['cen']['m'])
        cm_sat = np.sum(halos['sat']['m']*halos['sat']['pos'].T, axis=1)/np.sum(halos['sat']['m'])
        cm.append([cm_cen, cm_sat])
        dist.append(np.linalg.norm(cm_cen-cm_sat))
    except:
        pass
    
    
fig, ax = plt.subplots(figsize=(7, 7))
rp, ra = min(dist), max(dist)

ax.set_xlabel(r'$t$')
ax.set_ylabel(r'$r$')
ax.set_title(f'Simulation {int(params["simulation_id"])}', y=1.03)
ax.plot(time, dist, c='black', marker='.')
ax.axhline(y=ra, c='blue', label=r'$r_{a}$', ls='--')
ax.axhline(y=rp, c='red', label=r'$r_{p}$', ls='--')
ax.legend()
plt.savefig(f'../plots/r_{path}.png')