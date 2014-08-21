from lxml import etree
import urllib2
from lxml import html
from datetime import datetime
import json


#Opening a Connection with Page
response = urllib2.urlopen("file:///C:/Users/Sameed/Desktop/html/data20140815.html")


#Reading a Page
page = response.read()

#Getting tree from page
tree = html.fromstring(page)

#Obtaining Date by xpath
date = tree.xpath("//table//table//p/b/u/span/text()")
date = ' '.join(date[0].split())

#Removing Unwanted characters
date = date[date.index("at")+3:]
print date

#Converting from string to datetime object
date_object = datetime.strptime(date,"%d %B %Y")
print date_object

#Getting only date
date_object = date_object.date()
print date_object
date = date_object.strftime('%Y-%m-%d')

for bad in tree.xpath("//span[contains(@style,'mso-spacerun:yes')]"):
    bad.getparent().remove(bad)

location = []
#Getting Location
for td in tree.xpath('//table[@class="MsoNormalTable"]//table[@class="MsoNormalTable"]//tr/td[1]/p[not(b)]'):
    location.append(' '.join(td.text_content().split()))

print len(location)

#Geting cases
total = tree.xpath('//table[@class="MsoNormalTable"]//table[@class="MsoNormalTable"]//tr/td[2]/p/span/text()')
print len(total)

if len(total) == len(location):
    cases = [{"name": l , "total": t} for l,t in zip(location,total)]
    print len(cases)
else:
    print "missing values"

#Formating the data
output = {"snapshots" : [{"date":date,"cases":cases}]}
print output

#Dumping the data into json file
with open("data20140815.json","w") as outfile:
    json.dump(output,outfile)




 

