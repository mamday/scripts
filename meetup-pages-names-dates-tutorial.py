from __future__ import unicode_literals

import requests
import urllib
import json
import time
import codecs
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


def main():

        cities =[("Seattle","WA")]
        api_key= open(sys.argv[1]).readlines()[0] 
        # Get your key here https://secure.meetup.com/meetup_api/key/
        for (city, state) in cities:
            per_page = 200
            results_we_got = per_page
            offset = 0
            while (results_we_got == per_page):
                # Meetup.com documentation here: http://www.meetup.com/meetup_api/docs/2/groups/
                response=get_results({"sign":"true","country":"US", "city":city, "state":state, "radius": 10, "key":api_key, "page":per_page, "offset":offset })
                time.sleep(1)
                offset += 1
                #print response
                results_we_got = response['meta']['count']
                for group in response['results']:
                    category = ""
                    if "category" in group:
                        category = group['category']['name']
                    print "," .join(map(unicode, [city, group['name'].replace(","," "), group['created'], group['city'],group.get('state',""),category,group['members'], group.get('who',"").replace(","," ")]))

            time.sleep(1)


def get_results(params):
        print params
        ma_url = 'http://api.meetup.com/2/groups?'
        count=0
        for key,val in params.iteritems():
          count+=1
          print key,val
          if(count<(len(params))):
            ma_url+=str(key).rstrip()+'='+str(val).rstrip()+'&' 
          else:
            ma_url+=str(key).rstrip()+'='+str(val).rstrip() 
        print ma_url
        #data = request.json()
        request=urllib.urlopen(ma_url)	
        data = json.loads(request.read())
	return data


if __name__=="__main__":
        main()


## Run this script and send it into a csv:
## python meetup-pages-names-dates.py > meetup_groups.csv
