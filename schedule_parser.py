from html.parser import HTMLParser
import re

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.match_pat = re.compile("matchup[0-9]*")
        self.match_index = 0
        

    def get_match_index(self, attribute):
        result = re.search(r'\d+',attribute[1])
        return int(result.group())
    
    def handle_starttag(self, tag, attrs):
        for attribute in attrs:
            if self.is_matchup(attribute):
                self.active = True
                self.match_index = self.get_match_index(attribute)
        if self.active:
            print(self.match_index)
            for att,value in attrs:
                if att == "href" and "teamid" in value.lower():
                    print(att + ":" + value)
    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass
        
    def is_matchup(self,attribute):
        name = attribute[0]
        value = attribute[1]
        if name == "name" and self.match_pat.match(value):
            return True
        return False
        

parser = MyHTMLParser()

with open("espn-schedule.html","r") as schedule:
    parser.feed(schedule.read())

