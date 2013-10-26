import re
import pickle
import json
import Util
from bs4 import BeautifulSoup

class TeamPageParser:
    
    def parse_team(self, url):
        league_id,team_id,season_year = self.parse_url(url)
        team = Team(team_id)
        team.league = League(league_id)
        team.league.add_season(season_year)
        html = Util.download(url).decode('utf-8')
        page = BeautifulSoup(html)
        player_tags = page.find_all('a',playerid=re.compile("\d+"),text=True)
        team.players = set()
        for player in player_tags:
            team.players.add(Player(player['playerid'],player.string))
        return team

    def parse_season(self, url):
        league_id,team_id,season_year = self.parse_url(url)
        season = Season(season_year)
        return season

    def parse_url(self, url):
        url_regex = re.search("games\.espn\.go\.com/ffl/(?:clubhouse|leagueoffice)?\?leagueId=(\d+)(?:&teamId=(\d+))?(?:&seasonId=(\d+))?",url)
        league_id,team_id,season_year = url_regex.group(1,2,3)
        return league_id,team_id,season_year 


class Team:
    def __init__(self, id):
        self.id = int(id)

    def to_JSON(self):
        return json.dumps(self.__dict__, cls=TasyEncoder, indent=4)

class League:
    def __init__(self, id):
        self.id = int(id)
        self.seasons = {}

    def add_season(self, year):
        self.seasons[int(year)] = Season(year)

class Season:
    def __init__(self, year):
        self.year = int(year)

class Player:
    def __init__(self, id, name=None):
        self.id = int(id)
        self.name = name

    def __eq__(self,other):
        if isinstance(other, Player):
            if self.id == other.id:
                return True
        return False

    def __hash__(self):
        return self.id * 7

    def __repr__(self):
        return "<%d %s>" % (self.id,self.name)
       
class TasyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.to_JSON()
        except AttributeError:
            if isinstance(obj, set):
                return list(obj)
            return obj.__dict__
    
