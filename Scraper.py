"""Project Lab 02 Group 1
   Reverse Geolocation and Lubbock County Appraisal District Scraper
   Description: Recieves a GPS coordinates and then obtains an address. Using the address the program
                then scrapes the LCAD webpage for homeowner information such as name
   AUTHOR: DAVID HOEFS """

import time

import requests
from arcgis.geocoding import reverse_geocode
from arcgis.gis import GIS
from bs4 import BeautifulSoup
from scrapy import Selector
from selenium import webdriver
from streetaddress import StreetAddressParser

# getting address from arcGIS from GPS coordinates
gis = GIS("https://hoefsdavid9701.maps.arcgis.com", "hoefsdavid9701", "9989Jada!!")
results = reverse_geocode([-101.935077,33.581268])  # Will need to flip these around programmatically
valueFromGIS = results["address"]["Match_addr"]

# Use streetaddress library to parse address data from arcGIS
addr_parser = StreetAddressParser()
addr = addr_parser.parse(valueFromGIS)


# class to hold home owner information from LCAD scraping
class HomeOwner:
    def __init__(self, propertyid, account, name, address, value):
        self.propertyId = propertyid
        self.account = account
        self.name = name
        self.address = address
        self.value = value


# concatenating address to end of LCAD search URL
url = 'http://lubbockcad.org/Property-Search-Result/searchtext/' + addr['house'] + '_' + addr['street_name'] + '_' + \
      addr['street_type']
print(url)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
# extract homeowner info from LCAD
driver = webdriver.Safari()
driver.get(url)
time.sleep(5)
sel = Selector(text=driver.page_source)
item = sel.xpath('//*[@id="grid"]/div[3]/table/tbody/tr//text()').extract()
driver.quit()
ownerObject = HomeOwner(item[0], item[2], item[3], item[4], item[5])
print(ownerObject.name)
