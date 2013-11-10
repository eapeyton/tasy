import json

class Team:
    def __init__(self, id, owner=None):
        self.id = id
        self.owner = owner

    def __repr__(self):
        return "<%d %s>" % (self.id, self.owner)

    def __str__(self):
        return self.__repr__

    def __eq__(self,other):
        if isinstance(other, Team):
            if (self.id == other.id and
               self.owner == other.owner):
               return True
        return False 
        
    def to_JSON(self):
        return json.dumps(self.__dict__, cls=TasyEncoder, indent=4)

class League:

    def __init__(self, id):
        self.id = id
        self.seasons = {}

    def add_season(self, year):
        self.seasons[year] = Season(year)
        self.seasons[year].league = self

class Season:
    def __init__(self, year):
        self.year = year
        self.teams = {}

    def add_team(self, team):
        if isinstance(team, Team):
            self.teams[team.id] = team
        else:
            self.teams[team] = Team(team)

    def add_teams(self, teams):
        for team in teams:
            self.add_team(team)

class Player:
    def __init__(self, id, name=None):
        self.id = id
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
