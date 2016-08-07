import urllib, csv
from bs4 import BeautifulSoup,NavigableString

class Filing_Finder(object):
        

    def urlsToSearch(self, spamreader):
        urls = []
        baseUrl = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany'
        for row in spamreader:
            urls.append(baseUrl.format(row[1]))
        
        return urls

    def get10QUrls(self):
        outfile = '10Qs.csv'
        w_outfile = open(outfile,'w')
        a_outfile = open(outfile,'a')
        csv_outfile = csv.writer(a_outfile)
        
        # wipe the file
        w_outfile.write('')
        
        # insert headers
        headers = ['10QUrl']
        csv_outfile.writerow(headers)
        
        with open('sics.csv', 'rb') as csvfile:
             spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        
             urls = self.urlsToSearch(spamreader)
        
             urls10Q = []
        
             for url in urls:
                foundInteractive10Q = False
                web_cnx = urllib.urlopen(url)
                html = web_cnx.read()
                soup = BeautifulSoup(html)
        
                for tr in soup.find_all("tr"):
                    found10Q = False
        
                    for td in tr:        
                        if found10Q and type(td) is not NavigableString:             
                                          
                           links = td.find_all('a')
                           
                           if links is not None and links != -1:
                              for link in links:
                                 try:
                                     if "interactiveDataBtn" in link['id']:
                                        print('Found interactive 10q')
                                        urls10Q.append(link['href'])
                                        found10Q = False                                        
                                 except:
                                     pass
                        if '10-Q' == td.string:
                           print('Found 10Q')
                           found10Q = True 
                        
                        if len(urls10Q) >= 10: 
                           for url in urls10Q:
                              print(url)
                              csv_outfile.writerow([url])
                           urls10Q = []
                 
             