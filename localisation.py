__author__ = 'antoine'

import requests

r = requests.get('http://ip-api.com/json/')

if r.status_code == 200:
    content = r.json()
    print 'ip : ' +content['query']
    print 'lat : ' + str(content['lat'])
    print 'long : ' + str(content['lon'])
    print 'city : ' + str(content['city'])
else:
    print 'il faut tester avec un autre service'