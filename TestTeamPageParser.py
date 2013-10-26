import unittest
import Util
from TeamPageParser import TeamPageParser
from TeamPageParser import Player


class TestTeamPageParser(unittest.TestCase):

    def setUp(self):
        self.parser = TeamPageParser()
        
    def testDownload(self):
        webpage = Util.download("http://eapeyton.com").decode('utf-8')
        self.assertEqual(webpage[:95], """<!--\nTo change this template, choose Tools | Templates\nand open the template in the editor.\n-->""")

    def testRegexTeam(self):
        team = self.parser.parse_team("http://games.espn.go.com/ffl/clubhouse?leagueId=1015919&teamId=1&seasonId=2013")
        self.assertEqual(team.league.id, 1015919)
        self.assertEqual(team.id, 1)
        self.assertIn(2013, team.league.seasons)

    def testRegexSeason(self):
        season = self.parser.parse_season("http://games.espn.go.com/ffl/leagueoffice?leagueId=1015919&seasonId=2012")
        self.assertEqual(season.league.id, 1015919)
        self.assertEqual(season.year, 2012)

    def testParsePlayers(self):
        team = self.parser.parse_team("http://games.espn.go.com/ffl/clubhouse?leagueId=1015919&teamId=1&seasonId=2012")
        self.assertEqual(team.league.id, 1015919)
        self.assertEqual(team.id, 1)
        self.assertIn(2012, team.league.seasons)
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

    @unittest.skip("Impossible right now because dicts are serialized in no particular order...")
    def testParseToJSON(self):
        self.maxDiff = None
        team = self.parser.parse_team("http://games.espn.go.com/ffl/clubhouse?leagueId=1015919&teamId=1&seasonId=2012")
        key = open('TeamJSONKey.json','r')
        self.assertEqual(team.to_JSON(), key.read())
        key.close()

    def assertHasPlayer(self,team,id,name):
        player = Player(id,name)
        self.assertIn(player, team.players)
        
if __name__ == '__main__':
    unittest.main()
