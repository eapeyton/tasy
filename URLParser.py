import re
import pickle
import json
import Util
from bs4 import BeautifulSoup

class URLParser:
    def match_url(self, url):
        url_regex = re.search("games\.espn\.go\.com/ffl/(?:clubhouse|leagueoffice)?\?leagueId=(\d+)(?:&teamId=(\d+))?(?:&seasonId=(\d+))?",url)
        league_id,team_id,season_year = url_regex.group(1,2,3)
        if league_id is not None:
            league_id = int(league_id)
        if team_id is not None:
            team_id = int(team_id)
        if season_year is not None:
            season_year = int(season_year)
        return league_id,team_id,season_year

    def parse(self, url):
        league_id,team_id,season_year = self.match_url(url)
        if league_id is not None:
            self.league = League(league_id)

            if season_year is not None:
                self.league.add_season(season_year)
                self.season = self.league.seasons[season_year]
    
                if team_id is not None:
                    self.season.add_team(team_id)
                    self.team = self.season.teams[team_id]
                    html = Util.download(url).decode('utf-8')
                    self.team.players = self.parse_team_players(html)

    def parse_team_players(self, html):
        page = BeautifulSoup(html)
        player_tags = page.find_all('a',playerid=re.compile("\d+"),text=True)
        players = set()
        for player in player_tags:
            players.add(Player(player['playerid'],player.string))
        return players
        
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
        self.seasons[year] = Season(year)

class Season:
    def __init__(self, year):
        self.year = int(year)
        self.teams = {}

    def add_team(self, team_id):
        self.teams[team_id] = Team(team_id)

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
    
