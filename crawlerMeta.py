from bs4 import BeautifulSoup
import time, urllib2, re, pymongo, threading
from urlparse import urlparse
from pymongo import Connection
from random import randrange

try:
  # Establish db connection
  connection = Connection('localhost', 27017)
  db = connection.links
   
except Exception as e:
  print('Error connecting to database.')
  print e
	
def updateDb(metadata,metaUpdated,link):
  try:
    db.links.update({"_id":link["_id"]},{"$set" : {"meta":metadata, "metaUpdated":metaUpdated}})        
  except Exception as e:
    print e
    
def getFromDb():
  try:
    count = db.links.count()
    offset = randrange(0, count)
    link = db.links.find().skip(offset).limit(1)[0]
    return link
  except Exception as e:
    print e
	   
def capString(s,l):
  return s if len(s)<=l else s[0:l-3]+'...'

def getMetadata(url):
  try:
    cleanList = []
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html)
    cleanText = soup.get_text()
    return capString(cleanText,10000)
  except Exception as e:
    print e

def run():
  while True:
    link = getFromDb()
    updateDb(getMetadata(link['link']),time.time(),link)
    print 'Updated metadata for ' + link['link']
        
threads = []
for i in range(100):
  t = threading.Thread(target=run)
	threads.append(t)
	t.start()
