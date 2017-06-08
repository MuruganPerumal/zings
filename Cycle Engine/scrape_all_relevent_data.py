
'''
Action:
    1. Scrap datas from the websites 
'''

import nltk
from nltk.corpus import stopwords
#nltk.download()
import socket
import urllib2
import json
from bs4 import BeautifulSoup
from datetime import datetime
from time import gmtime, strftime
import time
import re

#import pip
#pip.main(['install','nltk'])
#import pandas as pd
import pymongo
import global_variable as var

# timeout in seconds
timeout = 5
socket.setdefaulttimeout(timeout)

# Connect mongodb db business layer
try:
    conn=pymongo.MongoClient(var.mongo_client_url)[var.database]
except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)

# for last updated date and time    
now = datetime.now()

# dynamic URL changes with content
def load_webpage(url):
    try:
        each_page_dic = dict()
        list_capa = list()
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        #html = soup.contents
        title_tag = soup.find_all('title')
        title = title_tag[0].text
        body_tag = soup.find_all('body')[0].text
        body_element = soup.find_all('body')[0]
        paragraph_tag = soup.find('meta', {"name":"description"})
        paragraph_middle = paragraph_tag['content']
        
        index_test_tag = soup.find('meta', {"name":"keywords"})
        index_test_middle_tag = index_test_tag['content']
        #print(index_test_middle_tag)
        #print(paragraph_tag[len(paragraph_tag)/2].text)
        stop_words = set(stopwords.words("english"))
        #sentence = """At eight o'clock on Thursday morning... Arthur didn't feel very good."""
        title_token = nltk.word_tokenize(title)
        tokens = nltk.word_tokenize(index_test_middle_tag)
        filtered_word = []                    
        for each_Word in tokens:
            if each_Word not in stop_words:
                if len(filtered_word) < 200:
                    filtered_word.append(each_Word)
        body_index = list(set(filtered_word))
        #print(body_with_tags)
        # append with documents to add
        each_page_dic["index_tags"] = body_index
        each_page_dic["title"] = title
        each_page_dic["paragraph_middle"] = paragraph_middle
        each_page_dic["URL"] = url
        # Store the result into database
        #conn.Moogle_indexed_pages.insert(each_page_dic)
        unique_id = "%.20f" % time.time()
        unique_id = unique_id.replace(".", "")
        print("%.20d" % time.time())
        #print(body_index)
        
        conn.Moogle_indexed_pages_1.update({
        'url': url
        },{
        'index_tags':body_index,
        'title':title,
        'paragraph_middle':paragraph_middle,
        'URL':url,
        'unique_id':unique_id
        }, upsert=True, multi=False)
        
        
    except Exception as e:
        print e

# To skip these websites from our history
google = re.compile('google')
zoho = re.compile('zoho')
demo_flynava = re.compile('demo.flynava')
youtube = re.compile('youtube')
facebook = re.compile('facebook')
wifi_hotspot = re.compile('10.10.10.1')
espncricinfo = re.compile('espncricinfo')
confluence = re.compile('confluence.flynava.com')
linkedin = re.compile('linkedin')
wordpress = re.compile('wordpress')
coursera = re.compile('coursera')


# getting the URL from history collection
#cursor = conn.Cycle_History_Murugan.find({'url': {'$not': {'$in':['/google/','/mail/','/demo.flynava/','/www.facebook.com/',
#    '/10.10.10.1/',
#    '/zoho/']}}})
cursor = conn.Cycle_History_Murugan.find({'url': {'$not': {'$in':[google,zoho,demo_flynava,youtube,facebook,wifi_hotspot,espncricinfo,confluence,linkedin,wordpress,coursera]}}})

for i in cursor:
    url = i["url"]
    title = i['title']
    visit_count = i["visit_count"]
    print(url)
    load_webpage(url)

'''
# for testing
test_URL = ["https://www.tutorialspoint.com/java/","http://www.javatpoint.com/java-tutorial"]
for i in test_URL:
    load_webpage(i)
'''   
