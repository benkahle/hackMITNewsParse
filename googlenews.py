import urllib2
import re
from bs4 import BeautifulSoup

hdrs = { 'User-Agent': "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11" } 

def grab_links(url):
	req = urllib2.Request(url, headers=hdrs)
	openedpage = urllib2.urlopen(req)
	html = openedpage.read()
	soup = BeautifulSoup(html)
	titles = soup.find_all('div', class_='basic-title')
	spans = soup.find_all('span', class_='section-name')
	links = find_links(titles)
	sections = find_sections(spans)
	sect_link = zip(sections,links)
	sect_dict = {}
	# for section in sect_link: #run for all sections
	#  	sect_dict[section] = into_section(section) #dictionary of {section: (articletitle,link),(,)...} for all sections
	articles = into_section(sect_link[0]) #list of tuples (articletitle, link) for just the first section

def create_article_weight(article):
	url = article[1]
	articleconn = urllib2.Request(url, headers=hdrs)
	openedpage = urllib2.urlopen(articleconn)
	articlehtml = openedpage.read()
	articleparse = BeautifulSoup(articlehtml)
	articletext = articleparse.text
	paragraphs = articleparse.find_all('p')
	text = ''
	for tag in paragraphs:
		tag = str(tag)
		tag = re.sub(r"([<]{1})(.*?)([>]{1})",'',tag)
		if tag.find('<w:') == -1 and tag.find('|') == -1 and len(tag) >= 50:
			text = text+tag #string of all text fitting the above parameters (mostly the main article)
	print text
	#create_hist(text)
	
# def create_hist(text):
# 	d = dict()
# 	text = text.split()
# 	for c in text:
# 		d[c] = d.get(c,0)+1
# 	l = d.keys() 		#grabs keys into new list
# 	l.sort()			#sorts keys alphabetically
# 	for i in l:	
# 		print i, d[i]	#prints keys and their values in new order

def into_section(section):
	sectionlink = section[1]
	url = 'http://news.google.com'+ sectionlink
	sectionconn = urllib2.Request(url, headers=hdrs)
	openedpage = urllib2.urlopen(sectionconn)
	sectionhtml = openedpage.read()
	sectionparse = BeautifulSoup(sectionhtml)
	# articletitles = sectionparse.find_all('span', class_='titletext')
	tag = sectionparse.find_all('h2', class_='esc-lead-article-title')
	articlelist = find_art(tag)
	create_article_weight(articlelist[0]) #list of tuples of (articlename,link) for all articles in a section

def find_art(tag):
	startlink = 'href='
	endlink = '" id='
	startname = '<span class="titletext">'
	endname = '</span>'
	articlelist = []
	for article in tag:
		articlehtml = str(article)
		startloclink = articlehtml.find(startlink)+6
		endloclink = articlehtml.find(endlink,startloclink)
		articlelink = articlehtml[startloclink:endloclink]
		startlocname = articlehtml.find(startname)+24
		endlocname = articlehtml.find(endname,startlocname)
		articlename = articlehtml[startlocname:endlocname]
		articlelist.append((articlename,articlelink))
	return articlelist #list of tuples of (articlename,link) of all articles in a section

def find_sections(sectionspan):
	startref = 'name">'
	endref = '</span>'
	sectionlist = []
	for section in sectionspan:
		span = str(section)
		startloc = span.find(startref)+6
		endloc = span.find(endref,startloc)
		sectionstring = span[startloc:endloc]
		if sectionstring.find('\xc2') != -1:
			sectionstring = sectionstring[:-4]
			sectionlist.append(sectionstring)
	return sectionlist #list of section titles on the main page in order

def find_links(titlespan):
	startref = 'href="'
	endref = '">'
	linklist = []
	for title in titlespan:
		span = str(title)
		startloc = str.find(span,startref)+6
		endloc = str.find(span,endref,startloc)
		linkcaps = (startloc,endloc)
		linkstring = span[startloc:endloc]
		if linkstring.find('news') != -1 and linkstring.find('topic=ir') == -1 and linkstring.find('geo=detect_metro_area') == -1:
			linkstring = linkstring.replace('&amp;','&')
			linklist.append(linkstring)
	return linklist #list of section links on the main page in order

grab_links('http://news.google.com')