# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 17:56:14 2017

@author: mtinti-x
"""
import pandas as pd
import sqlite3 as db


con = db.connect('cancer_mutect.db')
table_name = 'TCGA_CHOL_mutect'


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
    c = con.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    for t in tables:
        print t[0]


def main(gene, con):
    q_gene = '\"'+gene+'\"'
    c = con.cursor()
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
    print  gene, res_df.shape  
       
    
    

if __name__ == '__main__':
    #test_1()
    #test_2()
    #test_3()
    #test_4()
    main('ENSG00000130669', con)
    main('ENSG00000137843', con)
    main('ENSG00000101349', con)    
    con.close() 

