from lxml import etree
import urllib2
from lxml import html
from datetime import datetime
import json
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from pygeocoder import Geocoder
from pygeocoder import GeocoderError
import re

def correct_format(text):
  match=re.findall(r'\((.+?)\)',text)
  match =  ",".join(match)
  if match:
    match_with_brackets = '('+match+')'
    trimmed_sentence = text.replace(match_with_brackets,"")
    match = match.replace("Blk","")
    match = match.strip()
    modified_sentence = match+' '+ trimmed_sentence.strip() + ",Singapore"
    return modified_sentence
  else:
    return text + ",Singapore"

def find_coordinates(place):
  #print place
  try:
    geo = Geocoder.geocode(place)
    coords = geo[0].coordinates
    if coords[0]:
      print coords[0]
      location = [ coords[0],coords[1] ]
      return location
  except GeocoderError:
    geolocator = Nominatim()
    location = geolocator.geocode(place)
    #print(location.latitude,location.longitude,location.address)
    location = [ location.latitude,location.longitude ]
    return location

def write_json(filename,data):
  with open(filename,"w") as outfile:
    json.dump(data,outfile)

  

  
#Opening a Connection with Page
response = urllib2.urlopen("file:///C:/Users/Sameed/Desktop/html/data20140815.html")

#Reading a Page
page = response.read()

#Getting tree from page
tree = html.fromstring(page)
#Getting Date by xpath
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
    #cases = [{"name": l , "total": t} for l,t in zip(location,total)]
    cases = []
    for l,t  in zip(location,total):
        formatted_location = correct_format(l)
        c = find_coordinates(formatted_location)
        cases.append({"name" : l,"total" : t,"coords" : [c[0] , c[1]] })
else:
    print "missing values"
print len(cases)

#Formating the data
output = {"snapshots" : [{"date":date,"cases":cases}]}
print output

write_json("marker_data.json",output)




 

