#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Created on Aug 26, 2012

@author: xiayf
'''
from model import *
import time
import random
import helper

def getPosts():
    result = posts.query.order_by(posts.updatetime)
    listResults = list()
   
    for item in result:
        dictItem = dict()
        dictItem['postid'] = item.postid
        dictItem['posttitle'] = item.posttitle
        if not dictItem['posttitle']:
            dictItem['posttitle'] = u"文章未命名"
        dictItem['updatetime'] = item.updatetime
        listResults.append(dictItem)
    listResults.reverse()
    return listResults

def getPostDetails(post_id):
    dictResult = getMDPost(post_id)
    dictResult['postcontent'] = helper.handleMarkDownContent(dictResult['postcontent'])
    
    return dictResult

def getMDPost(post_id):
    result = posts.query.filter_by(postid=post_id).first()
    dictResult = dict()
    dictResult['postid'] = post_id
    dictResult['posttitle'] = result.posttitle
    dictResult['postcontent'] = result.postcontent
    dictResult['updatetime'] = result.updatetime
    
    return dictResult

def loginCheckUser(username, password):
    result = users.query.filter_by(username=username, password=password).all()
    if result and len(result):
        return True
    else:
        return False
    
def storePost(postName, postContent):
    createtime = time.strftime("%Y-%m-%d %H:%M:%S")
    postId = 'p' + str(time.time()).replace('.', '') + str("%.5f" % random.uniform(100, 1000)).replace('.', '')
    post = posts(postId, postName, postContent, createtime)
    db.session.add(post)
    db.session.commit()
    return postId
    
def updatePost(postid, posttitle, postcontent):
    updatetime = time.strftime("%Y-%m-%d %H:%M:%S")
    post = posts.query.filter_by(postid=postid).first()
    post.posttitle = posttitle
    post.postcontent = postcontent
    post.updatetime = updatetime
    db.session.add(post)
    db.session.commit()

def delPost(postid):
    post = posts.query.filter_by(postid=postid).first()
    db.session.delete(post)
    db.session.commit()
    
def getUserByEmail(email):
    user = users.query.filter_by(email=email).first()
    if user:
        return True
    else:
        return False
    
def getUserByUsername(username):
    result = users.query.filter_by(username=username).all()
    if result and len(result):
        return True
    else:
        return False

def addAccount(username, password, email):
    user = users(username, password, email)
    db.session.add(user)
    db.session.commit()
    return True

def addComment(postid, commentUsername, commentContent):
    commenttime = time.strftime("%Y-%m-%d %H:%M:%S")
    comment = comments(postid, commentUsername, commentContent, commenttime)
    db.session.add(comment)
    db.session.commit()
    return True

def getComments(postid):
    postcomments = comments.query.filter_by(postid=postid).all()
    commentList = list()
    for comment in postcomments:
        commentItem = dict()
        commentItem['commentusername'] = comment.commentusername
        commentItem['commentcontent'] = comment.commentcontent
        commentItem['commenttime'] = comment.commenttime
        commentList.append(commentItem)
    return commentList
