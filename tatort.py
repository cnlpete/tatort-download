#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from httpclient import Robot
from htmlparser import between
from mediathek import dump

from sys import argv

r = Robot()
r.GET('http://www.ardmediathek.de/sendung/tatort?documentId=602916')

r.GET('/ard/servlet/ajax-cache/3516962/view=list/documentId=602916/index.html')
page = str(r.Page)

def fetch(nr, dummy=False):
	section = between(page, '<h3 class="mt-title">', '</h3>', nr).strip()
	tatortURL = between(section, 'href="', '"')
	if not 'http://' in tatortURL:
		tatortURL = 'http://www.ardmediathek.de'+tatortURL

	if 'tgl-ab-20-uhr' in tatortURL:
		print '\n'+str(i)+': '+tatortURL+'\n'
		if not dummy:
			#print 'tatort URL: '+tatortURL
			dump(tatortURL)
		return True
	else:
		return False

if len(argv) > 1:
	i = int(argv[1])+1
	while not fetch(i):
		i += 1
else:
	for i in range(page.count('<h3 class="mt-title">')):
		fetch(i+1, dummy=True)


