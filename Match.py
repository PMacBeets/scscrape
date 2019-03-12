
import Team
import Season
import Round
from Player_Match_Stat import Player_Match_Stat

class Match():
    def __init__(self, team1: Team, team2: Team, stats: Player_Match_Stat, rd: Round, date, season: Season):
        self.teams = [team1, team2]
        self.teams.sort()
        self.date = date
        string = str(date.strftime("%m/%d/%Y"))
        string = string
        #print(string)
        self.ident = string + str(self.teams[0]) + str(self.teams[1])
        self.stats = stats
        self.round = rd
        self.season = season;

        # tmp == None if round does not exit
        tmp = season.rounds_dict.get(rd)
        if tmp is None:
            season.add_round(rd)

        #print(self)
        #print(season.rounds_dict[rd.ident])
        season.rounds_dict[rd.ident].add_match(self)


        self.result = None
        self.tags = None
        self.oval = None
        self.hometeam = None


    # For tags from fanfooty (far future)
    def add_tags(self, tags_list: list):
        self.tags = tags_list

    def add_result(self,result):
        self.result = result  # not str will depend on who is passing it through

    def add_oval(self,oval):
        self.oval = oval

    def add_oval(self,hometeam):
        self.hometeam = hometeam


class JLT_Match(Match):
    def __init__(self, team1: Team, team2: Team, stats: Player_Match_Stat, rd: str, date, season: Season):
        super(JLT_Match, self).__init__(team1, team2, stats, rd, date, season)

        # Not for players but for tuples (total, average)
        # Used to determine strength of th team
        # predicted average of players who played (indicitive strength)
        self.top_pos_ave = {
            "home":{
                "top22": None,
                "Midfield": [],
                "Ruck": [],
                "Forward": [],
                "Defender": []
            },
            "away": {
                "top22": None,
                "Midfield": [],
                "Ruck": [],
                "Forward": [],
                "Defender": []
            }
        }
        # scores in game (gameday strength)
        self.top_pos_scored = {
            "home": {
                "top22": None,
                "Midfield": [],
                "Ruck": [],
                "Forward": [],
                "Defender": []
            },
            "away": {
                "top22": None,
                "Midfield": [],
                "Ruck": [],
                "Forward": [],
                "Defender": []
            }
        }





