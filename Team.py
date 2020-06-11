import Const
import Player

class Team():
        def __init__(self,name: str):

            # Add team avergaes
            self.name = name
            self.players = []
            self.top_pos = {
                "Midfield": [],
                "Ruck": [],
                "Forward": [],
                "Defender": []
            }
            self.top_22_av = []

            self.tot_av_pos = {
                "top22": [0,0],
                "Midfield": [0,0],
                "Ruck": [0,0],
                "Forward": [0,0],
                "Defender": [0,0]
            }

        def __eq__(self, other):
            return self.name == other.name

        def __str__(self):
            return "%s" % (self.name)

        def print_top_team(self):
            print(self.name)
            for player in self.top_22_av:
                print(player, player.predict_2019)

            for pos in Const.positions:
                print(pos)
                for player in self.top_pos[pos]:
                    print(player, player.predict_2019)

        def add_player(self,player, Player):
            self.players.append(player)

        def get_team_info(self):
            self.players.sort(key=lambda x: x.predict_2019, reverse=True)
            self.top_22_av = self.players.copy()
            self.top_22_av = self.top_22_av[0:22]

            for player in self.top_22_av:
                #print(player.fullname)
                # loop through positions
                for pos in Const.positions:
                    #print(pos)
                    # if position is shared by a player in top 22 add to top_pos list under list
                    if pos in player.position:
                        #print(player.position, pos)
                        self.top_pos[pos].append(player)

            self.eval_team_info()

        def eval_team_info(self):

            # each player in top 22
            for player in self.top_22_av:
                self.tot_av_pos["top22"][0] += player.predict_2019
                self.tot_av_pos["top22"][1] += 1

                # match each position from player to dict
                for pos in player.position:
                    self.tot_av_pos[pos][0] += player.predict_2019
                    self.tot_av_pos[pos][1] += 1


        def print_22(self):
            for player in self.top_22_av:
                print(player.fullname,player.position,player.predict_2019)

        def print_team_splits(self):
            for key in self.tot_av_pos:
                print(self.tot_av_pos[key],key)
