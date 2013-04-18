#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.1'
__author__ = 'Isaac Koo (gujiaxi1991@gmail.com)'

'''
Sina Weibo Exporter
'''

from weibo import APIClient
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def oauth(APP_KEY, APP_SECRET, CALLBACK_URL):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

    url = client.get_authorize_url()
    print "Get the code number from here: " + str(url)
    code = raw_input()
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in

    client.set_access_token(access_token, expires_in)
    return client

def getStatuses(client, uid):
    pg = 1
    outputText = '<html>\n<head><meta http-equiv="content-type" content="text/html; charset=UTF-8">\n</head>\n<body>\n'

    while(pg < 5000):
        tl = client.get.statuses__user_timeline(uid=uid, page=pg)
        bd = getBody(tl)
        if not bd:
            break
        outputText += bd
        pg += 1

    outputText += '\n</body>\n</html>'
    
    filename = "export.html"
    toFile(filename, outputText)

def tweetTime(created_at):
    ts = created_at.split(' ')
    ctime = ts[3] + ' ' + ts[0] + ', ' + ts[2] + ', ' + ts[1] + ', ' + ts[5]
    return ctime

def rtStatus(retweeted_status):
    rtData = ''
    rtData += 'RT <a href="http://weibo.com/' + str(retweeted_status['user']['id']) + '">' + '@' + str(retweeted_status['user']['screen_name']) + '</a>: ' + str(retweeted_status['text'])
    return rtData

def getBody(tl):
    body = ''
    if tl['statuses'] == []:
        return False
    for st in tl['statuses']:
        body += st['text'] + '<br />'+'\n'

        if (st.has_key("original_pic")):
            body += '<img src="' + st['bmiddle_pic'] + '" />' + '<br />' + '\n'

        if (st.has_key('retweeted_status')):
            body += '<cite>' + rtStatus(st['retweeted_status']) + '</cite>' + '<br />' + '\n'
            if(st['retweeted_status'].has_key('original_pic')):
                body += '<img src="' + st['retweeted_status']['bmiddle_pic'] + '" />' + '<br />' + '\n'

        body += '<h5><i>'
        if (st.has_key('created_at')):
            body += tweetTime(st['created_at'])
        if (st.has_key('source')):
            body += ' From: ' + st['source']
        body += '</i></h5>'
        body += '<br /><br />' + '\n'
    return body

def toFile(filename, data):
    file = open(filename, 'w')
    file.write(data)
    file.close()

def main():
    APP_KEY = raw_input("APP KEY: ")
    APP_SECRET = raw_input("APP KEY: ")
    CALLBACK_URL = raw_input("CALLBACK URL: ")

    client = oauth(APP_KEY, APP_SECRET, CALLBACK_URL)

    uid = raw_input("The user id: ")
    getStatuses(client, uid)

if __name__ == '__main__':
    main()
