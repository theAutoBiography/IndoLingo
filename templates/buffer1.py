# -*- coding: utf-8 -*-
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, jsonify
from flask_pymongo import PyMongo
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import bcrypt
import sys

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
            session['logged_in'] = True
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

@app.route('/translate') #To move to translate main page
def translate():
    return render_template('translate.html')

@app.route('/storeFileDetails', methods=['GET','POST']) #Stores file details that is uploaded by the user
def storeFileDetails():
        data = {"Name":request.form['name'].encode('utf-8'), "Content": request.form['content'].encode('utf-8'), "Sentences":request.form['sentences'].encode('utf-8'), "toLanguage":request.form['tolang'].encode('utf-8'),
        "fileLanguage":reques.form['fromlang'].encode('utf-8')}

        file_name = data["Name"].split("\\")
        file_sentences = data["Sentences"].split(",")
        #data["content"] = request.form['content'].encode('utf-8');
        #data["sentences"] = request.form['sentences'].encode('utf-8');
        #data["language"] = request.form['language'].encode('utf-8');
        #separated_data = data.split('!@#$%,')
        #dataNew = {separated_data[0].split(":")}
        '''translate = mongo.db.translation

        existing_file = translate.find_one({
                            "fname":file_name,
                            "user":session["username"],
                            "transtolang":data["toLanguage"],
                            "filelang":data["fileLanguage"]
                        })

        if existing_file:
            return jsonify({'result':"Please try using a different file name. You have already made a similar request."})
        else:
            translate.insert({
                "fname":file_name[-1],
                "fcontent":data["Content"],
                "sentences":file_sfile_sentences,
                "transtolang":data["toLanguage"],
                "filelang":data["fileLanguage"],
                "tProgress":0
            })'''
        #entry_exits = translate.find_one({"FName":data[0],"Tlanguage":data[3]})
        if data:
            return jsonify({'result':file_name[-1], "sentences":file_sentences[2]})
        return jsonify({'error':'Sorry, we are yet to add this word to our database. Please come back later'})

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

@app.route('/lessonMainPage')
def lessonMainPage():
    return render_template('lessonMainPage.html')

@app.route('/lesson1')
def lesson1():
    return render_template('lesson1.html')

@app.route('/translatePhrase')
def translatePhrase():
    language = {"Language1":request.form["lang1"].encode("utf-8"), "language2":request.form["lang2"].encode("utf-8")}


    return render_template('translatePhrase.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('logged_in', None)
        session.pop('username',None)
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)
