from pymongo import MongoClient
client = MongoClient('mongodb://ramanan93:sRAM9393@ds151451.mlab.com:51451/indolingo')

db = client.indolingo

def Articles():
    '''articles = [
    {
        'id':1,
        'title':'Article One',
        'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'author':'Ramanan',
        'create_date':'28-05-2017'

    },

    {
        'id':2,
        'title':'Article Two',
        'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'author':'Ramanan',
        'create_date':'28-05-2017'

    },

    {
        'id':3,
        'title':'Article Three',
        'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'author':'Ramanan',
        'create_date':'28-05-2017'

    }
    ]'''

    articles = db.flashcardwords.find()

    if articles:
        return articles
    else:
        articles = [{
            'id':0,
            'fname':'Sorry, no words available!',
            'uname':'Please flag a word to be added to your flashcards. Thanks.',
            'author':'Ramanan',
            'create_date':'28-05-2017'
        }]
        return articles
