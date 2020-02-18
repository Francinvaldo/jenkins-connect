#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import dask.dataframe as dd
from dtw import dtw
import math
import ctypes
import pickle 
import multiprocessing
from joblib import Parallel, delayed


############################################################# Base de dados ###############################################################
dd_the_big_table = dd.read_parquet(f'../data/db_merged.parquet/*.parquet',engine='fastparquet')

############################################################# Base de dados ###############################################################


dd_the_big_table
dd_the_big_table.compute().shape

pet_ids = dd_the_big_table['pet_id'].unique().compute()

manhattan_distance = lambda x, y: np.abs(x - y)
##################################################### Functions #############################################################################
'''
    Appends all 'a_xyz' and all 'index' into one value when groupy is used
    in this case each column will have information of 10 rows
'''

def agg(df):
    return pd.Series(
        dict(
        l_xyz =df['a_xyz'].values,
        idxs = df.index.values
    
        )
    )

##################################################### Functions #############################################################################

'''
    Calculates DTW, variance and classify the data
'''
def time_wraping(x,df_full):
    next_idx = x['index'] + 1
    
    # check if next row exists in the dataset
    if next_idx in df_full.index:
        
        # calculates DTW and variance
        d,_, _,_ = dtw(x['l_xyz'], df_full.loc[next_idx]['l_xyz'], dist=manhattan_distance)
        var = np.var(x['l_xyz'])
        
        # Defines if the moviment is repetitive or not
        if d < 1.3 and var > 0.001:
            type_mov = 'repetitive'
        else:
            type_mov = 'ordinary'
        
        return pd.Series([d, var, type_mov])   





def slide_data(pet_id):
    
    #Loads one PET in memory
    df = dd_the_big_table.map_partitions(lambda df: df[df['pet_id'] == pet_id]).compute()
    
    
    df['date_time'] = df['time_stamp'].apply(lambda x: pd.Timestamp(x, unit='ms'))
   
    # Convert values of gyroscope and accelerometer
    df['ax'] = df['ax'].apply(lambda x : (ctypes.c_int16(int(x)).value * 32)/65536)
    df['ay'] = df['ay'].apply(lambda x : (ctypes.c_int16(int(x)).value * 32)/65536)
    df['az'] = df['az'].apply(lambda x : (ctypes.c_int16(int(x)).value * 32)/65536)
    
    # joins all 3 axis
    df['a_xyz'] = np.sqrt(df['ax']**2 + df['ay']**2 + df['az']**2)

    df.sort_values(by=['date_time'], inplace= True)

    df = df.reset_index()
    
    df['dist'] = None
    df['variance'] = None
    df['type'] = None

    # group 10 by 10 
    df_grouped = df.groupby(df.index // 10).apply(agg)

    df_grouped['index'] = df_grouped.index
    
    #calculates dist, variance and defines type (ordinary or repetitive)
    df_grouped[['dist', 'variance', 'type']] = a.apply(time_wraping, df_full=df_grouped, axis = 1)

    pickle.dump(df_grouped, open(f"../data/dtw_new/{pet_id}.p", "wb" ))



num_cores = multiprocessing.cpu_count()


len(pet_ids)

get_ipython().run_cell_magic('time', '', '# Use wisely\nParallel(n_jobs=num_cores)(delayed(slide_data)(i) for i in pet_ids)')



df = pickle.load(open('../data/dtw_new/1569850690.p', 'rb'))

#df.head()


