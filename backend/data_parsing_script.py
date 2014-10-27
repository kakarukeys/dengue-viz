from bs4 import BeautifulSoup
import json
import html5lib
import re
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from pygeocoder import Geocoder
from pygeocoder import GeocoderError
import sys, getopt
import os
import shelve

def parameterize_script():
  ifile=''
  ofile=''
  try:
    myopts, args = getopt.getopt(sys.argv[1:],"i:o:")
  except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -i input -o output" % sys.argv[0])
    sys.exit(2)
  for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a

  return (ifile,ofile)

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

def coords_google_api(place):
  try:
    geo = Geocoder.geocode(place)
    coords = geo[0].coordinates
    if coords[0]:
      print (coords[0])
      location = [ coords[0],coords[1] ]
      return location
  except:
    print("Geopy")
    location = [0.0,0.0]
    return location
    
def coords_nominatim_api(place):
  try:
    geolocator = Nominatim()
    location = geolocator.geocode(place)
    location = [ location.latitude,location.longitude ]
    return location
  except:
    print("Nominatim")
    location = [0.0,0.0]
    return location

def find_coordinates(place):
  coords = coords_google_api(place)
  if coords == [0.0,0.0]:
    coords = coords_nominatim_api(place)
  return coords
    
   
    
def find_coordinates_memoized(place):
  if place not in memory:
        l = correct_format(place)
        location = find_coordinates(l)
        memory[place] = location
       

  return memory[place]

def get_date(soup):
    date = soup(text=re.compile(r'As at'))[0]
    date = date[date.index("at")+3:]
    date_object = datetime.strptime(date,"%d %B %Y")
    date = date_object.strftime('%Y-%m-%d')
    return date

def get_table(soup):
  tables = soup.findAll("table", { "class" : "MsoNormalTable" })
  ind = 0
  for i in range(0,3):
    try:
      ans = tables[i].findAll('tr')[0].findAll('p')[4].b.text
      if ans == 'Breakdown':
        ind = i + 1
    except:
      pass
  tables = soup.findAll("table", { "class" : "MsoNormalTable" })[ind:]
  return tables
  
def get_location_and_cases(tables):
    total = []
    for table in tables:
        t = table.findAll('tr')[1:]
        for tr in t:
            output = {'name': ' '.join(tr.findAll('td')[0].text.split()),
                      'total': ' '.join(tr.findAll('td')[1].text.split()),
                      'coords':  find_coordinates_memoized(' '.join(tr.findAll('td')[0].text.split()))}
            total.append(output)
            print(output) 
    return total

def read_file(file):
  try:
    with open (file, "r") as myfile:
      data = myfile.read()
      return data
  except IOError:
      print("File Doesn't Exist")
      
  

def write_json(filename,data):
  with open(filename,"w") as outfile:
    json.dump(data,outfile) 

def parsing_script(input_html,output_json):
    data = read_file(input_html)
    soup = BeautifulSoup(data,'html5lib')
    date = get_date(soup)
    tables = get_table(soup)
    cases = get_location_and_cases(tables)
    output = {"snapshots" : [{"date":date,"cases":cases}]}
    write_json(output_json,output)      


memory = shelve.open("memory_coords")

if __name__ == '__main__':
  (i,o) = parameterize_script()
  parsing_script(i,o)
  memory.close()
#parsing_script("C:/Users/Sameed/Desktop/new.htm","datanew.json")

