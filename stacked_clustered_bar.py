# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 17:28:05 2017

@author: sdaldry
"""

import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt

def test1():
    # create fake dataframes
    df1 = pd.DataFrame(np.random.rand(4, 5),
                   index=["A", "B", "C", "D"],
                   columns=["I", "J", "K", "L", "M"])
    df2 = pd.DataFrame(np.random.rand(4, 5),
                   index=["A", "B", "C", "D"],
                   columns=["I", "J", "K", "L", "M"])
    df3 = pd.DataFrame(np.random.rand(4, 5),
                   index=["A", "B", "C", "D"], 
                   columns=["I", "J", "K", "L", "M"])
    
    plot_clustered_stacked([df1, df2, df3],["df1", "df2", "df3"])


def max_index(dfall):
    df_index = []
    for i in range(len(dfall)):
        df_index.append(len(dfall[i].index))
    return max(df_index)


def plot_clustered_stacked(dfall, labels=None,
                           title="Distribution of Mutation Impacts between PAK Genes for Given Cancer Types",
                           xlab="Cancer Type", 
                           ylab="Number of Mutations",
                           H="/", **kwargs):
    """Given a list of dataframes, with identical columns, create
        a clustered stacked bar plot. labels is a list of the names of the 
        dataframe, used for the legend title is a string for the title of 
        the plot H is the hatch used for identification of the different 
        dataframe"""


    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = max_index(dfall)
    axe = plt.subplot(111)
    

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      figsize=(20,12),
                      colormap="Accent",
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_df * n_col
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 90)
    axe.set_title(title)
    axe.set_xlabel(xlab)
    axe.set_ylabel(ylab)

    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[0.01, 0.87]) # Legend for mutation type
    if labels is not None:
        l2 = plt.legend(n, labels, loc=[0.01, 0.77]) # Legend for genes
    axe.add_artist(l1)
    return axe

# call in csv files as dataframes
#df1 = pd.read_csv("pak4_impact_count.csv", parse_dates=False, index_col=0)
#
#df2 = pd.read_csv("pak5_impact_count.csv", parse_dates=False, index_col=0)
#
#df3 = pd.read_csv("pak6_impact_count.csv", parse_dates=False, index_col=0)

df1 = pd.read_csv("Mutect_db/mutations_by_sample_number.csv", parse_dates=False, index_col=0)

df2 = pd.read_csv("Muse_db/mutations_by_sample_number_muse.csv", parse_dates=False, index_col=0)

df3 = pd.read_csv("Varscan_db/mutations_by_sample_number_varscan.csv", parse_dates=False, index_col=0)

df4 = pd.read_csv("SomaticSniper_db/mutations_by_sample_number_somaticsniper.csv", parse_dates=False, index_col=0)

# create set of indexes from all dataframes
index_list = set(df1.index)
index_list.update(df2.index)
index_list.update(df3.index)
index_list.update(df4.index)
index_list = list(index_list) # convert to list
index_list.sort()

# reindex dataframes such that indexes match
df1 = df1.reindex(index_list)
df2 = df2.reindex(index_list)
df3 = df3.reindex(index_list)
df4 = df4.reindex(index_list)


def main(dfs, labels):
    plot_clustered_stacked(dfs, labels)
        

if __name__=='__main__':
    main([df1, df2, df3, df4],["Mutect", "Muse", "Varscan", "SomaticSniper"])