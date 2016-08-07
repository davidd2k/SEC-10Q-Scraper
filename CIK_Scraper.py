import urllib, csv
from bs4 import BeautifulSoup

class Scraper():

    def getSIKCodes(self):
        print('Test')
        
        # where the data go
        outfile = 'sics.csv'
        w_outfile = open(outfile,'w')
        a_outfile = open(outfile,'a')
        csv_outfile = csv.writer(a_outfile)
        
        # wipe the file
        w_outfile.write('')
        
        # insert headers
        headers = ['company', 'CIK', 'SIC']
        csv_outfile.writerow(headers)
              
        # a list to hold our data 
        records = []
        
        # parts of paginated urls
        part_url = 'http://www.sec.gov/divisions/corpfin/organization/cfia-'
        pages = ['123', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'uv', 'wxyz']
        ext = '.htm'
        
        # a list to hold our urls
        urls = []
        
        # assemble the urls
        for page in pages:
            full_url = part_url + str(page) + ext
            urls.append(full_url)
        
        # request each url, read the page into beautiful soup
        # then find the tables and get the rows
        for url in urls:
            print(url)
            web_cnx = urllib.urlopen(url)
            html = web_cnx.read()
            soup = BeautifulSoup(html, "lxml")
            table = soup.find(id="cos")
            rows = table.findAll('tr')
            
            # get the data out of each row, append to records list
            for tr in rows[1:]:
                data = tr.findAll('td')
                row = [
                    data[0].text,
                    data[1].text,
                    data[2].text
                ]
                records.append(row)
        
        for row in records:
            print row
            csv_outfile.writerow(row)
                
        return records
            
        