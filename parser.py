#!/usr/bin/python

from HTMLParser import HTMLParser
import doctest

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

class BookfiParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.in_exact_match = False
		self.div_count = 0
		self.list_urls = []

	def get_results(self, html):
		"""Renvoie les urls des resultats"""

		self.list_urls = []
		self.feed(html)
		return self.list_urls

	def handle_starttag(self, tag, attrs):
		if ('class', 'resItemBox exactMatch') in attrs:
			self.in_exact_match = True

		else:
			if self.in_exact_match:
				if tag == 'a' and ('title', 'Electronic library download book  ') in attrs:
					self.list_urls.append(get_href(attrs))
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