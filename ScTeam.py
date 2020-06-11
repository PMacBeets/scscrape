import Const
import Player
import xlrd


class ScTeam():
    def __init__(self, name: str):
        self.name = name
        self.year = None
        self.round = None
        self.scplayers_dict = {
            Const.positions[0]: {},     # Defender
            Const.positions[1]: {},     # Midfield
            Const.positions[2]: {},     # Ruck
            Const.positions[3]: {}      # Forward
        }
        self.watchlist_dict = {}

    def name_team(self, name: str):
        self.name = name

    def check_add_player(self, pos_in: str, fullname: str, team: str):
        name = fullname.split(" ", 1)

        # If there is space for the player
        if len(self.scplayers_dict[pos_in]) < Const.pos_num_dict[pos_in][1]:

            tmp_player = Player.Player(name[0],name[1], team)
            #print(tmp_player)
            self.scplayers_dict[pos_in][tmp_player.ident] = tmp_player

        else:
            print("TOO MANY PLAYERS")
            exit(1)

    def read_in_sc_team(self):
        # Reads in Supercoach Player names
        wb = xlrd.open_workbook(Const.FILENAME)
        print(wb.get_sheets())
        print(wb.sheets())
        Team = wb.sheet_by_name("Team")
        self.round = int(Team.cell_value(0, 9))
        j = 0
        pos_in = None
        for i in range(Team.nrows):
            if str(Team.cell_value(i, 0)) != "":
                pos_in = str(Team.cell_value(i, 0))
                j += 1
                i += 1
            else:
                self.check_add_player(pos_in, Team.cell_value(i, 1), Team.cell_value(i, 2))
        # Read In Watchlist
        i = 18
        while str(Team.cell_value(i, 8)) != "":

            fullname = str(Team.cell_value(i, 8))
            #print(i,Team.cell_value(i, 8))
            name = fullname.split(" ", 1)
            team = str(Team.cell_value(i, 10))
            ident = fullname + team
            self.watchlist_dict[ident] = Player.Player(name[0],name[1], team)
            i += 1

    def read_in_2019(self)->list:
        # returns list of players that need info
        # Reads in Supercoach Player names
        wb = xlrd.open_workbook(Const.FILENAME)
        Team = wb.sheet_by_name("PlayerYear")
        games_read = 0
        player_list = []
        print("round:",self.round)
        for i in range(Team.nrows):
            # Skip first row
            if i == 0:
                continue

            games_read = 0
            for j in range(23):
                # check if game info has been recorded
                if str(Team.cell_value(i, 3 + j)) != "":
                    print("game read, score is:",Team.cell_value(i, 3 + j) )
                    games_read += 1

            if games_read < self.round and (Team.cell_value(i, 0)) != 0 and i<40:
                print(str(Team.cell_value(i, 0)),str(Team.cell_value(i, 1)))
                player_ident_tmp = str(Team.cell_value(i, 0)) + str(Team.cell_value(i, 1))
                print("ident",player_ident_tmp)
                player_list.append(player_ident_tmp)
            #print(player_list)
        return player_list





    def footy_wire_update(self,update_list: list)->list:
        # returns list of all players
        wire_name = []
        for position in Const.positions:
            #print(self.scplayers_dict[position])
            for player in self.scplayers_dict[position]:
                if self.scplayers_dict[position][player].ident in update_list:
                    wire_name.append(self.scplayers_dict[position][player].footywire_playername())
        for player in self.watchlist_dict:
            if self.watchlist_dict[player].ident in update_list:
                wire_name.append(self.watchlist_dict[player].footywire_playername())
        return wire_name


    def read_player_year(self)->list:
        wb = xlrd.open_workbook(Const.FILENAME)
        player_year = wb.sheet_by_name("Player_Year")
        j = 0
        for i in range(player_year.nrows):
            if i == 0:
                continue
            player_name = str(player_year.cell_value(i, 0))
            if player_name == "":
                break

            player_team = player_year.cell_value(i, 1)
            player_pos = player_year.cell_value(i, 1)
            player_ident = player_name + player_team

            if player_name != 0:
                # Search For Player in team
                player = self.scplayers_dict[player_team].get(player_ident)

                if player is not None:
                    game_tmp = []
                    for j in range(Const.NUMROUNDS):
                        game_tmp.append(player_year.cell_value(i, 1 + j))

                    print(player.fullname, game_tmp)
                    k = 0
                    # Add scores to score_list
                    for score in game_tmp:
                        if score != player.score['2019'][k]:
                            if player.score['2019'][k] != -99:
                                print("ERROR")
                                exit(1)

                            player.score['2019'][k] = score
                            k += 1
                else:
                    player = self.watchlist_dict.get(player_ident)
                    game_tmp = []
                    for j in range(Const.NUMROUNDS):
                        game_tmp.append(player_year.cell_value(i, 1 + j))

                    print(player.fullname, game_tmp)
                    k = 0
                    # Add scores to score_list
                    for score in game_tmp:
                        if score != player.score['2019'][k]:
                            if player.score['2019'][k] != -99:
                                print("ERROR")
                                exit(1)

                            player.score['2019'][k] = score
                            k += 1

    def print_player_year(self):
        for pos in self.scplayers_dict:
            for player in self.scplayers_dict[pos]:
                tmp_player = self.scplayers_dict[pos][player]
                print(tmp_player.fullname,tmp_player.scores)

