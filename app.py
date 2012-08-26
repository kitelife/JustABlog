#!/usr/bin/evn python
#-*- coding: utf-8 -*-

__author__ = 'xiayf'
import os
CONF = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config')

from flask import Flask
from flask import request, redirect, url_for
from flask import render_template
import controller
import helper

app = Flask(
	__name__
)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config.from_pyfile(os.path.join(CONF, 'base.py'))

@app.route('/')
def index():
	postinfos = controller.getPosts()
	return render_template('main.html', postinfolist=postinfos)
@app.route('/postdetail/<post_id>')
def post(post_id):
	postDetail = controller.getPostDetails(post_id)
	return render_template("postdetail.html", postinfo=postDetail)

@app.route('/projects')
def projects():
	return render_template("projects.html")

@app.route('/about')
def aboutblog():
	return render_template('aboutblog.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		trueUser = helper.login_handler(username, password)
		if trueUser:
			return render_template('adminpage.html')
	
	return render_template('loginform.html')

@app.route('/logout')
def logout():
	helper.logout_handler()
	return redirect(url_for('index'))

@app.route('/admin')
def admin():
	if not helper.getCurrentUser():
		return redirect(url_for('index'))
	return render_template('adminpage.html')

@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
	if request.method == 'POST':
		articlename = request.form['articlename']
		articlecontent = request.form['articlecontent']
		postid = controller.storePost(articlename, articlecontent)
		return redirect('/postdetail/%s' % postid)
	return render_template('addpost.html', post_handle_url=url_for('addpost'))

@app.route('/editpost', methods=['GET', 'POST'])
def editpost():
	if request.method == 'POST':
		articleid = request.form['articleid']
		articlename = request.form['articlename']
		articlecontent = request.form['articlecontent']
		controller.updatePost(articleid, articlename, articlecontent)
		return redirect('/postdetail/%s' % articleid)
	articleid = request.args.get('articleid', '')
	postDetail = controller.getMDPost(articleid)
	return render_template("addpost.html", post_handle_url='/editpost', articleid=articleid,
						 articlename=postDetail['posttitle'], articlecontent=postDetail['postcontent'])

@app.route('/deletepost')
def deletepost():
	postid = request.args.get('articleid', '')
	controller.delPost(postid)
	return redirect(url_for('index'))

###########################################
if __name__ == '__main__':
	app.run(debug=True)
