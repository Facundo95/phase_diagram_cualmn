#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 12:45:33 2022

@author: facundo
"""

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('./plots.mplstyle')

def grafico_binario(file, j3, j6, w2):
    marker = {'B2ferro': '^',
              'B2para': 's',
              'B2anti': 'D',
              'A2ferro': '^',
              'A2para': 's',
              'A2anti': 'D',
              'L21ferro': '^',
              'L21para': 's',
              'L21anti': 'D'}

    color = {'B2ferro': 'r',
             'B2para': 'r',
             'B2anti': 'r',
             'A2ferro': 'y',
             'A2para': 'y',
             'A2anti': 'y',
             'L21ferro': 'b',
             'L21para': 'orange',
             'L21anti': 'b'}

    # Puntos Kainuma
    x = [ 5.07246377,  5.65217391,  6.01449275,  7.68115942,  7.10144928,
        8.55072464,  8.04347826,  9.05797101, 10.14492754, 15.2173913 ,
       19.92753623, 22.31884058, 24.05797101, 22.89855072]
    y = [523.15      , 532.12435897, 541.73974359, 551.35512821,
       556.48333333, 570.58589744, 569.30384615, 578.27820513,
       584.68846154, 600.07307692, 598.15      , 570.58589744,
       550.07307692, 532.12435897]

    fig, ax1 = plt.subplots()

    ax1.set_ylabel('Temperature [K]')
    ax1.set_xlabel(r'$at.\%$ Mn')
    ax1.set_xlim(0, 25)
    ax1.set_ylim(350, 800)

    ax2 = ax1.twiny()
    ax2.set_xlabel(r'$y$')
    ax2.set_xlim(0, 1)
    ax2.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])

    ax1.text(1, 760, r'$Cu_{3-y}AlMn_y$', 
             bbox=dict(edgecolor='k', facecolor='w'),
             fontsize=15)
    ax1.text(10, 450, r'$DO_3+L2_1$', fontsize=20)


    ax1.plot(x, y, 'ko--', label='Experimental Data')

    df = pd.read_csv(file, sep=' ')

    df = df[np.abs(df['c_al'] - 25.0) < .5]

    for name, group in df.groupby('fase_magn'):
        # Note that we have to shuffle the order.
        # So the column order is: right, left, bottom.
        p = group[['c_mn', 'temperatura']].values
            
        ax1.scatter(p[:,0], p[:,1], marker=marker[name], s=50, 
                    edgecolors=color[name], facecolors='none',
                    linewidths=0.5)
        
    
    ax1.legend(loc='upper right')
    fsave = 'CuAlMn_bin_J3-{}_J6-{}_{}W2.eps'.format(j3, j6, w2)
    plt.savefig(fsave, format='eps')
    plt.show()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='archivo LRO para analizar')
    parser.add_argument('-j3', type=float, help='valor del j3')
    parser.add_argument('-j6', type=float, help='valor del j6')
    parser.add_argument('-w2', type=float, help='factor del w2')
    arg = parser.parse_args()    
    
    grafico_binario(arg.f, arg.j3, arg.j6, arg.w2)