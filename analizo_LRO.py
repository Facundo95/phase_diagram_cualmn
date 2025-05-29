#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 14:15:00 2022

@author: facundo
"""

import pandas as pd
import numpy as np
import argparse

def criterio_fase(row):
    xdcero_cu = (np.abs(row['x_cu_mean']) > 2 * row['x_cu_std'])
    #ydcero_cu = (np.abs(row['y_cu_mean']) > 2 * row['y_cu_std'])
    #zdcero_cu = (np.abs(row['z_cu_mean']) > 2 * row['z_cu_std'])
    xcero_cu = (np.abs(row['x_cu_mean']) < 2 * row['x_cu_std'])
    ycero_cu = (np.abs(row['y_cu_mean']) < 2 * row['y_cu_std'])
    zcero_cu = (np.abs(row['z_cu_mean']) < 2 * row['z_cu_std'])
    xdcero_al = (np.abs(row['x_cu_mean']) > 2 * row['x_cu_std'])
    #ydcero_al = (np.abs(row['y_cu_mean']) > 2 * row['y_cu_std'])
    #zdcero_al = (np.abs(row['z_cu_mean']) > 2 * row['z_cu_std'])
    xcero_al = (np.abs(row['x_cu_mean']) < 2 * row['x_cu_std'])
    ycero_al = (np.abs(row['y_cu_mean']) < 2 * row['y_cu_std'])
    zcero_al = (np.abs(row['z_cu_mean']) < 2 * row['z_cu_std'])
    if xcero_al and xcero_cu: 
        return 'A2'
    if xdcero_al and xdcero_cu:
        if ycero_al and ycero_cu and zcero_al and zcero_cu:
            return 'B2'
        else:
            return 'L21'
    
def criterio_magn(row):
    mdcero = (np.abs(row['magnetizacion_mean']) > 2 * row['magnetizacion_std'])
    sdx = (np.abs(row['x_mn_up_mean'] \
                  -row['x_mn_down_mean'])<2*(row['x_mn_up_std'] \
                                             +row['x_mn_down_std']))
    sdy = (np.abs(row['y_mn_up_mean'] \
                  -row['y_mn_down_mean'])<2*(row['x_mn_up_std'] \
                                             +row['x_mn_down_std']))
    sdz = (np.abs(row['z_mn_up_mean'] \
                  -row['z_mn_down_mean'])<2*(row['x_mn_up_std'] \
                                             +row['x_mn_down_std']))
    if mdcero: return 'ferro'
    else:
        if sdx and sdy and sdz:
            return 'para'
        else:
            return 'anti'
        
def analiza_datos(file):
    col_names = ['contador',
                 'temperatura',
                 'mu_cu',
                 'mu_al',
                 'x_cu',
                 'x_mn_up',
                 'x_mn_down',
                 'x_al',
                 'y_cu',
                 'y_mn_up',
                 'y_mn_down',
                 'y_al',
                 'z_cu',
                 'z_mn_up',
                 'z_mn_down',
                 'z_al',
                 'magnetizacion',
                 'c_cu',
                 'c_mn_up',
                 'c_mn_down',
                 'c_al',
                 'delta_e_q',
                 'delta_e_m',
                 'delta_e_qm']
    
    col_export = ['temperatura',
                 'mu_cu',
                 'mu_al',
                 'x_cu_mean',
                 'x_cu_std',
                 'x_mn_up_mean',
                 'x_mn_up_std',
                 'x_mn_down_mean',
                 'x_mn_down_std',
                 'x_al_mean',
                 'x_al_std',
                 'y_cu_mean',
                 'y_cu_std',
                 'y_mn_up_mean',
                 'y_mn_up_std',
                 'y_mn_down_mean',
                 'y_mn_down_std',
                 'y_al_mean',
                 'y_al_std',
                 'z_cu_mean',
                 'z_cu_std',
                 'z_mn_up_mean',
                 'z_mn_up_std',
                 'z_mn_down_mean',
                 'z_mn_down_std',
                 'z_al_mean',
                 'z_al_std',
                 'magnetizacion_mean',
                 'magnetizacion_std',
                 'delta_e_q_mean',
                 'delta_e_q_std',
                 'delta_e_m_mean',
                 'delta_e_m_std',
                 'delta_e_qm_mean',
                 'delta_e_qm_mean',
                 'c_cu',
                 'c_mn',
                 'c_al',
                 'fase_magn']
    
    df = pd.read_csv(file, sep='\t', header=None, index_col=False, 
                     names=col_names)
    
    df_group = df.groupby(['temperatura','mu_al', 'mu_cu']).describe()
    df_group.columns = df_group.columns.to_flat_index().str.join('_')


    df_group['fase'] = df_group.apply(lambda row: criterio_fase(row), axis=1)
    df_group['magnetismo'] = df_group.apply(lambda row: criterio_magn(row), 
                                            axis=1)
    df_group['fase_magn'] = df_group.apply(lambda row: row['fase'] \
                                       + row['magnetismo'], axis=1)

    df_group['c_cu'] = df_group['c_cu_mean'] * 100
    df_group['c_al'] = df_group['c_al_mean'] * 100
    df_group['c_mn'] = 100 - df_group['c_cu'] - df_group['c_al']

    file_export = 'fases_' + file
    df_export = df_group.reset_index()
    df_export = df_export[col_export]
    df_export.to_csv(file_export, sep=' ', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='archivo LRO para analizar')
    arg = parser.parse_args()
    
    analiza_datos(arg.f)