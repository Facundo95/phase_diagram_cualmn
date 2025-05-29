#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 14:04:43 2022

@author: facundo
"""

import pandas as pd
import argparse

def encontrar_tl(file):
    df = pd.read_csv(file, sep=' ')
    
    for name, group in df.groupby('temperatura'):
        file_export = f'TL_{name}_' + file
        
        #mu_al = group['mu_al'].values 
        #mu_cu = group['mu_cu'].values

        c_al = group['c_al'].values
        c_cu = group['c_cu'].values
        c_mn = group['c_mn'].values
        
        for n in range(len(c_al)-1):
            condicion_mn = ((c_mn[n+1] - c_mn[n]) < -10.0)
            #condicion_mu_al = (np.abs(mu_al[n+1] - mu_al[n]) == 0.0)
            #condicion_mu_cu = (np.abs(mu_cu[n+1] - mu_cu[n]) == 100.0)
            if condicion_mn:
                with open(file_export, 'a') as f:
                    line = f'{c_mn[n]} {c_al[n]} {c_cu[n]} {c_mn[n+1]} {c_al[n+1]} {c_cu[n+1]}\n'
                    f.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='archivo fases_LRO para analizar TL')
    arg = parser.parse_args()
    
    encontrar_tl(arg.f)
