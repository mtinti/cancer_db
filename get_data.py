# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 17:56:14 2017

@author: mtinti-x
"""
import pandas as pd
import sqlite3 as db
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')


con = db.connect('cancer_mutect.db')
table_name = 'TCGA_CHOL_mutect'
c = con.cursor()

def test_1():
    query_data = 'SELECT * FROM {tn} '.format(tn=table_name)
    df_data = pd.read_sql(query_data, con)
    print df_data.iloc[:3,:3]
    
def test_2():
    genes = [
    'ENSG00000049246',
    'ENSG00000142627',
    'ENSG00000055070'
    ] 
    genes = ['\"'+n+'\"' for  n in genes]
    query_data = 'SELECT * FROM {tn} WHERE Gene in ({li})'.format(tn=table_name, li=', '.join(genes))
    #print query_data
    df_data = pd.read_sql(query_data, con)
    print df_data.iloc[:3,:3]
    print  df_data.shape  

def test_3():
    gene = '\"ENSG00000109189\"'
    query_data = 'SELECT * FROM {tn} WHERE Gene = {g}'.format(tn=table_name, g=gene)
    #print query_data
    df_data = pd.read_sql(query_data, con)
    print df_data.iloc[:3,:3]
    print  df_data.shape 

def test_4():
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    for t in tables:
        print t[0]


def main(gene, con):
    q_gene = '\"'+gene+'\"'
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    tables = [n[0] for n in tables]
    #print tables
    res_df = []
    for table_name in tables:
        query_data = 'SELECT * FROM {tn} WHERE Gene = {g}'.format(tn=table_name, g=q_gene)
        temp_data = pd.read_sql(query_data, con)
        temp_data['table_name']=table_name
        res_df.append(temp_data)        
    res_df = pd.concat(res_df)
    #print  gene, res_df.shape
    #print res_df.head()
    return res_df
    
def count(table, in_df):
    res_df = in_df[in_df['table_name']==table]
    return float(res_df.shape[0])
        
          
if __name__ == '__main__':
    #test_1()
    #test_2()
    #test_3()
    #test_4()
    pak4 = main('ENSG00000130669', con)
    pak5 = main('ENSG00000137843', con)
    pak6 = main('ENSG00000101349', con)
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    tables = [n[0] for n in tables]
    res = {}
    for table in tables:
        ml = np.array([count(table, pak4),count(table, pak5),count(table, pak6)])
        if ml.sum()>10:
            ml = ml/ml.max() 
            res[table]=ml
    res = pd.DataFrame.from_dict(res)
    print res.shape
    print res.head()
    res = res.T
    res.columns = ['pak4','pak5','pak6']
    res.plot(kind='kde')
    plt.show()
    #res.plot(kind='box')
    #plt.show()    
    print res.head()
    
    fog1 = main('ENSG00000179588', con)
    fog2 = main('ENSG00000169946', con)    
    res = {}
    for table in tables:
        ml = np.array([count(table, fog1),count(table, fog2)])
        if ml.sum()>10:
            ml = ml/ml.max() 
            res[table]=ml
    res = pd.DataFrame.from_dict(res)
    res = res.T
    res.columns = ['fog1','fog2']
    res.plot(kind='kde')
    plt.show()    
    con.close() 
    
    
    
    
    

