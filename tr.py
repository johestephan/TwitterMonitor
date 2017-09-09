import twitter
import re
import json
import requests
from bs4 import BeautifulSoup
import os
import sys
import syslog

sys.path.append("./")
import sendmail
import MYTRconfig

api = twitter.Api(consumer_key=MYTRconfig.consumer_key,
                      consumer_secret=MYTRconfig.consumer_secret,
                      access_token_key=MYTRconfig.access_token_key,
                      access_token_secret=MYTRconfig.access_token_secret)

infile = open("Leaktweets.txt","r")
OldLeaks = infile.read()
infile.close()

outfile = open("Leaktweets.txt","a")

keywords = MYTRconfig.keywords

message = ""
print("Starting looking for: %s" % ",".join(keywords))
for item in api.GetListTimeline(MYTRconfig.TimeID):
        try:
                newD = json.loads(str(item))
                d1 = (newD["urls"][0]["url"])
                d2 = (newD["text"])
                d3 = (newD["id_str"])

                if not d3 in OldLeaks:
                        print("New one %s" % d3)
                        outfile.write('''%s: %s, %s\n''' % (d3, d2, d1))
                        r = requests.get(d1)
                        p1 = r.text
                        soup = BeautifulSoup(p1 , "html5lib")
                        pp1 = soup.get_text()
                        meska = ('''\n%s: %s, %s\n''' % (d3, d2, d1))
                        
                        # Save the website for caching
                        filename = "./CACHE/%s.txt" % d3
                        outfile1 = open(filename, "wb")
                        outfile1.write(bytes(pp1, 'UTF-8'))
                        outfile1.close()

                        for word in keywords:
                                Findings = set()
                                reg1 = re.compile("([a-zA-Z0-9\+\._-]+\@([a-zA-Z0-9-]+\.|\.|)%s)" % word)
                                for item in reg1.findall(pp1.lower()):
                                    Findings.add(item)
                                print(len(Findings))
                                if len(Findings) > 0:   
                                    logmessage = '''TwitterBot found %s (sum: %s) in %s (ID: %s)\n''' % (word, len(Findings), d1,d3)
                                    syslog.syslog(logmessage)
                                    print(logmessage)

                else:
                        print("Old one %s" % d3)
              
                
        except Exception as e:
                print(e.__doc__)
                print(e.message)
outfile.close()
if len(message) > 10:
        print(message)
        sendmail.send(message)

