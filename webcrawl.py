import urllib
from bs4 import BeautifulSoup as BS
from item import Item

class Crawler():
    def __init__(self, url):
        page = urllib.urlopen(url).readlines()
        self.soup = BS(''.join(page))

    def filter(self):
        #summary
        sums = [s.a.string for s in self.soup.find_all('div', 'summary')]
        #command
        cmds = [c.string for c in self.soup.find_all('div', 'command')]
        #description
        desc = self.soup.find_all('div', 'description')
        desc_str = []
        for perdes in desc:
            perdes_str = []
            for para in [p for p in perdes.contents if not isinstance(p,unicode)]:
                pstr = ''
                if para.name == 'p' or para.name == 'code':
                    for content in para.contents:
                        if isinstance(content, unicode):
                            pstr += content
                        else:
                            pstr += content.string
                    perdes_str.append(pstr)
            desc_str.append(perdes_str)
        print desc_str
        #vote
        vote = self.soup.find_all('div', 'num-votes')
        vote = [int(v.string) for v in vote]

        for i in xrange(len(sums)):
            it = Item(sums[i], cmds[i], desc_str[i], vote[i])
            print it
