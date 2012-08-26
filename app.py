#!/usr/bin/evn python
#-*- coding: utf-8 -*-

__author__ = 'xiayf'

from flask import Flask
from flask import request
from flask import render_template

app = Flask(
	__name__
)

@app.route('/')
def index():
	return render_template('main.html')

@app.route('/posts')
def posts():
	pass

@app.route('/projects')
def projects():
	pass

@app.route('/about')
def aboutblog():
	return render_template('aboutblog.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		login_handler()
	else:
		show_loginForm()

def logout():
	pass

if __name__ == '__main__':
	app.run(debug=True)