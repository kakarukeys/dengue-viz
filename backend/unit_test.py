import unittest
from data_parsing_script import *
from bs4 import BeautifulSoup
import re
import html5lib
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from pygeocoder import Geocoder
from pygeocoder import GeocoderError

class SimplisticTest(unittest.TestCase):

    def setUp(self):
        self.data = read_file("C:/Users/Sameed/Desktop/Work/html/data20140624.htm")
        self.soup = BeautifulSoup(self.data,'html5lib')
        self.tables = get_table(self.soup)
        
    def test_date(self):
        self.assertIsInstance(get_date(self.soup), str)
        
    def test_date_length(self):
        self.assertEqual(len(get_date(self.soup)),10)

    def test_location_and_cases(self):
        self.assertIsInstance(get_location_and_cases(self.tables),list)

    def test_location_and_cases_not_empty(self):
        self.assertNotEqual(get_location_and_cases(self.tables),None)
    
            
    def test_correct_format_without_Blk(self):
        text = "Aroozoo Avenue"
        c = correct_format(text)
        self.assertEqual(c,"Aroozoo Avenue,Singapore")

    def test_correct_format_with_Blk(self):
        text = "Lorong Ah Soo (Blk 143)"
        c = correct_format(text)
        self.assertEqual(c,"143 Lorong Ah Soo,Singapore")

    def test_find_coordinates(self):
        coords = find_coordinates("143 Lorong Ah Soo,Singapore")
        self.assertAlmostEqual(coords,[1.3524529, 103.882963])

    def test_get_table(self):
        self.assertIsInstance(get_table(self.soup),list)    
    
if __name__ == '__main__':
    unittest.main()
