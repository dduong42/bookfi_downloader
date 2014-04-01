#!/usr/bin/python

import doctest
import os
import sys
from parser import BookfiParser
from url import *

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:28.0) Gecko/20100101 Firefox/28.0'
URL_PREFIX = 'http://en.bookfi.org/s/?q='

def generate_search_url(query):
	"""Retourne l'url de recherche sur bookfi a partir d'une requete.

	>>> generate_search_url("coucou toi")
	'http://en.bookfi.org/s/?q=coucou+toi'
	>>> generate_search_url("test 2")
	'http://en.bookfi.org/s/?q=test+2'
	>>> generate_search_url("dernier test")
	'http://en.bookfi.org/s/?q=dernier+test'
	"""

	l = query.split()
	return URL_PREFIX + '+'.join(l)

def get_results(url_query):
	"""Retourne la liste des urls des resultats d'une recherche"""

	html = get_page(url_query)
	parser = BookfiParser()
	return parser.get_results(html)

def download(url_download):
	md5 = get_location(url_download)
	os.system('wget "%s" --referer="%s"' % (url_download, md5))

def choose_answer(l):
	"""Demande a l'utilisateur de choisir dans une liste"""

	for index, el in enumerate(l):
		print "[%d] %s" % (index, el)
	while True:
		try:
			i = int(raw_input('Your choice: '))
		except KeyboardInterrupt:
			sys.exit(0)
		if i >= 0 and i < len(l):
			return l([i])
		else:
			print 'Bad choice'

if __name__ == '__main__':
	doctest.testmod()
	while True:
		try:
			query = raw_input('Search: ')
		except KeyboardInterrupt:
			break
		search_url = generate_search_url(query)
		results = get_results(search_url)
		if results:
			choice = choose_answer(results)
			url_download = get_location(choice)
			download(url_download)
		else:
			print 'Not found'
