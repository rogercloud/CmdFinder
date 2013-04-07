class Item(object):
    def __init__(self,summary,cmd,desc,vote):
        self.summary = summary
        self.cmd = cmd 
        self.desc = desc 
        self.vote = vote
        
    def __str__(self):
        d = '\n'.join(self.desc)
        return 'smmary: %s\ncmd: %s\ndesc: %s\nvote:%d\n' % (\
                self.summary, self.cmd, d, self.vote)
