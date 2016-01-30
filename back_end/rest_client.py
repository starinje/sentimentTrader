#!/usr/bin/env

from urllib2 import Request, urlopen, URLError
import oauth2 as oauth
import simplejson

def getData(url):
    req = Request(url)
    try:
        response = urlopen(req)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
        print '\n'.join(response.readlines())

def postData(url,data):
    req = Request(url)
    try:
        response = urlopen(req,data)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server could not fulfill the request.'
            print 'Error code: ', e.code
    else:
        print '\n'.join(response.readlines())
        

def oauth_req(url, key, secret):
    consumer = oauth.Consumer(key, secret)
    client = oauth.Client(consumer)
    resp, content = client.request(url,"GET")
    result = simplejson.loads(content)
    if 'Error' in result:
        # An error occurred; raise an exception
        raise result['Error']
    return result

#these are our official Twitter OAuth credentials
consumer_key="otI5peYY2lIQogqOsjBTL57K7"
consumer_secret="7PST9jWvv4SrPZMyxVtaeMwAKpAgjlVansNgXHobEKbKNFtCIN"

counter = 0
next_results='?q=%24AAPL&count=100'

while counter < 3:
    url = 'https://api.twitter.com/1.1/search/tweets.json'+next_results
    returned = oauth_req(url,consumer_key, consumer_secret)
    metadata=returned['search_metadata']
    next_results=metadata['next_results']
    #print "Next query:"+next_results
    statuses = returned['statuses']
    counter=counter+1
    for status in statuses:
        print status['text']

#url="http://www.sentiment140.com/api/bulkClassifyJson"
#data='{"data": [{"text": "RT @GEQSense: Why worry about something you have absolutely no control of? When I trade $AAPL every day i know i am not in control. I just"}, {"text": "Apple Stock Price Set To Bounce &amp;#8211; $AAPL http://t.co/bino4O8Nwb via @kourtlandk"}]}'
#postData(url,data)