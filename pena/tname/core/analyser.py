import Levenshtein, re
from difflib import SequenceMatcher
from bs4 import BeautifulSoup

class Analyser:
    def __init__(self, unexpected_added, unexpected_removed):
        self.sequencer = SequenceMatcher(isjunk=None, a='', b='', autojunk=True)
        self.unexpected_added = unexpected_added
        self.unexpected_removed = unexpected_removed
        self.typeof_removal = None
    
    def run(self):
        """ run and remove spurious """
        if not self.is_valid():
            return (self.unexpected_added, self.unexpected_removed)            

        self.handle_closing_tag()
        self.handle_union()

        return (self.unexpected_added, self.unexpected_removed, self.typeof_removal)
    
    def handle_closing_tag(self):
        added, removed = list(self.unexpected_added), list(self.unexpected_removed)
        
        # check in distinct lists
        for line_removed in removed:
            for line_added in added:
                if self.is_closing_tag(line_removed, line_added):
                    self.unexpected_added.remove(line_added)
                    self.unexpected_removed.remove(line_removed)

        if not self.is_valid():
            self.typeof_removal = "optional_closing"
            return

        added, removed = list(self.unexpected_added), list(self.unexpected_removed)
        
        # check inside the same list
        for _list in [added, removed]:
            aux = []
            for line in _list:
                index = _list.index(line)

                if (index+1) > len(_list):
                    break
                
                for nxt_line in _list[index+1::]:
                    if self.is_closing_tag(line, nxt_line):
                        if line not in aux:
                            aux.append(line)
                        if nxt_line not in aux:
                            aux.append(nxt_line)
            [_list.remove(line) for line in aux if line in _list]
        
        if not added and not removed:
            self.typeof_removal = "optional_closing"

        self.unexpected_added = added
        self.unexpected_removed = removed

    def is_valid(self):
        if (not self.unexpected_added) and (not self.unexpected_removed):
            return False
        return True
    
    def is_closing_tag(self, s1, s2):
        '''
        Description:
            Check if the difference between two strings is only a char (levenshtein distance == 1).
            Example backslash inserted optionally on tags: <meta> and <link>
        Params:
            s1: string one
            s2: string two
        Return:
            True if levenshtein distance == 1
        '''
        s1, s2 = self._parser(s1), self._parser(s2)
        distance = Levenshtein.distance(s1, s2)
        return (not distance)
       
    def _parser(self, string, chars=['-<', '+<', '<', '/>', '>']):
        new_string = string.strip()
        for c in chars:
            new_string = new_string.replace(c, '')
        return new_string

    def parser(self):
        tag = BeautifulSoup()

    def is_union(self, unexpected_added):
        for line in unexpected_added:
            if self.is_js_list(line) or self.is_html_class(line):
                return True
        return False

    def handle_union(self):
        if not len(self.unexpected_removed) or not self.is_union(self.unexpected_added):
            return
                
        _added = list(self.unexpected_added)
        _removed = list(self.unexpected_removed)

        _type, html_list, js_list = None, None, None

        for line in self.unexpected_added:
            # check if the line added is a js/html list
            if self.is_js_list(line):
                items = self.get_js_list_items(line)
                _type = 'js'
            elif self.is_html_class(line):
                items = self.get_html_class_items(line)
                _type = 'html'
            else:
                continue

            if items:
                items = items.split(',') if _type == 'js' else items.split(' ')
            else:
                continue

            items = [item.strip() for item in items]
            items.sort()
            
            for line_removed in self.unexpected_removed:
                # check if the line removed is a js/html list
                if _type == 'js':
                    if not self.get_js_list_items(line_removed):
                        continue
                    js_list = self.get_js_list_items(line_removed).split(',')
                    js_list.sort()
                    aux = [obj for obj in js_list if obj.strip() not in items]
                else:
                    if not self.get_html_class_items(line_removed):
                        continue
                    html_list = self.get_html_class_items(line_removed).split(' ')
                    html_list.sort()
                    aux = [obj for obj in html_list if obj.strip() not in items]
                
                # some lines have the same class but attributes distincts
                # for this case, the conflict is not handle
                if html_list == items:
                    attrs_line_added = line.split()
                    attrs_line_removed = line_removed.split()
                    if [attr for attr in attrs_line_added if attr not in attrs_line_removed]:
                        continue

                if not aux:
                    if line_removed in _removed:
                        _removed.remove(line_removed)
                    
                    if line in _added:
                        _added.remove(line)
        
        if (not _added) and (not _removed):
            self.typeof_removal = "union_tags"

        self.unexpected_added = _added
        self.unexpected_removed = _removed

    def get_html_class_items(self, string):
        pattern = '<\s*\w*\s*class\s*=\s*"?\s*([\w\s%#\/\.;:_-]*)\s*"?.*?>'
        regex = re.compile(pattern)
        match = regex.search(string)

        if match:
            return match.group(1)
        
        return None

    def get_js_list_items(self, string):
        pattern = '\[(.+)\]'
        regex = re.compile(pattern)
        match = regex.search(string)

        if match:
            return match.group(1)
        
        return None

    def is_js_list(self, string):
        '''
        Description:
            Check if the string is a javascript variable inserted on html page 
            Example: var wp_load_script = [...];
        Params:
            string: unexpected code found by PENA
        Return:
            True if is a javascript variable
        '''
        pattern = '(.+)\=.+\[.+\]\;$'
        regex = re.compile(pattern, re.IGNORECASE)
        return regex.search(string.strip()) is not None

    def is_html_class(self, string):
        '''
        Description:
            Check if the string is a html tag with class attribute
            Example: <body class="home blog styles hfeed responsive-menu-slide-left"> 
        Params:
            string: unexpected code found by PENA
        Return:
            True if is a javascript variable
        '''
        pattern = '<\s*\w*\s*class.*?>'
        regex = re.compile(pattern, re.IGNORECASE)
        return regex.search(string.strip()) is not None
