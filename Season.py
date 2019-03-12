import Round

class Season():
    def __init__(self,identifier: str,):
        self.ident = identifier
        identifier = identifier.split(",")
        self.year = identifier[1]
        self.rounds_dict = {}

    def add_round(self, rd: Round):
        if rd.ident not in self.rounds_dict:
            self.rounds_dict[rd.ident] = rd

    def print_season(self):
        for round in self.rounds_dict:
            print(self.rounds_dict[round].ident)
            for match in self.rounds_dict[round].matches_dict:
                print("    ",match)


