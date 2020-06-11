import Player
import Match
import Player_year
import Season

class Player_Stat():
    def __init__(self, player: Player, match: Match, af: int, sc: int, tog: float):
        self.player = player


        # for future
        # remove team_list and player_list into one compact object
        # create tmp player
        # see if current team exists, if not create and add to list
        # within team see if current player exists, if not create and add to list
        self.match = match
        self.af = af
        self.sc = sc
        self.tog = tog
        self.age = None
        self.tags = None

        self.match.add_stats(self)
        self.player.add_check_game(self, match.season.ident)




    # For tags from fanfooty (far future)
    def add_tags(self, tags_list: list):
        self.tags = tags_list

    def add_age(self):
        self.age = self.match.date - self.player.birthdate

