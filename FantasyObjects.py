import json

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
