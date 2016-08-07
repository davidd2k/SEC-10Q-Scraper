from CIK_Scraper import Scraper
from Filing_Finder import Filing_Finder
from Filing_Scraper import Filing_Scraper
import urllib, csv
from bs4 import BeautifulSoup,NavigableString





print('Hello')

filingScraper = Filing_Scraper()
filingScraper.scrape10Qs()

#scraper = Scraper()
#scraper.getSIKCodes()

#finder = Filing_Finder()
#finder.get10QUrls()

