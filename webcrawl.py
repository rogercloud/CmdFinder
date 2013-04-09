import urllib
import sqlite3
import re
from bs4 import BeautifulSoup as BS
from item import Entry, Desc

class Crawler(object):
    def __init__(self, url):
        page = urllib.urlopen(url).readlines()
        self._soup = BS(''.join(page))
        self.entrys = []
        self._filt()

    def _filt(self):
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

    def last_page(self):
        aa = self._soup.find_all('a')
        pattern = re.compile('^Last')
        for a in aa:
            if a.string and pattern.match(a.string):
                return a.get('href').split('/')[-1]


class Database(object):
    def __init__(self, db):
        self.db = db
        self.pri_id = 0

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        self._clean_db()
        return self

    def _clean_db(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';") 
        for table in self.c.fetchall():
            print 'delete table %s' % (table[0], )
            self.c.execute("drop table %s;" % (table[0],))
        self.c.execute("create table entry (id num, summ text, cmd text, desc text, vote num)")
        return

    def _append_id(self, t):
        self.pri_id += 1
        return (self.pri_id,) + t
        
    def add_entry(self, entry):
        print entry.to_tuple()
        self.c.execute("insert into entry values (?,?,?,?,?);",
                self._append_id(entry.to_tuple()))

    def add_n_entry(self, entry):
        self.c.executemany("insert into entry values (?,?,?,?,?);",
                map(self._append_id, [e.to_tuple() for e in entry]))

    def _close(self):
        self.conn.commit()
        self.conn.close()

    def __exit__(self, t, value, traceback):
        self._close()


def grab_and_database():
    url = 'http://www.commandlinefu.com/commands/browse/'
    step = 25
    last = int(Crawler(url).last_page())

    with Database('db') as db:
        for i in xrange(0,last,step):
            print 'grabing page %d' % (i/25,)
            c = Crawler(url + str(i))
            db.add_n_entry(c.entrys)

def test():
    url = 'http://www.commandlinefu.com/commands/browse/'
    with Database('db') as db:
        c = Crawler(url + str(11 * 25))
        db.add_n_entry(c.entrys)


def main():
    #test()
    grab_and_database()

if __name__ == '__main__':
    main()
