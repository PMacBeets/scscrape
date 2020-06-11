import Const
import Season
import Team
import Player
import datetime
import csv
from fuzzywuzzy import fuzz

class DataContainer():
    team_dict = {}
    season_dict = {}

    def create_season(self, season_ident):
        self.season_dict[season_ident] = Season.Season(season_ident)

    def add_team(self, name: str):
        self.team_dict[name] = Team.Team(name)

    def add_player(self,player: Player):
        player_tmp = self.team_dict[player.team]
        if player_tmp is None :
            print("ERROR")
            exit(1)
        else:
            # Add player to player list within team dict assume couldnt have been added before
            self.team_dict[player.team].add_player(player)

    def check_add_team_player(self,firstname: str, secondname: str, team_name: str)->Player:
        fullname = firstname + " " + secondname
        index1 = fullname.find("(")
        if index1 != -1:
            fullname = fullname[:index1 - 1]

        if team_name not in self.team_dict:
            self.add_team(team_name)

        for player in self.team_dict[team_name].players:
            """if fuzz.ratio(player.fullname, "Joshua Kennedy")> 50:
                print("HERE",player.fullname, fullname)"""

            if fuzz.ratio(player.fullname,fullname) > 90 and player.team == team_name:
                print(player.fullname, fullname, player.team, team_name)
                return player
        # if player not already there
        tmp_player = Player.Player(firstname,secondname)
        tmp_player.add_team(team_name)
        self.team_dict[team_name].players.append(tmp_player)
        #print("CREATE PLAYER")

        return tmp_player

    def print_players_year(self):
        print(self.team_dict)
        for team in self.team_dict:
            #print(self.team_dict[team].players)
            for player in self.team_dict[team].players:
                player.print_years()

    def print_players_info(self):
        print(self.team_dict)
        for team in self.team_dict:
            #print(self.team_dict[team].players)
            for player in self.team_dict[team].players:
                player.print_years()

    def calc_jlt_match_stats(self):
        for season in self.season_dict:
            for round in self.season_dict[season].rounds_dict:
                for match in self.season_dict[season].rounds_dict[round].matches_dict:
                    self.season_dict[season].rounds_dict[round].matches_dict[match].calc_top_pred_ave()

    def predict_player_years(self):
        for team in self.team_dict:
            #print(self.team_dict[team].players)
            for player in self.team_dict[team].players:
                player.predict_year()

    def analyse_team_info(self):
        for team in self.team_dict:
            self.team_dict[team].get_team_info()

    def print_team_info(self):
        for team in self.team_dict:
            self.team_dict[team].print_22()
            self.team_dict[team].print_team_splits()

    def update_player_info(self, playerin: Player, games: int, birthdate: datetime.date, position: str, scprice: int,
                            height: int,
                            weight: int):
        for team in self.team_dict:
            #print(self.team_dict[team].players)
            for player in self.team_dict[team].players:
                if player.fullname == playerin.fullname:
                    player.update_info_current(games,birthdate,position,scprice,height,weight)


    def print_player_for_draft(self):

        with open('Draft_Players.csv', mode='w') as employee_file:
            writer = csv.writer(employee_file, delimiter=',', quotechar='"')
            value = ["Name","Team","Position","Price","Prediction",]
            writer.writerow(value)


            for team in self.team_dict:

                # print(self.team_dict[team].players)
                for player in self.team_dict[team].players:
                    value = [str(player.fullname),str(player.team), str(player.position), str(player.scPrice), str(player.predict_2019)]
                    print(value)
                    writer.writerow(value)




