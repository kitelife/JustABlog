#-*- coding: utf-8 -*-
'''
Created on Aug 26, 2012

@author: xiayf
'''
from flask import session
import controller

def login_handler(user, password):
    trueUser = controller.loginCheckUser(user, password)
    if not trueUser:
        return None
    session.permanent = True
    session['username'] = user
    return True

def logout_handler():
    session.pop('username')
    
def getCurrentUser():
    if 'username' not in session:
        return None
    else:
        return session['username']
    
def handleMarkDownContent(content):
    import markdown
    html = markdown.markdown(content, safe_mode=True, output_format='html4')
    return html
