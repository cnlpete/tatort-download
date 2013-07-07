#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from subprocess import Popen
from shlex import split

def rtmpdump(fetch, pageURL, outfile):
	flashVer = 'LNX 11,1,102,55'
	swfUrl = 'http://www.ardmediathek.de/ard/static/player/plugins/flash/PluginFlash.swf/[[DYNAMIC]]/9'
	cmd = 'rtmpdump -V -r "'+fetch['resource']+'" -W "'+swfUrl+'" -f "'+flashVer+'" -p "'+pageURL+'" -y "'+fetch['playpath']+'" -o '+outfile
	print cmd
	Popen(split(cmd)).wait()

def wget(fetch, outfile):
	cmd = 'wget --user-agent="" "'+fetch['playpath']+'" -O "'+outfile+'"'
	print cmd
	Popen(split(cmd)).wait()

def dump(pageURL):
	from httpclient import Robot
	from htmlparser import between
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
		URLs.append( {'resource': between(excerpt, ', "', '", '), 'playpath': between(excerpt, ', "', '", ', 2)} )
	#print URLs

	outfile = between(pageURL, '/tatort/', '-fsk')+'.f4v'
	if outfile == '':
		outfile = 'streamdump.f4v'
	if exists(outfile):
		remove(outfile)

	if len(URLs) > 0:
		selected = URLs[len(URLs)-1]
		if selected['playpath'][:7] == 'http://':
			wget( selected, outfile )
		elif selected['playpath'][:4] == 'mp4:':
			rtmpdump( selected, pageURL, outfile )
		else:
			print 'Unsupported resource type: '+str(selected)
	else:
		print 'error: no URLs found'

