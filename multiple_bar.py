# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 11:20:03 2017

@author: sdaldry
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# call in csv files as dataframes
df1 = pd.read_csv("Mutect_db/mutations_by_sample_number.csv", parse_dates=False, index_col=0)
df1 = df1.sort_index()

df2 = pd.read_csv("Muse_db/mutations_by_sample_number_muse.csv", parse_dates=False, index_col=0)
df2 = df2.sort_index()

df3 = pd.read_csv("Varscan_db/mutations_by_sample_number_varscan.csv", parse_dates=False, index_col=0)
df3 = df3.sort_index()

df4 = pd.read_csv("SomaticSniper_db/mutations_by_sample_number_somaticsniper.csv", parse_dates=False, index_col=0)
df4 = df4.sort_index()

dfall = [df1, df2, df3, df4]

# set index and columns so we can combine dataframes, assuming identical number of indexes
ind = [df1.index[i].split('_')[1] for i in range(len(df1.index))]
#col = [dfall[i].index[0].split('_')[2] for i in range(len(dfall))]

ndf = pd.DataFrame({(str(df1.index[0].split('_')[2])) : [df1.values[i][0] for i in range(len(df1))], \
                    (str(df2.index[0].split('_')[2])) : [df2.values[i][0] for i in range(len(df2))], \
                    (str(df3.index[0].split('_')[2])) : [df3.values[i][0] for i in range(len(df3))], \
                    (str(df4.index[0].split('_')[2])) : [df4.values[i][0] for i in range(len(df4))]}, \
                    index=ind)   #empty dataframe with desired indexing and column labels

# save dataframe to csv
ndf.to_csv('mutations_by_sample_number_all.csv')