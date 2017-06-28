# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 18:56:12 2017

@author: ramanan
"""
# -*- coding: utf-8 -*-
from bson.json_util import dumps

from pymongo import MongoClient
client = MongoClient('mongodb://ramanan93:sRAM9393@ds151451.mlab.com:51451/indolingo')


db = client.indolingo
sentences = db.translation
loadSentences1 = dumps(sentences.find({'filelang':'hi','transtolang':'en'},{'sentences':1}))
loadSentences2 = sentences.find_one({'filelang':'en','transtolang':'hi'},{'sentences':1})

print loadSentences2['sentences'][0]
