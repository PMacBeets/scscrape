import datetime
import Player_Stat
import Const

class Player():



    list_index = -1;  # index specifying location in list (maybe dont worry about it)
    years_played = 0

    def __init__(self,firstname, secondname):
        self.firstname = firstname
        self.secondname = secondname
        self.fullname = firstname + " " + secondname
        self.fullname2 = []
        self.games = None
        self.birthdate = None
        self.age = None
        self.position = []
        self.scPrice = None
        self.height = None
        self.weight = None
        self.predict_2019 = 0
        # Change Year_list to dict
        self.year_dict = {}
        self.team = None

    def __str__(self):
        return "%s %s " %(self.fullname, self.scPrice)

    # For Odering and Comparisons (check works later)
    def __eq__(self, other):
        return self.fullname == other.fullname

    def update_Birthdate(self, birthdate):
        self.birthdate = birthdate

    def update_info(self, birthdate: str, draftpick: int, draft_year: int):
        self.birthdate = birthdate
        self.draftpick = draftpick
        self.draft_year = draft_year


    def print_self(self):
        print(self.fullname,self.games,self.birthdate,self.age,self.position,self.scPrice,self.height,self.weight)

    # For Data_clean
    """def update_info_current(self, games: int, birthdate: datetime.date, position: str, scprice: int,
                            height: int,
                            weight: int):
        self.games = games
        self.birthdate = birthdate
        self.position = position
        self.scPrice = scprice
        self.height = height
        self.weight = weight"""

    def update_info_current(self, games: int, birthdate: datetime.date, position: str, scprice: int,
                            height: int,
                            weight: int):
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

    def predict_year(self):

        divisor = 0;
        for year in Const.years:
            year_tmp = self.year_dict.get(str(year))
            if year_tmp is not None:
                self.predict_2019 += Const.year_to_w[str(year)] * year_tmp.sc_ave * year_tmp.perc_played
                divisor += Const.year_to_w[str(year)] * year_tmp.perc_played
                # print("2018",year_tmp.sc_ave, year_tmp.perc_played,divisor)


        if divisor == 0:
            self.predict_2019 = 0
        else:
            self.predict_2019 /= divisor



