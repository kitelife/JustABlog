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
app.config['active_page'] = dict()
#print app.config

@app.route('/')
def index():
	app.config['active_page'].clear()
	app.config['active_page']['HOME'] = 'active'
	postinfos = controller.getPosts()
	return render_template('main.html', postinfolist=postinfos)

@app.route('/postdetail/<post_id>')
def post(post_id):
	postDetail = controller.getPostDetails(post_id)
	postComments = controller.getComments(post_id)
	return render_template("postdetail.html", postinfo=postDetail, commentlist=postComments)

@app.route('/projects')
def projects():
	app.config['active_page'].clear()
	app.config['active_page']['PROJECTS'] = 'active'
	from github import Github
	g = Github(app.config['GITHUBUSERNAME'], app.config['GITHUBPASSWORD'])
	
	repoList = list()
	for repo in g.get_user().get_repos():
		repodict = dict()
		repodict['reponame'] = repo.name
		repodict['repohomepage'] = repo.homepage
		repodict['repolanguage'] = repo.language
		repoList.append(repodict)
	repoList.sort()
	return render_template("projects.html", repos=repoList)

@app.route('/about')
def aboutblog():
	app.config['active_page'].clear()
	app.config['active_page']['ABOUT'] = 'active'
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

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		repassword = request.form['repassword']
		email = request.form['email']
		
		if password == repassword:
			emailExists = controller.getUserByEmail(email)
			usernameExists = controller.getUserByUsername(username)
			if emailExists:
				return render_template('registerform.html', tip=u"邮箱已被注册")
			elif usernameExists:
				return render_template('registerform.html', tip=u"用户名已被注册")
			else:
				controller.addAccount(username, password, email)
				return redirect(url_for('login'))
		else:
			return render_template('registerform.html', tip=u"两次密码输入不一致")
	return render_template('registerform.html')

@app.route('/admin')
def admin():
	if not helper.getCurrentUser():
		return redirect(url_for('index'))
	return render_template('adminpage.html')

@app.route('/addpost', methods=['GET', 'POST'])
def addpost():
	if helper.getCurrentUser():
		if request.method == 'POST':
			articlename = request.form['articlename']
			articlecontent = request.form['articlecontent']
			postid = controller.storePost(articlename, articlecontent)
			return redirect('/postdetail/%s' % postid)
		return render_template('addpost.html', post_handle_url=url_for('addpost'))
	else:
		return redirect(url_for('login'))

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

@app.route('/addcomment', methods=['POST'])
def addcomment():
	postid = request.form['postid']
	commentusername = request.form['username']
	commentcontent = request.form['commentcontent']
	controller.addComment(postid, commentusername, commentcontent)
	return redirect('/postdetail/' + postid)

###########################################
if __name__ == '__main__':
	app.run(debug=True)
