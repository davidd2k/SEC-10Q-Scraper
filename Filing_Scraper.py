import urllib, csv
from bs4 import BeautifulSoup,NavigableString

import urlparse

class Filing_Scraper(object):
    def scrape10Qs(self):
        inputUrl = "https://www.sec.gov/cgi-bin/viewer?action=view&cik=1050797&accession_number=0001050797-15-000008&xbrl_type=v"
        url = urlparse.urlparse(inputUrl)
        params = urlparse.parse_qs(url.query)
        cik = params['cik'][0]
        accessionNumber = params['accession_number'][0]
        accessionNumber = accessionNumber.replace('-', '')
        #toUrl = "https://www.sec.gov/Archives/edgar/data/{CIK}/{accessionNumber}/R48.htm".format(CIK=cik, accessionNumber=accessionNumber)
        toUrl = "https://www.sec.gov/Archives/edgar/data/721371/000072137116000221/R48.htm"
        print toUrl
        web_cnx = urllib.urlopen(toUrl)
        html = web_cnx.read()
        soup = BeautifulSoup(html)
        
        
        dateInfo = []
        
        periods = soup.find_all("th", colspan=2)
        dates = soup.find_all("tr")[1].find_all("th")
        
        for th in periods:
            for td in dates:
                dateStr = th.text + " " + td.text
                dateInfo.append(dateStr.replace(","," ").replace("."," "))
                break
            break
                
        print dateInfo
        print len(dateInfo)
        