"""
    MLEKO
    Machine Learning Ecosystem for KOsmology 

    (C) Edoardo Carlesi 2020
    https://github.com/EdoardoCarlesi/MLEKO
"""

from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import webtools as wt
import pandas as pd
import seaborn as sns
import numpy as np
import tools as t


if __name__ == "__main__":
    """
        MAIN PROGRAM - compute K-Means
    """

    # Program Options: what should we run / analyze?
    normalize = False
    evalMetrics = True
    doYehuda = False

    plotNew = False
    plotStd = False
    plot3d = False
    plotKLV = False
    plotEVs = False
    plotLambdas = False

    file_base = '/home/edoardo/CLUES/DATA/Vweb/512/CSV/'
    #web_file = 'vweb_00_10.000032.Vweb-csv'; str_grid = '_grid32'; grid = 32
    #web_file = 'vweb_00_10.000064.Vweb-csv'; str_grid = '_grid64'; grid = 64
    web_file = 'vweb_00_10.000128.Vweb-csv'; str_grid = '_grid128'; grid = 128
    #web_file = 'vweb_25_15.000128.Vweb-csv'; str_grid = '_grid128'; grid = 128
    #web_file = 'vweb_00_00.000128.Vweb-csv'; str_grid = '_grid128'; grid = 128; normalize = True

    #web_file = 'vweb_128_.000128.Vweb-csv'; str_grid = '_grid128box500'; grid = 128
    #web_file = 'vweb_256_.000256.Vweb-csv'; str_grid = '_grid256box500'; grid = 256

    #box = 500.0e+3; thick = 7.0e+3
    #box = 500.0; thick = 5.0
    box = 100.0; thick = 2.0

    web_df = pd.read_csv(file_base + web_file)

    n_clusters = 10
    n_init = 1

    threshold_list = [0.0, 0.1, 0.2]

    # Check out that the vweb coordinates should be in Mpc units
    if normalize == True:
        norm = 1.0e-3   # kpc to Mpc
        print('Norm: ', norm) 

        web_df['l1'] = web_df['l1'] / norm
        web_df['l2'] = web_df['l2'] / norm
        web_df['l3'] = web_df['l3'] / norm

    if plotStd == True: 

        f_out = 'output/kmeans_oldvweb' + str_grid
        #norm = web_df['l1'].max()

        for threshold_lambda in threshold_list:
            wt.plot_vweb(fout=f_out, data=web_df, thresh=thresh, grid=grid, box=box, thick=thick)

    #web_df['logdens'] = np.log10(web_df['dens'])
    #print(web_df.head())

    cols_select = ['l1', 'l2', 'l3']; vers = ''; str_kmeans = r'$k$-means $\lambda$s'
    #cols_select = ['l1', 'l2', 'l3', 'dens']; vers = 'd'; str_kmeans = r'$k$-means $\lambda$s, \Delta_m'
    #cols_select = ['l1', 'l2', 'l3', 'logdens']; vers = 'ld'; str_kmeans = r'$k$-means $\lambda$s, $\log_{10}\Delta_m$'
    #cols_select = ['l1', 'l2', 'l3', 'dens', 'Vx', 'Vy', 'Vz']; vers = 'd_vx'

    #data = web_df[cols_select]

    print('Running kmeans...')
    n_clusters = 4
    n_init = 101
    kmeans = KMeans(n_clusters=n_clusters, n_init=n_init)
    kmeans.fit(web_df[cols_select])
    print('Done.')

    web_df['envk_std'] = kmeans.labels_
    web_df = wt.order_kmeans(data=web_df)

    for col in cols_select:
        med = np.median(web_df[col])
        std = np.std(web_df[col])

        str_print = '%.3f \pm %.3f & ' % (med, std)
        #print(str_print)
        #print('')

        thresh = [0.0, 0.1, 0.2]

    for th in thresh:
        web_df = wt.std_vweb(data=web_df, thresh=th)
        
        wt.compare_vweb_kmeans(vweb=web_df)

