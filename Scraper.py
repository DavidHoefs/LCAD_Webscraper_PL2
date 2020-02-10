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

# getting address from arcGIS from GPS coordinates
gis = GIS("https://hoefsdavid9701.maps.arcgis.com", "hoefsdavid9701", "9989Jada!!")
results = reverse_geocode([-101.846811, 33.625072]) # Will need to flip these around programmatically
valueFromGIS = results["address"]["Match_addr"]


# function to insert underscore into address string for LCAD scraping
def insert_underscore(string, index):
    return string[:index] + '_' + string[index:]


# Modify address string from arcGIS to be in correct format for LCAD scraping
valueFromGIS = valueFromGIS.upper()
inputForScrape = valueFromGIS[0:12]
inputForScrape = insert_underscore(inputForScrape, 5)
inputForScrape = insert_underscore(inputForScrape, 10)
inputForScrape = ''.join(inputForScrape.split())
print(inputForScrape)


# class to hold home owner information from LCAD scraping
class HomeOwner:
    def __init__(self, propertyid, account, name, address, value):
        self.propertyId = propertyid
        self.account = account
        self.name = name
        self.address = address
        self.value = value


# concatinating address to end of LCAD search URL
url = 'http://lubbockcad.org/Property-Search-Result/searchtext/' + inputForScrape
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
