from bs4 import BeautifulSoup
import json
import html5lib
import sys, getopt
import os
from data_parsing_script import find_coordinates

def write_json(data,filename):
  with open(filename,"w") as outfile:
    json.dump(data,outfile)
    
def data_parsing(input_html,output_json):
    with open (input_html, "r") as myfile:
      data = myfile.read()
    soup = BeautifulSoup(data,'html5lib')
    n = soup.findAll('table')[7].findAll('table')
    output = []
    
    for tr in n:
        project_name = tr.findAll('td')[1].text.strip().title()
        property_type = tr.findAll('td')[3].text.strip().title()
        name = project_name + ' - ' + property_type
        top = tr.findAll('td')[5].text.split()
        road = tr.findAll('td')[9].text.strip().title()
        coords = find_coordinates(road +',Singapore')
        result = {"name":name,
                  "top":top[0],
                  "address":road,
                  "coords":coords}
        output.append(result)
    write_json({'sites':output},output_json)
    

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


#Calling the functions
(i,o) = parameterize_script()

try:
  data_parsing(i,o)
except:
  print("Usage: %s -i input -o output" % sys.argv[0])


