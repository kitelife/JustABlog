#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Created on Aug 26, 2012

@author: xiayf
'''
import sqlite3

def postTable():
    conn = sqlite3.connect("justablog.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE posts
             (postid PRIMARY KEY, posttitle TEXT, postcontent TEXT, updatetime TEXT)''')
    testposts = [('p123456789', 'Hello World', 'C, C++, Python, Java, Ruby, Hello!', '2012-08-22')
                 ]
    cursor.executemany('INSERT INTO posts (postid, posttitle, postcontent, updatetime) VALUES (?,?,?,?)', testposts)
    conn.commit()
    cursor.execute('SELECT postid, posttitle, postcontent, updatetime FROM posts')
    for row in cursor.fetchall():
        print row
    cursor.close()
    conn.close()

def userTable():
    conn = sqlite3.connect("justablog.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE users
                    (userid INTEGER PRIMARY KEY ASC, username TEXT, password TEXT, email TEXT)''')
    testusers = [('youngsterxyf', '06122553', 'sas.198708@gmail.com')]
    cursor.executemany('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', testusers)
    conn.commit()
    cursor.execute('SELECT username, password, email FROM users')
    for row in cursor.fetchall():
        print row
    cursor.close()
    conn.close()
    
def countUser():
    conn = sqlite3.connect("justablog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    print cursor.fetchone()

def commentTable():
    conn = sqlite3.connect('justablog.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE comments
                    (commentid INTEGER PRIMARY KEY ASC, postid TEXT, commentusername TEXT, commentcontent TEXT, commenttime TEXT)''')
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    #postTable()
    #userTable()
    #countUser()
    commentTable()
    
