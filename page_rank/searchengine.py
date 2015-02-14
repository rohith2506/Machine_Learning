import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite

class crawler:
	def __init__(self,dbname):
		self.con = sqlite.connect(dbname)

	def __del__(self):
		self.con.close()
	
	def dbcommit(self):
		self.con.commit()

#Add it to the entry table

	def getentryid(self,table,field,value,createnew = True):
		cur = self.con.execute("select rowid from %s where %s = '%s'" %(table,field,value))
		res = cur.fetchone()
		if res == None:
			cur = self.con.execute("insert into %s (%s) values ('%s')" %(table,field,value))
			return row.lastrowid
		else:
			return res[0]
	

# Add it to the index 

	def AddToIndex(self,url,soup):
		if self.IsIndexed(url): return
		print "Indexing" + url

		text = self.gettextonly(url)
		words = self.separatewords(text)

		urlid = self.getentryid('urllist','url',url)
		
		for i in range(0,len(words)):
			word = words[i]
			
			if word in ignorewords: continue
			wordid = self.getentryid('wordlist','word',word)
			self.con.execute('insert into wordlocation(urlid,wordid,location) values (%d%d%d)' %(urlid,wordid,i))

# Get separate words

	def gettextonly(self,soup):
		v = soup.string
		if v == None:
			c = soup.contents()
			resulttext = ''
			for t in c:
				subtext = self.gettextonly(t)
				resulttext = resulttext + '\n'
			return resulttext
		else:
			return v.strip()


# split words used for indexing

	def separatewords(self,soup):
		splitter = re.compile('//W*')
		return [s.lower() for s in splitter.split(text) if s!='']


#check for whether it is already indexed or not

	def IsIndexed(self,url):
		u = self.con.execute("select rowid from urllist where url = '%s'" % url).fetchone()
		if u!=None:
			v = self.con.execute("select * from wordlocation where urlid = '%d'" %(u[0])).fetchone()
			if v!=None:
				return True
		return False
		
	def AddLinkRef(self,UrlFrom,UrlTo,linkText):
		pass

	def crawl(self,pages,depth = 3):
		for i in range(depth):
			newpages = set()
			for page in pages:
				soup = BeautifulSoup()
				try:
					c = urllib2.urlopen(page)
					soup = BeautifulSoup(c.read())
					self.AddToIndex(page,soup)
				except:
					print "could not open %s page" %(page)
					continue
				
				links = soup('a')
				for link in links:
					if ('href' in dict(link.attrs)):
						url = urljoin(page,link['href'])
						if url.find("'")!=-1: continue
						url = url.split('#')[0]
						if url[0:4]=='http' and not self.IsIndexed(url):
							newpages.add(url)
						linkText = self.gettextonly(link)
						self.AddLinkRef(page,url,linkText)
				self.dbcommit()
			pages = newpages
						
	
	def createindextables(self):
		self.con.execute('create table urllist(url)')
		self.con.execute('create table wordlist(word)')
		self.con.execute('create table wordlocation(urlid , wordid , location)')
		self.con.execute('create table link(fromid integer , toid integer)')
		self.con.execute('create table linkwords(wordid , linkid)')
		self.con.execute('create index wordidx on wordlist(word)')
		self.con.execute('create index urlidx on urllist(url)')
		self.con.execute('create index wordurlidx on wordlocation(wordid)')
		self.con.execute('create index urltoindx on link(toid)')
		self.con.execute('create index urlfromidx on link(fromid)')
		self.dbcommit()
