import urllib
from bs4 import BeautifulSoup as BS
from item import Entry, Desc
import sqlite3

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

class Database(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()
        self._clean_db()

    def _clean_db(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';") 
        for table in self.c.fetchall():
            print 'delete table %s' % (table[0], )
            self.c.execute("drop table %s;" % (table[0],))
        self.c.execute("create table entry (summ text, cmd text, desc text, vote num)")
        return
        
    def add_entry(self, entry):
        print entry.to_tuple()
        self.c.execute("insert into entry values (?, ?, ?, ?);",
                entry.to_tuple())

    def add_n_entry(self, entry):
        self.c.executemany("insert into entry values (?,?,?,?);",
                [e.to_tuple() for e in entry])

    def close(self):
        self.conn.commit()
        self.conn.close()



def main():
    """test"""
    # crawl
    c = Crawler('http://www.commandlinefu.com/commands/browse/')
    # write to database
    db = Database('db')
    db.add_n_entry(c.entrys)
    db.close()


if __name__ == '__main__':
    main()
