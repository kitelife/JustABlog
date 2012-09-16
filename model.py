#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Created on Aug 26, 2012

@author: xiayf
'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        
class posts(db.Model):
    postid = db.Column(db.Text, primary_key=True)
    posttitle = db.Column(db.String(500))
    postcontent = db.Column(db.Text)
    updatetime = db.Column(db.String(20))
    
    def __init__(self, postid, posttitle, postcontent, updatetime):
        self.postid = postid
        self.posttitle = posttitle
        self.postcontent = postcontent
        self.updatetime = updatetime

class comments(db.Model):
    commentid = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.Integer)
    commentusername = db.Column(db.String(100))
    commentcontent = db.Column(db.Text)
    commenttime = db.Column(db.String(20)) 
    
    def __init__(self, postid, commentusername, commentcontent, commenttime):
        self.postid = postid
        self.commentusername = commentusername
        self.commentcontent = commentcontent
        self.commenttime = commenttime
