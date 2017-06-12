# -*- coding: utf-8 -*-
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, jsonify
from flask_pymongo import PyMongo
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import bcrypt

app = Flask(__name__,static_url_path='/static')

Articles = Articles()

app.config['MONGO_DBNAME'] = 'indolingo'
app.config['MONGO_URI']  = 'mongodb://ramanan93:sRAM9393@ds151451.mlab.com:51451/indolingo'
app.config['SECRET_KEY'] = 'super secret key'

mongo = PyMongo(app)

@app.route('/')
def index():
    #return 'INDEX'
    if 'username' in session:
        return render_template('loginhome.html')
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])#Post method would allow the user to register, Get method returns the registration template
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'uname': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'fname':request.form['fname'], 'lname':request.form['lname'],'uname': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            flash('You were successfully logged in')
            return render_template('loginhome.html')

        flash('The username already exists. Please login to continue.')
        return render_template('login.html')
    return 'User Already exists. Please login.'

@app.route('/signin', methods=['POST'])
def signin():
    user = mongo.db.users
    existing_user = user.find_one({'uname': request.form['username']})

    if existing_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), existing_user['password'].encode('utf-8')) == existing_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('loginhome'))

    flash('Invalid username/password combination. Please retry')
    return redirect(url_for('login'))



@app.route('/loginhome')
def loginhome():
    if 'username' in session:
        return render_template('loginhome.html')

@app.route('/mycourses')
def mycourses():
    return render_template('mycourses.html')


@app.route('/flashcards')
def flashcards():
    articles = mongo.db.users.find()

    if articles:
        return render_template('flashcards.html',articles = articles)
    else:
        articles = [{
            'id':0,
            'fname':'Sorry, no words available!',
            'uname':'Please flag a word to be added to your flashcards. Thanks.',
            'author':'Ramanan',
            'create_date':'28-05-2017'
        }]
        return render_template('flashcards.html',articles = articles)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/process', methods=['POST'])
def process():
    keyword = request.form['word'].encode('utf-8')
    lang = request.form['lang'].encode('utf-8')
    words = mongo.db.search
    word_exists = words.find_one({"word":keyword,"language":lang})

    if word_exists:
        wMeaning = word_exists["meaning"]
        return jsonify({'result':wMeaning})
    return jsonify({'error':'Sorry, we are yet to add this word to our database. Please come back later'})

@app.route('/translate')
def translate():
    return render_template('translate.html')

@app.route('/addFlashcard', methods=['POST'])
def addFlashcard():
    keyword = request.form['word'].encode('utf-8')
    lang = request.form['lang'].encode('utf-8')
    words = mongo.db.search
    word_exists = words.find_one({"word":keyword,"language":lang})

    if word_exists:
        words.update_one({'word':keyword},{"$set":{'flashcardFlag':1},"$currentDate": {"lastModified": True}})
        wMeaning = word_exists["meaning"]
        return jsonify({'result':wMeaning})
    return jsonify({'error':'Sorry, we are yet to add this word to our database. Please come back later'})


if __name__ == '__main__':
    app.run(debug = True)
