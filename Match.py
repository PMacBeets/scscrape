
import Team
import Season
import Round
import Player_Stat
import Const

class Match():
    # add regular season variable
    def __init__(self, team1: Team, team2: Team, rd: Round, date, season: Season):
        #if season.season_dict.get(season_ident).rounds_dict.get(cur_round.ident) is None:
        # hometeam is read in first
        self.hometeam = team1
        self.teams = [team1, team2]
        self.teams.sort()
        self.date = date
        string = str(date.strftime("%m/%d/%Y"))
        self.ident = string + str(self.teams[0]) + str(self.teams[1])
        self.stats = []
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


    # For tags from fanfooty (far future)
    def add_tags(self, tags_list: list):
        self.tags = tags_list

    def add_result(self,result):
        self.result = result  # not str will depend on who is passing it through

    def add_oval(self,oval):
        self.oval = oval

    def add_oval(self,hometeam):
        self.hometeam = hometeam

    def add_stats(self,stat: Player_Stat):
        #print("ADD STATS",self)

        self.stats.append(stat)
