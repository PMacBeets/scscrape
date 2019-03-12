import Const

class Team():
        def __init__(self,name: str):
            self.name = name
            self.players = []
            self.top_pos = {
                "Midfield": [],
                "Ruck": [],
                "Forward": [],
                "Defender": []
            }
            self.top_22_av = []

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

