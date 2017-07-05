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

def count(table, in_df):   #Returns the number of mutations in a given table of a given dataframe
    res_df = in_df[in_df['table_name']==table]
    return float(res_df.shape[0])

def count_var_class(table, in_df, var_class):
    res_df = in_df[(in_df['table_name']==table) & (in_df['Variant_Classification']==var_class)]
    return float(res_df.shape[0])

def count_rows(table):   #returns the number of rows in each table
    c.execute('SELECT Count(rowid) FROM {tn}' .format(tn=table))
    rows = c.fetchall()
    rows = (rows[0])[0]
    return rows

def count_samples(table):   #Returns the number of unique samples in each table
    c.execute('SELECT Count(DISTINCT(Tumor_Sample_UUID)) FROM {tn}' .format(tn=table))
    ids = c.fetchall()
    ids = (ids[0])[0]
    return ids

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
    

            
if __name__ == '__main__':
    #test_1()
    #test_2()
    #test_3()
    #test_4()
    pak4 = main('ENSG00000130669', con)
    pak4.to_csv('pak4.csv')
    
    pak5 = main('ENSG00000101349', con)
    pak5.to_csv('pak5.csv')
    
    pak6 = main('ENSG00000137843', con)
    pak6.to_csv('pak6.csv')
    
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    tables = [n[0] for n in tables]
    
    
#    res = {}
#    for table in tables:
#        ml = np.array([count(table, pak4),count(table, pak5),count(table, pak6)])
#        if ml.sum()>10:
#            #ml = ml/ml.max()   #divide by largest number
#            #ml = ml/ml.sum()   #divide by sum of mutations
#            res[table]=ml
#    res = pd.DataFrame.from_dict(res)
#    print res.shape
#    print res.head()
#    res = res.T
#    res.columns = ['pak4','pak5','pak6']
#    res.to_csv('pakfam_abcount.csv')
#    #res.plot(kind='kde')
#    #plt.show()
#    res.plot(kind='box')
#    plt.show()
    
    
#    res = {}
#    for table in tables:
#        vc = np.array([count_var_class(table, pak4, 'Silent'), 
#                       count_var_class(table, pak4, 'Missense_Mutation'),
#                       count_var_class(table, pak4, 'Nonsense_Mutation' or 'Frame_Shift_Ins' or 'Frame_Shift_Del'),
#                       count_var_class(table, pak4, '3\'UTR' or '5\'UTR')])
#        if vc.sum()>0:   #currently no threshold
#            #vc = vc/vc.max()
#            vc = vc/vc.sum()
#            res[table]=vc
#    res = pd.DataFrame.from_dict(res)
#    print res.shape
#    print res.head()
#    res = res.T
#    res.columns = ['Synonymous', 'Missense', 'Nonsense, FS_Ins, FS_Del', '3\' or 5\' UTR']
#    res.to_csv('pak4_var_class_ratio.csv')
    
    
    rows_dict = {}   #iterates through tables and returns number of rows in a dataframe divided by the number of unique samples in each table
    counter = 0
    for table in tables:
        counter += 1
        print counter
        mutes = count_rows(table)/count_samples(table)
        rows_dict[table] = mutes
    print rows_dict
    rows_dict = pd.DataFrame.from_dict(rows_dict, orient='index')
    print rows_dict
    rows_dict.to_csv('mutations_by_sample_number.csv')
    
    
#    fog1 = main('ENSG00000179588', con)
#    fog1.to_csv('fog1.csv')
#    fog2 = main('ENSG00000169946', con)
#    fog2.to_csv('fog2.csv')    
#    res = {}
#    for table in tables:
#        ml = np.array([count(table, fog1),count(table, fog2)])
#        if ml.sum()>10:
#            ml = ml/ml.max() 
#            res[table]=ml
#    res = pd.DataFrame.from_dict(res)
#    res = res.T
#    res.columns = ['fog1','fog2']
#    res.to_csv('fogfam.csv')
#    #res.plot(kind='kde')
#    #plt.show()    

    con.close() 
    
    
    
    
    
    
    

