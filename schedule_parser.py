from html.parser import HTMLParser
import re

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.match_pat = re.compile("matchup[0-9]*")
        self.match_index = 0
        
    def handle_starttag(self, tag, attrs):
        for attribute in attrs:
            if is_matchup(attribute):
                print(att + ":" + value)
        if self.active:
            for att,value in attrs:
                if att == "href" and "teamid" in value.lower():
                    print(att + ":" + value)
    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass
        
    def is_matchup(attribute):
        name = attribute[0]
        value = attribute[1]
        if name == "name" and self.match_pat.match(value):
            print(att + ":" + value)
        

parser = MyHTMLParser()

with open("espn-schedule.html","r") as schedule:
    parser.feed(schedule.read())

