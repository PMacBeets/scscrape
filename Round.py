import Match


class Round():
    def __init__(self,identifier: str):
        self.ident = identifier
        self.matches_dict = {}

    def add_match(self, match: Match):
        if match.ident not in self.matches_dict:
            self.matches_dict[match.ident] = match

