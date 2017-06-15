# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pandas as pd
import sqlite3 as db



def test_1():
    in_path = os.path.join(
    'in_data',
    '0b4f69bd-e32e-484f-9948-6934ea230c4a',
    'TCGA.LGG.varscan.0b4f69bd-e32e-484f-9948-6934ea230c4a.DR-6.0.somatic.maf.gz'
                        )
    df = pd.read_table(in_path,comment='#',
                       sep='\t',
                        index_col=False,
                        compression='gzip')
    print df.head()
    table_name = in_path.split('\\')[-1]
    table_name = '_'.join(table_name.split('.')[0:3])
    print table_name

    
def get_table_name(in_path):
    table_name = in_path.split('\\')[-1]
    table_name = '_'.join(table_name.split('.')[0:3]) 
    return table_name

    
def dump(in_path, con, c):
        df = pd.read_table(in_path,comment='#',
                       sep='\t',
                        index_col=False,
                        compression='gzip')
        #print df.head()
        table_name = get_table_name(in_path)
        #print table_name
        df.to_sql(name=table_name, con=con,  flavor='sqlite', if_exists='replace') 
        c.execute('CREATE INDEX {ix} on {tn} ({cn})'.format(ix='gene_index_'+table_name, tn=table_name, cn='Gene'))  
        
        

def main(tag='mutect', db_name='cancer_mutect.db')       
    con = db.connect(db_name)
    c = con.cursor()
    a=0
    for folder in os.listdir('in_data'):
        for file_name in os.listdir(os.path.join('in_data',folder)):
            if file_name.endswith('.gz') and tag in file_name:
                in_path = os.path.join('in_data', folder, file_name)
                dump(in_path, con, c)
                a+=1
                print a, file_name


    
    con.commit()
    con.close()         

if __name__ == '__main__':
    main()
    
   
    #test_1()



