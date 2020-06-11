import datetime
import Const
import Player_year
import Team
import Player_Stat

class Player():



    list_index = -1;  # index specifying location in list (maybe dont worry about it)
    years_played = 0

    def __init__(self,firstname: str, secondname: str,team : str):
        #print("NEWPLAYER")
        self.firstname = firstname
        self.secondname = secondname
        self.fullname = firstname + " " + secondname
        self.team = team
        self.ident = self.fullname + self.team

        self.games = None
        self.birthdate = None
        self.age = None
        self.position = []
        self.scPrice = None
        self.height = None
        self.weight = None
        self.predict_2019 = 0
        self.mypredict_2019 = None
        # Change Year_list to dict
        self.year_dict = {}
        self.year_list = []

        # Basic Prediciton
        self.scores = {
            '2019': [-99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99,
                     -99, -99, -99, -99, -99, -99, -99, -99, -99, -99]
        } # add dict within dict for years ect...
        self.std_game = None
        self.std_pred_seas = None
        self.std_inter_seas = None
        self.game_pdf = None
        self.year_ave_pdf = None # Confidence in the average score prediction

    def __str__(self):
        return "%s %s %s " %("player is", self.fullname, self.scPrice)

    # For Odering and Comparisons (check works later)
    def __eq__(self, other):
        return self.fullname == other.fullname

    def update_info(self, birthdate: str, draftpick: int, draft_year: int):
        self.birthdate = birthdate
        self.draftpick = draftpick
        self.draft_year = draft_year

    def print_self(self):
        print(self.fullname,self.games,self.birthdate,self.age,self.position,self.scPrice,self.height,self.weight)

    def update_info_current(self, games: int, birthdate: datetime.date, position: str, scprice: int,
                            height: int,
                            weight: int):
        #print(self.fullname,games,position,scprice)

        if birthdate is not None:
            birthdate = birthdate.split(",")
            if len(birthdate) == 3:

                self.birthdate = datetime.date(int(birthdate[0]), int(birthdate[1]), int(birthdate[2]))
                self.age = datetime.date.today() - self.birthdate
        if position is not None:
            self.position = position.split(",")

        if scprice is not None:
            self.scPrice = int(scprice)

        # Cotroll Player does not have these stats
        if games is not None:
            self.games = games
            self.height = height
            self.weight = weight

    def check_add_year(self,year):
        if str(year) not in self.year_dict:
            self.year_dict[str(year)] = Player_year.Player_year(year)
            self.year_list.append(self.year_dict[str(year)])

    def add_check_game(self,player_stat: Player_Stat,year):
        self.check_add_year(str(year))
        self.year_dict[str(year)].add_check_game(player_stat)

    def print_years(self):
        print(self.fullname)
        for year in self.year_dict:
            self.year_dict[year].print_player_year()

    # Returns string for footywire players site
    def footywire_playername(self)->str:
        wire_name = self.secondname + ', ' + self.firstname
        return wire_name

