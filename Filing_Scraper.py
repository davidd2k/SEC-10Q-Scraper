import urllib, csv
from bs4 import BeautifulSoup,NavigableString

import urlparse

class Filing_Scraper(object):

    def getDateHeaders(self, soup):
        
        dateInfo= []
         
        periods = soup.find_all("th", {'class':"tl", "rowspan":2})
        doubleRowHeader = False
        if len(periods) > 0:
            doubleRowHeader = True
        dates = []
        if doubleRowHeader:
            dates = soup.find_all("tr")[1].find_all("th")
        else:
            dates = soup.find_all("tr")[0].find_all("th")
        for td in dates:
            if td.get('class')[0] == "tl":
                continue
            
            dateStr = td.text
            dateInfo.append(dateStr.replace(",", " ").replace(".", " "))
            
        return dateInfo


    def getData(self, cik, toUrl, csv_outfile):        
        web_cnx = urllib.urlopen(toUrl)
        html = web_cnx.read()
        
        if "key does not exist" in html:
            print("No data for "+ toUrl)
            return
        
        soup = BeautifulSoup(html)
        #Getting the dates!
        dateInfo = self.getDateHeaders(soup)
        
        typeTitle = ""
        productType = ""
        rows = soup.find_all("tr")


        for row in rows:
            if not row.has_key('class'):
                continue 
            
            if row.get('class')[0] == "rh":
                typeTitle = row.find("td").text
                continue
                
            if typeTitle != "" and row.get('class')[0] == "re":
                cells = row.find_all("td")
                
                col = 0;
                
                for cell in cells:
                    if cell.get('class')[0] == "pl":
                        productType = cell.text
                    else:
                        #outputrow = ( +","+  +","+  +"," + 
                        row = [
                            cik,
                            typeTitle.replace(",", "-").encode('utf-8').rstrip('\r\n'),
                            productType.encode('utf-8').rstrip('\r\n'),
                            dateInfo[col].encode('utf-8').rstrip('\r\n'),
                            cell.text.encode('utf-8').rstrip('\r\n')
                        ]
                        
                        if "Interest Rate" in row[1] or "Currency"in row[2]:
                            csv_outfile.writerow(row)
                            
                        if "FX" in row[1] or "FX" in row[2]:
                            print("May be of interest: "+ row)


    def getURLToSearch(self, inputUrl):
        url = urlparse.urlparse(inputUrl)
        params = urlparse.parse_qs(url.query)
        cik = params['cik'][0]
        accessionNumber = params['accession_number'][0]
        accessionNumber = accessionNumber.replace('-', '')
        toUrl = "https://www.sec.gov/Archives/edgar/data/{CIK}/{accessionNumber}/R48.htm".format(CIK=cik, accessionNumber=accessionNumber)
        return toUrl, cik

    def scrape10Qs(self):        
        outfile = 'Swap_FX_Data.csv'
        w_outfile = open(outfile,'w')
        a_outfile = open(outfile,'a')
        csv_outfile = csv.writer(a_outfile)
        
        # wipe the file
        w_outfile.write('')
        
        # insert headers
        headers = ['CIK', 'Header', 'Product', 'Date', 'Amount']
        csv_outfile.writerow(headers)
        
        with open('10Qs.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                try:
                    toUrl, cik = self.getURLToSearch(row[0])
                    print(toUrl)
                    self.getData(cik, toUrl, csv_outfile)
                except:
                    print("Error with "+ row[0])
                    
        
       # inputUrl = "https://www.sec.gov/cgi-bin/viewer?action=view&cik=1050797&accession_number=0001050797-15-000008&xbrl_type=v"
        
        
        
        # /cgi-bin/viewer?action=view&cik=1233275&accession_number=0001233275-13-000017&xbrl_type=v
        #toUrl = "https://www.sec.gov/Archives/edgar/data/1050797/000105079715000008/R48.htm"
        
                      
                      
                      
        #toUrl = "https://www.sec.gov/Archives/edgar/data/721371/000072137116000221/R48.htm"
        #print toUrl
        
            
        
                             
        
        