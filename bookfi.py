#!/usr/bin/python

import doctest
import urllib2
from HTMLParser import HTMLParser


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:28.0) Gecko/20100101 Firefox/28.0'
URL_PREFIX = 'http://en.bookfi.org/s/?q='

def generate_url(query):
	"""Retourne l'url de recherche sur bookfi a partir d'une requete.

	>>> generate_url("coucou toi")
	'http://en.bookfi.org/s/?q=coucou+toi'
	>>> generate_url("test 2")
	'http://en.bookfi.org/s/?q=test+2'
	>>> generate_url("dernier test")
	'http://en.bookfi.org/s/?q=dernier+test'
	"""

	l = query.split()
	return URL_PREFIX + '+'.join(l)

def get_href(attrs):
	"""Retourne la valeur de l'href

	>>> get_href([('href', '/partners/'), ('target', '_blank')])
	'/partners/'
	>>> get_href([('class', 'color2'), ('href', 'http://bookre.org/reader?file=677155')])
	'http://bookre.org/reader?file=677155'
	>>> get_href([('href', 'javascript:void(0)'), ('onclick', 'return false')])
	'javascript:void(0)'
	"""

	for attr, value in attrs:
		if attr == 'href':
			return value
	return None

class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.in_exact_match = False
		self.div_count = 0

	def handle_starttag(self, tag, attrs):
		if ('class', 'resItemBox exactMatch') in attrs:
			self.in_exact_match = True

		else:
			if self.in_exact_match:
				if tag == 'a' and ('title', 'Electronic library download book  ') in attrs:
					print get_href(attrs)
				elif tag == 'div':
					self.div_count += 1

	def handle_endtag(self, tag):
		if self.in_exact_match and tag == 'div':
			if self.div_count == 0:
				self.in_exact_match = False
			else:
				self.div_count -= 1

if __name__ == '__main__':
	doctest.testmod()
	url = generate_url('Python for Data Analysis')
	req = urllib2.Request(url)
	req.add_header('User-agent', USER_AGENT)
	res = urllib2.urlopen(req)
	html = res.read()
	parser = MyHTMLParser()
	parser.feed(html)