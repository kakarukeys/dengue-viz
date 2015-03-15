#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import glob
import json

from bs4 import BeautifulSoup

from data_parsing_script import find_coordinates_memoized


def data_parsing(input_html):
    with open (input_html, "r", errors="replace") as myfile:
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
        coords = find_coordinates_memoized(road +',Singapore')
        result = {"name":name,
                  "top":top[0],
                  "address":road,
                  "coords":coords}
        output.append(result)
    return output

def process_html_files(all_files):
    sites = [site for input_html in all_files for site in data_parsing(input_html)]
    return {"groups": [{
        "name": "construction sites",
        "sites": sites
    }]}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process property data.')
    parser.add_argument("-i", metavar="input htm", help="Input files")
    parser.add_argument("-o", metavar="output json", type=argparse.FileType('w'), help="Output file")

    args = parser.parse_args()
    results = process_html_files(glob.glob(args.i))
    json.dump(results, args.o)
