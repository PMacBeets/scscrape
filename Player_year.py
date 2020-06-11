import Player_Stat

class Player_year():

    GAMES = 22

    def __init__(self, year: str):
        self.year = str(year)
        self.sc_mean = None
        self.perc_played = None
        self.af_av = None
        self.game_dict = {}
        self.game_list = []
        self.std_dev = None
        self.age_ave = None
        self.team_that_year = None

    def update_sc(self, aveSC: int, perc_games: int):
        self.sc_ave = int(aveSC)
        self.perc_played = float(perc_games)

    def add_check_game(self, player_stat: Player_Stat):
        if self.game_dict.get(player_stat.match.ident) is None:
            self.game_dict[player_stat.match.ident] = player_stat
            self.game_list.append(self.game_dict[player_stat.match.ident])


    def print_player_year(self):
        for stat in self.game_list:
            print("        ",stat.sc)

    #def find_stnd_dev(self):
        #for game in self.game_list:


