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
		self.in_title = False
		self.in_author = False
		self.div_count = 0
		self.title = ""
		self.author = ""
		self.url = ""
		self.results = []

	def get_results(self, html):
		"""Renvoie les resultats"""

		self.title = ""
		self.author = ""
		self.url = ""
		self.results = []
		self.feed(html)
		return self.results

	def handle_starttag(self, tag, attrs):
		if ('class', 'resItemBox exactMatch') in attrs:
			self.in_exact_match = True

		else:
			if self.in_exact_match:
				if tag == 'a':
					if ('title', 'Electronic library download book  ') in attrs:
						self.url = get_href(attrs)
						el = {'title': self.title, 'author': self.author, 'url': self.url}
						self.results.append(el)
					elif ('title', "Find all the author's book") in attrs:
						self.in_author = True
				elif tag == 'a':
					print attrs
				elif tag == 'div':
					self.div_count += 1
				elif tag == 'h3':
					self.in_title = True

	def handle_data(self, data):
		if self.in_title:
			self.title = data
		elif self.in_author:
			self.author = data

	def handle_endtag(self, tag):
		if self.in_exact_match and tag == 'div':
			if self.div_count == 0:
				self.in_exact_match = False
			else:
				self.div_count -= 1
		elif self.in_title and tag == 'h3':
			self.in_title = False
		elif self.in_author and tag == 'a':
			self.in_author = False

if __name__ == '__main__':
	doctest.testmod()
