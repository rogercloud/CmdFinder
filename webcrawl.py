import urllib
from bs4 import BeautifulSoup as BS
from item import Entry, Desc
import sqlite3

class Crawler(object):
    def __init__(self, url):
        page = urllib.urlopen(url).readlines()
        self._soup = BS(''.join(page))
        self.entrys = []

    def filter(self):
        #summary
        sums = [s.a.string for s in self._soup.find_all('div', 'summary')]
        #command
        cmds = [c.string for c in self._soup.find_all('div', 'command')]
        #description
        desc = [Desc(per) for per in self._soup.find_all('div', 'description')]
        #vote
        vote = [int(v.string) for v in self._soup.find_all('div', 'num-votes')]

        for i in xrange(len(sums)):
            self.entrys.append(Entry(sums[i], cmds[i], desc[i], vote[i]))
