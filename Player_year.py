
class Player_year():

    GAMES = 22

    def __init__(self, year: int, aveSC: int, perc_games: int):
        self.year = year
        self.sc_ave = int(aveSC)
        self.perc_played = float(perc_games)
        self.af_av = None
        self.game_list = []
        self.age_ave = None
        self.team_that_year = None





        """"#Change to a Year object that can be created
           def create_year(self, game_list: Game, ave_age: int, team: str, af_av: int, sc_av: int):
               """