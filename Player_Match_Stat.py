import Match

class Player_Match_Stat():

    def __init__(self, match: Match, af: int, sc: int, age: int):
        self.match = match
        self.af = af
        self.sc = sc
        self.age = age

    # For tags from fanfooty (far future)
    def add_tags(self, tags_list: list):
        self.tags = tags_list