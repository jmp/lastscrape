#!/usr/bin/env python
"""usage: lastscrape.py user"""
import sys, time
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup

def process_page(page):
	page = urlopen(page)
	soup = BeautifulSoup(page)
	for tr in soup.find('table', 'tracklist big').findAll('tr'):
		artist, track, timestamp = parse_track(tr)
		if artist and track:
			print '%s\t%s\t%s' % (artist, track, timestamp)

def parse_track(tr):
	try:
		artist, track = tr.findAll('a', 'primary')
		timestamp = tr.find('td', 'border dateCell last')
		artist = artist.contents[0].strip()
		track = track.contents[0].strip()
		timestamp = timestamp.contents[0].strip()
		return (artist, track, timestamp)
	except:
		# Parsing failed
		return (None, None, None)

def scrape_data(user, request_delay=1):
	num_pages = 1
	url = 'http://last.fm/user/%s/library/recent' % user
	page = urlopen('http://last.fm/user/%s/library/recent' % user)
	soup = BeautifulSoup(page)
	num_pages = int(soup.find('a', 'lastpage').contents[0]) + 1

	print 'Artist\tTrack\tTimestamp'
	for cur_page in range(1, num_pages):
		process_page(url + '?page=' + str(cur_page))
		if cur_page < num_pages:
			time.sleep(request_delay)

def main(*args):
	if len(args) > 1:
		scrape_data(args[1])
	else:
		print __doc__

if __name__ == '__main__':
	sys.exit(main(*sys.argv))
