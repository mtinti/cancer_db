# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:12:10 2017

@author: sdaldry
"""

import pandas as pd
import sqlite3 as db
import time


con = db.connect('cancer_mutect.db')
c = con.cursor()


# create index of gene names from all data tables
def make_index(con):
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    tables = [n[0] for n in tables]
    index = set()
    for table in tables:
        c.execute("SELECT Gene FROM {tb}".format(tb=table))
        n_index = set(c.fetchall())
        index.update(n_index)
    index = [str(n[0]) for n in index]
    print "Index Generated!"
    return index

# get cancer types as column names
def col_names(con):
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    cols = [(str(n[0])).split('_')[1] for n in tables]
    cols.sort()
    cols.remove("READ") # remove READ cancer type until issue is dealt with
    print "Columns Generated!"
    return cols

def count_mutations(table, gene):   #returns the number of rows for a given mutation
    c.execute('SELECT Count(rowid) FROM {tn} WHERE Gene="{g}"' .format(tn=table, g=gene))
    rows = c.fetchall()
    rows = (rows[0])[0]
    return rows

# generate table by looping through database tables and getting
# absolute mutations counts for each gene name in each cancer type
def main(con):
    ind = make_index(con)
    #ind = ["ENSG00000101349"] #test to see if table can be generated with one ensembl ID (from pak5)
    cols = col_names(con)
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    tables = [n[0] for n in tables]
    tables.remove("TCGA_READ_mutect") # remove READ cancer type until issue is dealt with
    tables.sort()
    
    df = pd.DataFrame(index=ind, columns=cols)   # empty dataframe with index and labels
    print df.head
    
    for table in tables: #loop through cancer types
        start = time.time() #start timing for given cancer type
        print "Currently looping through %s." % (table)
        for n in range(len(df.index)): #loop through genes
            count = count_mutations(table, df.index[n])
            df[(str(table)).split('_')[1]][df.index[n]] = count
        end = (time.time() - start)
        print "Time taken to loop through %s was %s seconds." % (table, end) #output time taken to complete cancer type
    df.fillna(value=0)
    df.to_csv("mutation_counts.csv")
    print "Table Generated!"
    return df
            
if __name__ == "__main__":
    main(con)
            