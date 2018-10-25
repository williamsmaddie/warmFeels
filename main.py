import twurl
import urllib.request, urllib.parse, urllib.error
import ssl
import json
import sqlite3

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py
TWITTER_URL = 'https://api.twitter.com/1.1/search/tweets.json'
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


## set up our beautiful databaseu

conn = sqlite3.connect('warmFeels.sqlite')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS Tweets (user TEXT, tweet TEXT, date TEXT)')


##

while True:
    print('')
    acct = input('Say hi: ')
    if (len(acct) < 1): break
    url = twurl.augment(TWITTER_URL, {'q': 'global warming', 'result_type': 'mixed'})
    # How to keep track of results? How to keep track of sampling interval? I'm limited to the past 7 days.
    # One idea: Ask to collect a random sample from 7 days in the past.
    print('Retrieving', url)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    print(json.dumps(js, indent=2))

    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])
    # How do I keep track of what tweets i've already added? Is there a concept of pagination results?


    for st in js['statuses']:

        ## writing each status to the database
        tw = st['text']

        if 'text' not in st:
            tw = ' * No text found'
            continue
        u = st['user']['screen_name']

        #consider checking by ID field?
        cur.execute('SELECT * FROM Tweets WHERE tweet = ? ', (tw,))
        row = cur.fetchone()
        if row is None:
            ## need to add date here
            cur.execute('''INSERT INTO Tweets (user, tweet)
                    VALUES (?,?)''', (u, tw))

        else:
            print('hey silly, you are repeating your calls to the API! I just came across the same tweet again.')
            print('the tweet is ', u, tw)
            continue
            ## need to add date here
            # cur.execute('UPDATE Tweets SET count = count + 1 WHERE email = ?',
            #             (email,))
        conn.commit()

        ##

        print(st['text'])
        if 'text' not in st:
            print(' * No text found')
            continue
        u = st['user']['screen_name']
        print(' ', u[:50])
# Code: http://www.py4e.com/code3/twitter2.py
