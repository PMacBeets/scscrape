import datetime
import Round
import Player
import Match
import Season

class Player_Stat():
    def __init__(self, team: str, firstname: str, secondname: str, match: Match, af: int, sc: int, age: int, team_list: list, player_list: list):
        # for future
        # remove team_list and player_list into one compact object
        # create tmp player
        tmp_player = Player.Player(firstname,secondname)
        # see if current team exists, if not create and add to list
            if team

        # within team see if current player exists, if not create and add to list

        self.rd = rd
        self.match = match
        self.af = af
        self.sc = sc
        self.age = age

    # For tags from fanfooty (far future)
    def add_tags(self, tags_list: list):
        self.tags = tags_list
