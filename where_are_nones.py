# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:43:21 2017

@author: sdaldry
"""

import sqlite3 as db



con = db.connect('cancer_mutect.db')
c = con.cursor()


# runnning lines 19-30 will tell you which cancer types contain mutations 
# attributed to a gene/position with no Ensembl ID
def make_index(con):
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    tables = [n[0] for n in tables]
    for table in tables:
        c.execute("SELECT Gene FROM {tb}".format(tb=table))
        n_index = c.fetchall()
        n_index = [n[0] for n in n_index]
        n_index = str(str(n_index))
        if 'None' in n_index:
            print "IN HERE: >>> %s <<<" % (table)
        else:
            print "Not in table %s" % (table)
    return 'bwuh?' 