import re
from bs4 import BeautifulSoup
from FantasyObjects import *
import Util

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
            players.add(Player(int(player['playerid']),player.string))
        return players
        

    