'''
    if doYehuda:

        n_clusters_tot = [2, 3, 4, 5, 6, 7, 8, 9, 10] 
        random_state = 1

        for n_clusters in n_clusters_tot:
            kmeans = KMeans(n_clusters=n_clusters, n_init=n_init, random_state=random_state)
            kmeans.fit(data)
            web_df['class'] = kmeans.labels_

            fout = 'output/vweb_' + str(grid) + '_k' + str(n_clusters) + '_rand_state' + str(random_state) + '.txt'
            print(n_clusters, fout)
            web_df.to_csv(path_or_buf=fout, sep='\t', index=False, float_format='%.3f')

    if evalMetrics == True:

        n_ks = 10
        rescale = 1
        f_out = 'output/kmeans_stability' + str_grid
        #n_clusters_tot = [2, 3] 
        n_clusters_tot = [2, 3, 4, 5, 6, 7, 8, 9, 10] 
        #kmeans = evaluate_metrics(data=web_ev_df, n_clusters_max=n_clusters, n_init=n_init)
        #kmeans_stability(data=web_ev_df, n_clusters_max=n_clusters, n_ks=n_ks, rescale_factor=rescale, f_out=f_out)
    
        prior='lognorm'
        #prior='gauss'
        #prior='flat'
        mode='ordered'
        #mode='simple'
        #data_rand = wt.generate_random(data=data, grid=grid, prior=prior, verbose=True, mode=mode)
        #data_rand = wt.generate_random(data=data, grid=grid, prior='gauss', verbose=True, mode='ordered')
        #print(data_rand.head())
        #data_rand.to_csv('output/random_web_128.txt', index=False)
        #data_rand = pd.read_csv('output/random_web_128.txt')
        #print(data_rand.head())

        k_all = []
        k_std = []
        k_rand = []
        #wt.evaluate_metrics(data=data_rand, n_clusters_max=10, n_init=0, rescale_factor=1, visualize=True, elbow=True)
        wt.evaluate_metrics(data=data, n_clusters_max=10, n_init=0, rescale_factor=1, visualize=True, elbow=True)
#def evaluate_metrics(data=None, n_clusters_max=None, n_init=10, rescale_factor=10, visualize=False, elbow=True):

        n_clusters_tot = 0
        for n_clusters in n_clusters_tot:
            kmeans = KMeans(n_clusters=n_clusters, n_init=n_init)
            kmeans.fit(data)
                
            kmeans_rand = KMeans(n_clusters=n_clusters, n_init=n_init)
            kmeans_rand.fit(data_rand)

            centers_rand = kmeans_rand.cluster_centers_
            centers = kmeans.cluster_centers_

            data_rand['label'] = kmeans_rand.labels_
            data['label'] = kmeans.labels_

            wsc = 0.0
            wsc_rand = 0.0 
        
            for i in range(0, n_clusters):

                n = len(data[data['label'] == i])
                c = centers[i]
                c = np.reshape(c, (3, 1))
                vals = data[data['label'] == i][cols_select].T.values - c
                wsc += np.sum(np.sqrt((vals)**2.0))

                n_rand = len(data_rand[data_rand['label'] == i])
                c_rand = centers_rand[i]
                c_rand = np.reshape(c_rand, (3, 1))
                vals_rand = data_rand[data_rand['label'] == i][cols_select].T.values - c_rand
                wsc_rand += np.sum(np.sqrt((vals_rand)**2.0))

            print(f'ROUND k={i+1}/{n_clusters}')
            print(n_clusters, wsc/n_clusters, wsc_rand/n_clusters)

            k_all.append(n_clusters)
            k_std.append(wsc/n_clusters)
            k_rand.append(wsc_rand/n_clusters)

                #diffs_rand = data_rand[data_rand['label'] == i].values
                #print(i, 'Std: ', len(diffs))
                #print(i, 'Ran: ', len(diffs_rand))
                #print(f'Cluster i has stddev: {stddev}')

            data_rand.drop(labels='label', inplace=True, axis=1)
            data.drop(labels='label', inplace=True, axis=1)

        k_all = np.array(k_all)
        k_std = np.array(k_std)
        k_rand = np.array(k_rand)

        print(k_all)
        print(k_std)
        print(k_rand)

        #plt.plot(k_all, k_std)
        #plt.plot(k_all, k_rand)
        figname = 'output/gap_stats_' + prior + '_' + mode + '_' + str(grid) + '.png'
        plt.xlabel('k')
        plt.ylabel('WSCdata - WSCrand')
        plt.plot(k_all, np.abs(k_rand-k_std))
        plt.title('Gap Statistics (' + prior + ', ' + mode + ')')
        plt.tight_layout()
        plt.savefig(figname)
        plt.show()

        exit()


    else:
        kmeans = KMeans(n_clusters = n_clusters, n_init = n_init)
        kmeans.fit(web_ev_df)

centers = kmeans.cluster_centers_
web_df['env'] = kmeans.labels_

if n_clusters == 2:
    colors = ['lightgrey', 'black']
    envirs = ['void', 'knot']
elif n_clusters == 3:
    colors = ['lightgrey', 'darkgrey', 'red']
    envirs = ['underdense', 'filament', 'knot']
elif n_clusters == 4:
    colors = ['lightgrey', 'grey', 'black', 'red']
    envirs = ['void', 'sheet', 'filament', 'knot']
elif n_clusters == 5:
    colors = ['lightgrey', 'grey', 'darkgrey', 'black', 'red']
    envirs = ['void', 'sheet', 'wall', 'filament', 'knot']
elif n_clusters == 6:
    colors = ['lightgrey', 'grey', 'darkgrey', 'black', 'orange', 'red']
    envirs = ['void', 'sheet', 'wall', 'filament', 'clump', 'knot']

vers = vers + '_k' + str(n_clusters)
out_evs_dist = 'output/kmeans_vweb_' + vers
out_dens_dist = 'output/kmeans_dens_' + vers
out_web_slice = 'output/kmeans_web_lv_' + vers

envirs_sort = []
colors_sort = []

deltas = np.zeros((n_clusters))
ntot = len(web_df)

for i in range(0, n_clusters):
    deltas[i] = np.median(web_df[web_df['env'] == i]['dens'].values)

deltas_sort = np.sort(deltas)

for i in range(0, n_clusters):
    n = len(web_df[web_df['env'] == i]) 
    index = np.where(deltas_sort == deltas[i])
    env_str = envirs[index[0][0]]
    envirs_sort.append(env_str)
    colors_sort.append(colors[index[0][0]])

    num_str = '& $ %.3f $ & $%.3f$ ' % (deltas[i], n/ntot)
    tab_str = env_str + num_str
    print(tab_str)

print('\n')
for i in range(0, n_clusters):
    c_str = ' & $ %.3f $  &  $ %.3f $ & $ %.3f $ ' % (centers[i,0], centers[i, 1], centers[i, 2])
    line_str = envirs_sort[i] + c_str
    print(line_str)

cols = []

   
out_evs_new = 'output/kmeans_new_' + vers
f_out = out_evs_new + str_grid + '.png'
wt.plot_new(labels=kmeans.labels_, data=web_ev_df, f_out=f_out)

out_evs_3d = 'output/kmeans_3d_' + vers
f_out = out_evs_3d + str_grid + '.png'
wt.plot3d(labels=kmeans.labels_, data=web_ev_df, f_out=f_out)

    # TODO there should be some loop on the environments here
env_type = ''
f_out_base = ''
wt.plot_eigenvalues_per_environment_type(data=None, env_type=None, out_base=None, grid=None) 

'''

#if plotLambdas == True:
#def plot_lambda_distribution(data=None, grid=None, base_out=None, envirs=None):
#def plot_local_volume_density_slice(data=None, box=100, file_out=None, title=None):


