#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 15:43:53 2022

@author: facundo
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import ternary
import numpy as np
import os


def grafico_ternario(file, j3, j6, w2):
    plt.style.use('./plots.mplstyle')
    
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

    df = pd.read_csv(file, sep=' ')
    
    df = df[np.abs(df['c_al'] - 25.0) < 10]
    
    tmp = df.groupby('temperatura').describe().reset_index()
    temperaturas = tmp['temperatura'].to_numpy()

    for temp in temperaturas:
        mask = df['temperatura'] == temp
        df_t = df[mask]
        
        fig, tax = ternary.figure(scale=50)
        fig.set_size_inches(10, 9)

        for name, group in df_t.groupby('fase_magn'):
            # Note that we have to shuffle the order.
            # So the column order is: right, left, bottom.
            points = group[['c_mn', 'c_al', 'c_cu']].values
    
            tax.scatter(points, marker=marker[name], s=150, 
                        edgecolors=color[name], facecolors='none',
                        linewidths=0.5)

        # Draw some lines.
        p1, p2 = (0, 25, 75), (25, 25, 0)
        tax.line(p1, p2, linewidth=3, color='r', alpha=0.35, linestyle="--")
        
        
        file_tl = f'TL_{temp}_' + file
        path = os.path.exists(file_tl)
        if path:
            df_tl = np.genfromtxt(file_tl, delimiter=' ')
            for p1, p2, p3, p4, p5, p6 in df_tl:
                tax.line((p1, p2, p3), (p4, p5, p6), linewidth=1.5, color='k')

        

        # Labels
        fontsize = 35
        offset = 0.24
        title = 'T={}K \n $J_3^M={}k_B$ \n $J_6^M={}k_B$'.format(temp, j3, j6)
        tax.get_axes().text(-5.0, 35.0, title, fontsize=30)
        tax.left_axis_label(r"$\leftarrow$Cu [at.\%]", fontsize=fontsize, 
                            offset=0.15)
        tax.right_axis_label(r"$\leftarrow$Al [at.\%]", fontsize=fontsize, 
                             offset=0.15)
        tax.bottom_axis_label(r"Mn$\rightarrow$ [at.\%]", fontsize=fontsize, 
                              offset=0.15)
        tax.right_corner_label("Mn", fontsize=fontsize, offset=offset)
        tax.top_corner_label("Al", fontsize=fontsize, offset=offset)
        tax.left_corner_label("Cu", fontsize=fontsize, offset=offset)

        # Decorations.
        #tax.legend(fontsize=15, bbox_to_anchor=(0.6, 0.5, 0.5, 0.5))
        tax.boundary(linewidth=3.0)
        tax.gridlines(multiple=10, color="gray")
        #tax.ticks(axis='lbr', linewidth=2.0, multiple=10, fontsize=25, offset=0.02)

        tax.set_axis_limits({'b': [0, 50], 'l': [50, 100], 'r': [0, 50]})
        tax.get_ticks_from_axis_limits(multiple=10)
        tax.set_custom_ticks(fontsize=25, offset=0.02, multiple=10)
        tax._redraw_labels()
        tax.get_axes().axis('off')
        tax.clear_matplotlib_ticks()
        tax.show()

        filename = 'CuAlMn_T-{}_J3-{}_J6-{}_{}W2.eps'.format(temp, j3, j6, w2)
        tax.savefig(filename, format='eps')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='archivo LRO para analizar')
    parser.add_argument('-j3', type=float, help='valor del j3')
    parser.add_argument('-j6', type=float, help='valor del j6')
    parser.add_argument('-w2', type=float, help='factor del w2')
    arg = parser.parse_args()
    
    grafico_ternario(arg.f, arg.j3, arg.j6, arg.w2)