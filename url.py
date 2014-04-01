#!/usr/bin/python

import urllib2
import re
import httplib

def get_host_n_path(url):
	"""Retourne un couple (host, path) a partir d'une url

	>>> get_host_n_path('http://dl.lux.bookfi.org/genesis/864000')
	('dl.lux.bookfi.org', '/genesis/864000')
	>>> get_host_n_path('https://docs.python.org/2/library/httplib.html')
	('docs.python.org', '/2/library/httplib.html')
	>>> get_host_n_path('http://en.bookfi.org/s/?q=python&t=0')
	('en.bookfi.org', '/s/?q=python&t=0')
	>>> get_host_n_path('http://ldap42.clem.org/')
	('ldap42.clem.org', '/')
	>>> get_host_n_path('http://ldap42.clem.org')
	('ldap42.clem.org', '/')
	"""

	mo = re.search(r"//([^/]+)(/.*)?", url)
	host, path = mo.groups()
	if path is None:
		path = '/'
	return (host, path)

def get_page(url):
	"""Retourne le contenu d'une url"""

	req = urllib2.Request(url)
	req.add_header('User-agent', USER_AGENT)
	u = urllib2.urlopen(req)
	ret = u.read()
	u.close()
	return ret

def get_location(url):
	"""Renvoie la Location d'une requete HTTP"""

	host, path = get_host_n_path(url)
	conn = httplib.HTTPConnection(host)
	conn.request('HEAD', path)
	res = conn.getresponse()
	location = res.getheader('Location')
	conn.close()
	return location

if __name__ == '__main__':
	doctest.testmod()