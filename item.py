class Entry(object):
    ''' database entry '''
    def __init__(self,summ,cmd,desc,vote):
        self.summ= summ
        self.cmd = cmd 
        self.desc = desc 
        self.vote = vote
        
    def __str__(self):
        return 'smmary: %s\ncmd: %s\ndesc: %s\nvote:%d\n' % (\
                self.summ, self.cmd, self.desc, self.vote)

    def to_tuple(self):
        return self.summ ,self.cmd , unicode(self.desc), self.vote


class Desc(object):
    ''' Single description may contains multipul paragraphs '''
    def __init__(self, desc):
        self.desc = desc
        self.desc_list = self._filter()
        
    def _filter(self):
        perdes_str = []
        # contents may contains '\n', ignore it
        for para in [p for p in self.desc.contents if not isinstance(p,unicode)]:
            pstr = ''
            if para.name == 'p' or para.name == 'code':
                for content in para.contents:
                    if isinstance(content, unicode):
                        pstr += content.strip()
                    elif content.string is not None:
                        pstr += content.string.strip()
                perdes_str.append(pstr)
        return perdes_str

    def __str__(self):
        return '\n'.join(self.desc_list)
