import urllib2
from BeautifulSoup import BeautifulSoup

def go(soup):
	v = soup.string
	if v == None:
		c = soup.contents
		resulttext = ""
		for t in c:
			subtext = go(t)
			resulttext = resulttext + "\n"	
		print resulttext
		return resulttext
	else:
		return v.strip()

site = "http://icpc.amrita.ac.in/"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib2.Request(site, headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page.read())
go(soup)
#links = soup('a')
#for i in range(0,len(links)):
#	print links[i]['href']
