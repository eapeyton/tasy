from html.parser import HTMLParser
import xml.etree.ElementTree as ET
import argparse
import re
import logging

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.match_pat = re.compile("matchup\d*")
        self.team_pat = re.compile("/ffl/clubhouse\?leagueId=\d*&teamId=(\d*)&seasonId=\d*")
        self.week_index = 0
        self.weeks = []
        self.pair = None
        

    def get_week_index(self, attribute):
        result = re.search(r'\d+',attribute[1])
        return int(result.group())
    
    def handle_starttag(self, tag, attrs):
        for attribute in attrs:
            if self.is_matchup(attribute):
                self.active = True
                self.week_index = self.get_week_index(attribute)
                logging.debug("ON WEEK %d" % self.week_index)
            elif self.active and attribute[1] != None: 
                if(attribute[0] == "href"):
                    logging.debug("FOUND ATTRIBUTE ----%s----" % attribute[1].encode())
                    pass
                team_id = self.team_pat.match(attribute[1])
                if team_id != None:
                    logging.debug("MATCHED!")
                    team_id = team_id.group(1)
                    if self.pair:
                        self.add_to_week(Matchup(int(self.pair),int(team_id)))
                        self.pair = None
                    else:
                        self.pair = team_id
                
                    
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
    
    def is_team(self, attribute):
        if attribute[0] == "href" and "teamid" in attribute[1].lower():
            return True
        return False
    
    def add_to_week(self, matchup):
        while len(self.weeks) != self.week_index:
            self.weeks.append([])
        week = self.weeks[self.week_index-1]
        week.append(matchup)

    def test(self, key):
        tree = ET.parse(key)
        schedule = tree.getroot()
        for iweek in range(len(schedule)):
            week = schedule[iweek]
            for imatchup in range(len(week)):
                matchup = week[imatchup]
                away = int(matchup[0].text)
                home = int(matchup[1].text)
                awayt = self.weeks[iweek][imatchup].away
                homet = self.weeks[iweek][imatchup].home
                if away == awayt and home == homet:
                    logging.info("OK")     
                else:
                    logging.warn("WEEK %d MATCHUP %d MISMATCH!!!!" % (iweek,imatchup))

        

    def __str__(self):
        return "\n".join([str(week) for week in self.weeks])
        
class Matchup():
    def __init__(self, away, home):
        self.away = away
        self.home = home
        
    def __repr__(self):
        return self.__str__() 
    def __str__(self):
        return "(Away: %s, Home: %s)" % (self.away,self.home)
        
class Week():
    def __init__(self):
        self.matchups = []
        
    def add_matchup(self, matchup):
        self.matchups.append(matchup)
        
    def __str__(self):
        return str(self.matchups)
        
class Team():
    def __init__(self,id):
        self.id = id
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("html")
    arg_parser.add_argument("-t","--test",dest="test")
    args = arg_parser.parse_args() 
    parser = MyHTMLParser()
    with open(args.html,"r") as schedule:
        parser.feed(schedule.read())
    parser.test(args.test)

