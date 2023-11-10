from datetime import datetime

from flask import Flask, request, session, jsonify
from flask import render_template
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'A78Zrejn359854tjnsT98j/3yX R~XHH!jmN]LWXT'

#Users
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(25), nullable=False)
    user_password = db.Column(db.String(25), nullable=False)
    def __init__(self, login, password):
        self.user_login = password
        self.user_password = login

#News
class News(db.Model):
    __tablename__ = 'News'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    news_image = db.Column(db.String(25), nullable=False)
    likes_number = db.Column(db.Integer, nullable=False)
    news_name = db.Column(db.String(50), nullable=False)
    news_description = db.Column(db.Text(), nullable=False)
    def __init__(self, news_image, news_name, news_description):
        self.news_image = news_image
        self.likes_number = 0
        self.news_name = news_name
        self.news_description = news_description

class Comments(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    photo_src = db.Column(db.String(25), nullable=False)
    comment_text = db.Column(db.Text(), nullable=False)
    def __init__(self, src, text):
        self.photo_src = src
        self.comment_text = text

#Travel
class Travel(db.Model):
    __tablename__ = 'travel'
    id = db.Column(db.Integer, primary_key=True)
    travel_name = db.Column(db.String(255), nullable=False)
    travel_text = db.Column(db.Text(), nullable=False)
    travel_image = db.Column(db.String(255), nullable=False)
    def __init__(self, name, text, url):
        self.travel_name = name
        self.travel_text = text
        self.travel_image = url

@app.route('/')
def index():
    return render_template('basic.html')

@app.route('/<name>')
def user_index(name):
    return render_template('basic.html', user_name = name)

@app.route('/login', methods=['GET'])
def user_enter():
    message = "Enter your login and password."
    return render_template('login.html', message=message)

@app.route('/login', methods=['POST'])
def user_login():
    login = request.form['login']
    password = request.form['password']
    if User.query.filter_by(user_login=login).all() == []:
        message = "Enter correct login!"
        return render_template('login.html',  message=message)
    else:
        if User.query.filter_by(user_password=password).all() == []:
            message = "Enter correct password!"
            return render_template('login.html', message=message)
        else:
            if 'link' in session:
                session['user'] = login
                return redirect(session['link'])
            else:
                return render_template('login.html')

@app.route('/add_news', methods=['POST'])
def add_news():
    file = request.files['file']
    lastRow = db.session.query(News).order_by(News.id.desc()).first()
    fileName = str(lastRow.id + 1)
    nameParts = file.filename.split('.')
    filenameExtension = nameParts[len(nameParts) - 1]
    fileName += '.' + filenameExtension
    file.save(os.path.join("static", "img", "news", fileName))
    description = request.form['description']
    name = request.form['name']
    row = News(fileName, name, description)
    db.session.add(row)
    db.session.commit()
    return render_template('basic.html')

@app.route('/add_news', methods=['GET'])
def add_news_check():
    if 'user' in session:
        return render_template('add_news.html')
    else:
        session['link'] = '/add_post'
        message = "Enter your login and password."
        return render_template('login.html', message=message)

@app.route('/add_travel', methods=['POST'])
def add_post():
    file = request.files['file']
    lastRow = db.session.query(Travel).order_by(Travel.id.desc()).first()
    fileName = str(lastRow.id + 1)
    nameParts = file.filename.split('.')
    filenameExtension = nameParts[len(nameParts) - 1]
    fileName += '.' + filenameExtension
    file.save(os.path.join("static", "img", "travel", fileName))
    description = request.form['description']
    name = request.form['name']
    row = Travel(name, description, fileName)
    db.session.add(row)
    db.session.commit()
    return render_template('basic.html')

@app.route('/add_travel', methods=['GET'])
def add_post_check():
    if 'user' in session:
        return render_template('travel_add.html')
    else:
        session['link'] = '/add_post'
        message = "Enter your login and password."
        return render_template('login.html', message=message)

@app.route('/travel')
def travel():
    new_post = Travel.query.all()
    return render_template('travel.html', travels=new_post)

@app.route('/api/get/data', methods=['GET'])
def getData():
    js_data = []
    data_example = {}
    data_example['user'] = 'Pol'
    data_example['password'] = '123'
    js_data.append(data_example)
    return jsonify(js_data)

@app.route('/api/get/news/all', methods=['GET'])
def getNews():
    js_all_photos = []
    db_news = News.query.all()
    for row in db_news:
        news_data = {}
        news_data['id'] = row.id
        news_data['image'] = '../static/img/news/' + row.news_image
        news_data['name'] = row.news_name
        news_data['description'] = row.news_description
        news_data['likes'] = row.likes_number
        news_data['commentsNumber'] = Comments.query.filter_by(photo_src=row.news_image).count()
        js_all_photos.append(news_data)
    return jsonify(js_all_photos)

@app.route('/api/get/news/data', methods=['POST'])
def getNewsInformation():
    newsSrcParts = request.form['src'].split('/')
    newsName = newsSrcParts[len(newsSrcParts)-1]
    newsRow = News.query.filter_by(news_image=newsName).first()
    newsCommentsRows = Comments.query.filter_by(photo_src=newsName).all()
    jsNewsData = {}
    jsNewsData['src'] = request.form['src']
    jsNewsData['name'] = newsRow.news_name
    jsNewsData['description'] = newsRow.news_description
    jsNewsData['likes'] = newsRow.likes_number
    newsComments = []
    for row in newsCommentsRows:
        newsComments.append(row.comment_text)
        jsNewsData['comments'] = newsComments
        jsNewsData['commentsNumber'] = 0 + len(newsComments)
    return jsonify(jsNewsData)

@app.route('/api/add/photo/comments', methods=['POST'])
def uploadComment():
    photo_src = request.form['src'].split('/')
    newsName = photo_src[len(photo_src) - 1]
    commentText = request.form['comment']
    commentRow = Comments(newsName, commentText)
    db.session.add(commentRow)
    db.session.commit()
    return ''

@app.route('/api/update/add/likes', methods=['POST'])
def addNewsLikes():
    news_src = request.form['src'].split('/')
    newsName = news_src[len(news_src) - 1]
    row = News.query.filter_by(news_image=newsName).first()
    row.likes_number += 1
    db.session.commit()
    return ''

@app.route('/api/update/delete/likes', methods=['POST'])
def deleteNewsLikes():
    news_src = request.form['src'].split('/')
    newsName = news_src[len(news_src) - 1]
    row = News.query.filter_by(news_image=newsName).first()
    row.likes_number -= 1
    db.session.commit()
    return ''

if __name__ == "__main__":
   app.run()