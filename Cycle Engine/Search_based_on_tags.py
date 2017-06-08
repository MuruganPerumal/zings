'''
Action :
    1. split sentace into tags
    2. download data from database based on each tags
    3. check how many tags results have the same unique_id
    4. return common unique article and pages
'''
import nltk
from nltk.corpus import stopwords
import urllib2
import json
import pymongo
from datetime import datetime
import global_variable as var

# Connect mongodb db business layer
try:
    conn=pymongo.MongoClient(var.mongo_client_url)[var.database]
except ConnectionFailure, e:
    sys.stderr.write("Could not connect to MongoDB: %s" % e)
    sys.exit(1)
    
# for last updated date and time    
now = datetime.now()
def searchEngine(sentence):
    print(sentence)
    stop_words = set(stopwords.words("english"))
    tokens = nltk.word_tokenize(sentence)
    filtered_word = []
    for each_Word in tokens:
        if each_Word not in stop_words:
            if len(filtered_word) < 200:
                filtered_word.append(each_Word)
    body_index = list(set(filtered_word))
    tot_result_set = []
    for keys in body_index:
        print(keys)
        cursor = conn.Moogle_indexed_pages.find({"index_tags":keys}).limit(10)
        capa_dic=dict()
        list_capa=list()
        for i in cursor:
            capa_dic['title'] = i['title']
            capa_dic['url'] = i["URL"]
            capa_dic['paragraph_middle'] = i["paragraph_middle"]
            capa_dic['unique_id'] = i["unique_id"]
            list_capa.append( capa_dic.copy() )
        tot_result_set.append(list_capa)

    # Extract the output object list
    first = True
    match_result = dict()
    result_array = []
    second_result_array = []
    for each_result_set in range(len(tot_result_set)):
        if first == True:
            print each_result_set
            reserve = tot_result_set[0]
            first = False
            for each_reserve in reserve:
                for each_object_set in tot_result_set[each_result_set]:
                    if each_reserve["unique_id"] == each_object_set['unique_id']:
                        match_result = each_object_set
                        result_array.append(match_result)
                        #print(each_result_set,"= Match =>",each_object_set['unique_id'])
                    else:
                        #print(each_result_set,"= Not Match =>",each_object_set['unique_id'])
                        second_result_array.append(match_result)

        else:

            for each_reserve in reserve:
                for each_object_set in tot_result_set[each_result_set]:
                    if each_reserve["unique_id"] == each_object_set['unique_id']:
                        match_result = each_object_set
                        result_array.append(match_result)
                        print(each_result_set,"= Match =>",each_object_set['unique_id'])
                    else:
                        print(each_result_set,"= Not Match =>",each_object_set['unique_id'])
                        second_result_array.append(match_result)

    seen = set()
    new_l = []
    for d in result_array:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    for d in second_result_array:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)

    return new_l

#calling search engine with searchable tags
sentence = """Java of program"""
#print(searchEngine(sentence))
'''
# get data from database for each tags
cursor = conn.Moogle_indexed_pages.find().limit(10)
for i in cursor:
    url = i["URL"]
    title = i['title']
    paragraph_middle = i["paragraph_middle"]
    unique_id = i["unique_id"]
    print(url)
    print(title)
    print(paragraph_middle)
    print(unique_id)
'''
