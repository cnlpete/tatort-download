#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

def dump(pageURL):

	from httpclient import Robot
	from htmlparser import between

	from subprocess import Popen
	from shlex import split
	from os.path import exists
	from os import remove

	r = Robot()
	r.GET(pageURL)

	URLs = []

	q = 0
	key = 'mediaCollection.addMediaStream('
	while r.Page.find(key, q) > 0:
		p = r.Page.find(key, q)
		q = r.Page.find(');', p)
		excerpt = str(r.Page)[p:q]
		URLs.append( {	'resource': between(excerpt, ', "', '", '),
				'playpath': between(excerpt, ', "', '", ', 2)
				 } )
	#print URLs

	flashVer = 'LNX 11,1,102,55'
	swfUrl = 'http://www.ardmediathek.de/ard/static/player/plugins/flash/PluginFlash.swf/[[DYNAMIC]]/9'

	outfile = between(pageURL, '/tatort/', '-fsk')+'.f4v'
	if outfile == '':
		outfile = 'streamdump.f4v'
	if exists(outfile):
		remove(outfile)

	if len(URLs) > 0:
		fetch = URLs[len(URLs)-1]
		cmd = 'rtmpdump -V -r "'+fetch['resource']+'" -W "'+swfUrl+'" -f "'+flashVer+'" -p "'+pageURL+'" -y "'+fetch['playpath']+'" -o '+outfile
		Popen(split(cmd)).wait()
	else:
		print 'error: no URLs found'


