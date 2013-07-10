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
    
def insertIntoDb(linkList):
    try:
        db.links.insert(linkList)
    except Exception as e:
        print e
    
def getFromDb():
    try:
        count = db.links.count()
        offset = randrange(0, count)
        link = db.links.find().skip(offset).limit(1)[0]
        return link['link']
    except Exception as e:
        print e

def getLinks(url):
    try:
        cleanList = []
        links = re.findall('href=[\"\'](.[^\"\']+)[\"\']', urllib2.urlopen(url).read(), re.I)
        curTime = time.time()
        for link in links:
            linkParsed = urlparse(link)
            if ("http" in linkParsed.scheme):
                cleanLink = linkParsed.scheme + '://' + linkParsed.netloc
                cleanDict = {"parentLink":url, "link":cleanLink}
                cleanList.append(dict(cleanDict))
                
        uniqueLinks = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in cleanList)]
        print(len(uniqueLinks))
        return uniqueLinks
    except Exception as e:
        print e

def run():
    while True:
        link = getFromDb()
        print("From " + link)
        insertIntoDb(getLinks(link))

threads = []
for i in range(50):
  t = threading.Thread(target=run)
	threads.append(t)
	t.start()
