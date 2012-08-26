#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Created on Aug 26, 2012

@author: xiayf
'''
import model

def getPosts():
    db = model.StoreOperation('postsinfo.db')
    result = db.sqlSelectFetchAll("SELECT postid, posttitle, updatetime FROM posts")
    db.closeDB()
    listResults = list()
    dictItem = dict()
    for item in result:
        dictItem['postid'] = item[0]
        dictItem['posttitle'] = item[1]
        dictItem['updatetime'] = item[2]
        listResults.append(dictItem)
    
    return listResults

def getPostDetails(post_id):
    db = model.StoreOperation('postsinfo.db')
    result = db.sqlSelectFetchOne("SELECT posttitle, postcontent, updatetime FROM posts WHERE postid = %s" % post_id)
    dictResult = dict()
    dictResult['posttitle'] = result[0]
    dictResult['postcontent'] = result[1]
    dictResult['updatetime'] = result[2]
    
    return dictResult

if __name__ == '__main__':
    getPosts()
