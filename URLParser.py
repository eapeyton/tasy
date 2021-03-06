import re
from bs4 import BeautifulSoup
from FantasyObjects import *
from urllib.parse import *
from Util import Downloader
from datetime import date
from collections import OrderedDict

class URLParser:

    def __init__(self):
        pass

    def match_url(self, url):
        url = urlparse(url)
        query = parse_qs(url.query)
        league_id = None
        team_id = None
        season_year = None
        if 'leagueId' in query:
            league_id = int(query['leagueId'][0])
        if 'teamId' in query:
            team_id = int(query['teamId'][0])
        if 'seasonId' in query:
            season_year = int(query['seasonId'][0])
        return league_id,team_id,season_year
    
    def composeURL(self, **args):
        scheme = 'http'
        location = 'games.espn.go.com'
        if('teamId' in args):
            path = '/ffl/clubhouse'
        else:
            path = '/ffl/leagueoffice'
        params = ''
        ordered_args = OrderedDict(sorted(args.items(), key=lambda t: t[0]))
        query = urlencode(ordered_args)
        fragment = ''
        url = urlunparse((scheme,location,path,params,query,fragment))
        return url

    def parse(self, url):
        league_id,team_id,season_year = self.match_url(url)
        if league_id is not None:
            self.league = League(league_id)

            if season_year is None:
                season_year = date.today().year
            self.league.add_season(season_year)
            self.season = self.league.seasons[season_year]

            if team_id is not None and "clubhouse" in url:
                league_URL = self.composeURL(leagueId=league_id,seasonId=season_year)
                self.season.add_teams(self.parse_teams(league_URL))
                with Downloader() as dler:
                    html = dler.download(url)
                self.team = self.season.teams[team_id]
                self.team.players = self.parse_team_players(html)
            if "leagueoffice" in url:
                self.season.add_teams(self.parse_teams(url))
                for team in self.season.teams.values():
                    team_URL = self.composeURL(leagueId=league_id,seasonId=season_year,teamId=team.id)
                    with Downloader() as dler:
                        html = dler.download(team_URL)
                    team.players = self.parse_team_players(html)

    def parse_teams(self, league_url):
        with Downloader() as dler:
            html = dler.download(league_url)
        page = BeautifulSoup(html)
        owner_tags = page.find_all('a',href=re.compile('teamId'),title=True)
        links = set()
        for owner_tag in owner_tags:
            links.add((owner_tag['href'],owner_tag['title']))
        teams = []
        for link in links:
            title = link[1]
            title_rg = re.search("(.*)\((.*)\)", title)
            team_name,owner = title_rg.group(1,2)
            parsedUrl = urlparse(link[0])
            query = parse_qs(parsedUrl.query)
            teamId = int(query['teamId'][0])
            teams.append(Team(teamId,owner=owner))
        return teams
        
    def parse_team_players(self, html):
        page = BeautifulSoup(html)
        player_tags = page.find_all('a',playerid=re.compile("\d+"),text=True)
        players = set()
        for player in player_tags:
            players.add(Player(int(player['playerid']),player.string))
        return players
        

    
