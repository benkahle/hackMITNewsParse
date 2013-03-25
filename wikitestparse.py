import urllib2
import re
from bs4 import BeautifulSoup

hdrs = { 'User-Agent': "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11" } 

def grab_links(url):
	req = urllib2.Request(url, headers=hdrs)
	openedpage = urllib2.urlopen(req)
	html = openedpage.read()
	soup = BeautifulSoup(html)
	text = soup.get_text()
	refs = find_ref(text)
	print refs

def find_ref(text):
	"""From a body of text with references as '[[refexample]]' returns a list of all reference strings."""
	startref = '[['
	endref = ']]'
	regex1 = re.compile(startref)
	regex2 = re.compile(endref)
	startloc = [a.end()+1 for a in regex1.finditer(text)]
	endloc = [a.start() for a in regex2.finditer(text)]
	refcaps = zip(startloc,endloc)
	reflist = []
	for a,z in refs:
		reflist.append(text[a:z])
	return reflist

def form_link(page):
	baselinka = 'http://en.wikipedia.org/w/api.php?format=xml&action=query&titles='
	baselinkb = '&prop=revisions&rvprop=content'
	url = baselinka+page+baselinkb
	return url

grab_links(form_link('Mug'))