import unittest
from Util import Downloader
from URLParser import URLParser
from FantasyObjects import *


class TestURLParser(unittest.TestCase):

    def setUp(self):
        self.parser = URLParser()
        
    def testDownload(self):
        my_url = "http://eapeyton.com"
        with Downloader() as dler:
            dler.uncache(my_url)
            webpage = dler.download(my_url)
            self.assertEqual(webpage[:15], """<!DOCTYPE html>""")

    def testDownloadCache(self):
        my_url = "http://eapeyton.com"
        with Downloader() as dler:
            dler.uncache(my_url)
            dler.cache[my_url] = "Be cool Honey Bunny!"
            webpage = dler.download("http://eapeyton.com")
            self.assertEqual(webpage, "Be cool Honey Bunny!")
        

    def testComposeLeagueURL(self):
        url = self.parser.composeURL(leagueId=1015919)
        self.assertEqual(url, "http://games.espn.go.com/ffl/leagueoffice?leagueId=1015919")
        url = self.parser.composeURL(leagueId=5555555)
        self.assertEqual(url, "http://games.espn.go.com/ffl/leagueoffice?leagueId=5555555")

    def testComposeTeamURL(self):
        url = self.parser.composeURL(teamId=4,leagueId=1015919)
        self.assertEqual(url,"http://games.espn.go.com/ffl/clubhouse?leagueId=1015919&teamId=4")
        url = self.parser.composeURL(leagueId=5555555, teamId=12)
        self.assertEqual(url,"http://games.espn.go.com/ffl/clubhouse?leagueId=5555555&teamId=12")

    def testRegexTeam(self):
        self.parser.parse("http://games.espn.go.com/ffl/clubhouse?leagueId=1015919&teamId=1&seasonId=2013")
        self.assertEqual(self.parser.league.id, 1015919)
        self.assertEqual(self.parser.team.id, 1)
        self.assertIn(2013, self.parser.league.seasons)

    def testRegexSeason(self):
        self.parser.parse("http://games.espn.go.com/ffl/leagueoffice?leagueId=1015919&seasonId=2012")
        self.assertEqual(self.parser.league.id, 1015919)
        self.assertEqual(self.parser.season.year, 2012)

    def testParseNoYear(self):
        self.parser.parse("http://games.espn.go.com/ffl/leagueoffice?leagueId=1020911")
        self.assertEqual(self.parser.league.id, 1020911)
        self.assertEqual(self.parser.season.year, 2013)

    def testParsePlayers(self):
        self.parser.parse("http://games.espn.go.com/ffl/clubhouse?leagueId=1015919&teamId=1&seasonId=2012")
        team = self.parser.team
        self.assertEqual(team.id, 1)
        self.assertHasSequoyahPlayers(team)

    def assertHasSequoyahPlayers(self, team):
        self.assertHasPlayer(team, 11237, "Matt Ryan")
        self.assertHasPlayer(team, 11289, "Ray Rice")
        self.assertHasPlayer(team, 14885, "Doug Martin")
        self.assertHasPlayer(team, 9705, "Brandon Marshall")
        self.assertHasPlayer(team, 10447, "Calvin Johnson")
        self.assertHasPlayer(team, 13232, "Jimmy Graham")
        self.assertHasPlayer(team, 2578, "Reggie Wayne")
        self.assertHasPlayer(team, 60015, "Dolphins D/ST")
        self.assertHasPlayer(team, 3504, "Shayne Graham")
        self.assertHasPlayer(team, 11238, "Darren McFadden")
        self.assertHasPlayer(team, 13204, "Ryan Matthews")
        self.assertHasPlayer(team, 60007, "Broncos D/ST")
        self.assertHasPlayer(team, 11439, "Pierre Garcon")
        self.assertHasPlayer(team, 9613, "DeAngelo Willioms")

    def assertHasPlayer(self,team,id,name):
        player = Player(id,name)
        self.assertIn(player, team.players)

    def testParseSeason(self):
        self.parser.parse("http://games.espn.go.com/ffl/leagueoffice?leagueId=408631&seasonId=2013")
        season = self.parser.season
        self.assertEqual(season.year, 2013)
        self.assertHasTeam(season, 1, "Nick Burke")
        self.assertHasTeam(season, 2, "Jeff Siegel")
        self.assertHasTeam(season, 3, "Nick Macie")
        self.assertHasTeam(season, 4, "D Duncanson")
        self.assertHasTeam(season, 5, "Chris Nachmias")
        self.assertHasTeam(season, 6, "Chris Thorne")
        self.assertHasTeam(season, 7, "ryan davis")
        self.assertHasTeam(season, 8, "Vishnu Iyengar")
        self.assertHasTeam(season, 9, "vishaak ravi")
        self.assertHasTeam(season, 10, "Eric Peyton")

    def testParseSeason2(self):
        self.parser.parse("http://games.espn.go.com/ffl/leagueoffice?leagueId=1015919&seasonId=2012")
        season = self.parser.season
        self.assertHasTeam(season, 1, "Eric Peyton")
        team = season.teams[1]
        self.assertHasSequoyahPlayers(team)

    def testParsePlayers2(self):
        self.parser.parse("http://games.espn.go.com/ffl/clubhouse?leagueId=1015919&teamId=1&seasonId=2012")
        season = self.parser.season
        self.assertEqual(season.year, 2012)
        self.assertEqual(season.league.id, 1015919)
        self.assertHasSequoyahPlayers(self.parser.team)
        self.assertHasTeam(season, 1, "Eric Peyton")
        self.assertHasTeam(season, 2, "Eddie Peyton")
        self.assertHasTeam(season, 3, "Mala Morjaria")
        self.assertHasTeam(season, 10, "Rikin Marfatia")

    def assertHasTeam(self,season,id,owner):
        team = Team(id, owner=owner)
        self.assertIn(team, season.teams.values())

    @unittest.skip("Impossible right now because dicts are serialized in no particular order...")
    def testParseToJSON(self):
        self.maxDiff = None
        team = self.parser.parse_team("http://games.espn.go.com/ffl/clubhouse?leagueId=1015919&teamId=1&seasonId=2012")
        key = open('TeamJSONKey.json','r')
        self.assertEqual(team.to_JSON(), key.read())
        key.close()

        
if __name__ == '__main__':
    unittest.main()
