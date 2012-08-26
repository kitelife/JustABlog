#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Created on Aug 26, 2012

@author: xiayf
'''
import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect("postsinfo.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE posts
             (postid INTEGER PRIMARY KEY ASC, posttitle TEXT, postcontent TEXT, updatetime TEXT)''')
    testposts = [('Hello World', 'C, C++, Python, Java, Ruby, Hello!', '2012-08-22')
                 ]
    cursor.executemany('INSERT INTO posts (posttitle, postcontent, updatetime) VALUES (?,?,?)', testposts)
    conn.commit()
    cursor.execute('SELECT postid, posttitle, postcontent, updatetime FROM posts')
    for row in cursor.fetchall():
        print row
    cursor.close()
    conn.close()
