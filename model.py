#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Created on Aug 26, 2012

@author: xiayf
'''

import sqlite3

class StoreOperation(object):
    
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.cursor = self.conn.cursor()
        
    def sqlCanModifyTable(self, sql, data):
        self.cursor.execute(sql, data)
        self.conn.commit()
        
    def sqlSelectFetchOne(self, sql, data):
        if not data:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, data)
        return self.cursor.fetchone()
    
    def sqlSelectFetchAll(self, sql, data):
        if not data:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, data)
        return self.cursor.fetchall()
    
    def closeDB(self):
        self.cursor.close()
        self.conn.close()
