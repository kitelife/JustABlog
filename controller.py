#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Created on Aug 26, 2012

@author: xiayf
'''
import model
import time
import random
import helper

def getPosts():
    db = model.StoreOperation('justablog.db')
    result = db.sqlSelectFetchAll("SELECT postid, posttitle, updatetime FROM posts ORDER BY updatetime DESC", data=None)
    db.closeDB()
    listResults = list()
   
    for item in result:
        dictItem = dict()
        dictItem['postid'] = item[0]
        dictItem['posttitle'] = item[1]
        if not dictItem['posttitle']:
            dictItem['posttitle'] = u"文章未命名"
        dictItem['updatetime'] = item[2]
        listResults.append(dictItem)
    
    return listResults

def getPostDetails(post_id):
    dictResult = getMDPost(post_id)
    dictResult['postcontent'] = helper.handleMarkDownContent(dictResult['postcontent'])
    
    return dictResult

def getMDPost(post_id):
    db = model.StoreOperation('justablog.db')
    result = db.sqlSelectFetchOne("SELECT posttitle, postcontent, updatetime FROM posts WHERE postid = ?" , (post_id,))
    dictResult = dict()
    dictResult['postid'] = post_id
    dictResult['posttitle'] = result[0]
    dictResult['postcontent'] = result[1]
    dictResult['updatetime'] = result[2]
    
    return dictResult

def loginCheckUser(username, password):
    db = model.StoreOperation('justablog.db')
    result = db.sqlSelectFetchOne("SELECT COUNT(*) FROM users WHERE username = ? AND password = ?" , (username, password))
    if result and result[0]:
        return True
    else:
        return False
    
def storePost(postName, postContent):
    createtime = time.strftime("%Y-%m-%d %H:%M:%S")
    db = model.StoreOperation('justablog.db')
    postId = 'p' + str(time.time()).replace('.', '') + str("%.5f" % random.uniform(100, 1000)).replace('.', '')
    db.sqlCanModifyTable("INSERT INTO posts (postid, posttitle, postcontent, updatetime) VALUES(?, ?, ?, ?)", (postId, postName, postContent, createtime))
    db.conn.commit()
    db.closeDB()
    
    return postId
    
def updatePost(postid, posttitle, postcontent):
    updatetime = time.strftime("%Y-%m-%d %H:%M:%S")
    db = model.StoreOperation('justablog.db')
    db.sqlCanModifyTable("UPDATE posts SET posttitle = ?, postcontent = ?, updatetime = ? WHERE postid = ?", (posttitle, postcontent, updatetime, postid))
    db.conn.commit()
    db.closeDB()

def delPost(postid):
    db = model.StoreOperation('justablog.db')
    db.sqlCanModifyTable("DELETE FROM posts WHERE postid = ?", (postid,))
    db.conn.commit()
    db.closeDB()
    
def getUserByEmail(email):
    db = model.StoreOperation('justablog.db')
    result = db.sqlSelectFetchOne("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
    if result and result[0]:
        return True
    else:
        return False
    
def getUserByUsername(username):
    db = model.StoreOperation('justablog.db')
    result = db.sqlSelectFetchOne("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    if result and result[0]:
        return True
    else:
        return False

def addAccount(username, password, email):
    db = model.StoreOperation('justablog.db')
    db.sqlCanModifyTable("INSERT INTO users (username, password, email) VALUES(?, ?, ?)", (username, password, email))
    db.conn.commit()
    db.closeDB()
    return True

def addComment(postid, commentUsername, commentContent):
    commenttime = time.strftime("%Y-%m-%d %H:%M:%S")
    db = model.StoreOperation('justablog.db')
    db.sqlCanModifyTable("INSERT INTO comments (postid, commentusername, commentcontent, commenttime) VALUES (?, ?, ?, ?)",
                          (postid, commentUsername, commentContent, commenttime))
    db.conn.commit()
    db.closeDB()
    return True

def getComments(postid):
    db = model.StoreOperation('justablog.db')
    comments = db.sqlSelectFetchAll("SELECT commentusername, commentcontent, commenttime FROM comments WHERE postid = ?", (postid,))
    commentList = list()
    for comment in comments:
        commentItem = dict()
        commentItem['commentusername'] = comment[0]
        commentItem['commentcontent'] = comment[1]
        commentItem['commenttime'] = comment[2]
        commentList.append(commentItem)
    return commentList
 
if __name__ == '__main__':
    getPosts()
