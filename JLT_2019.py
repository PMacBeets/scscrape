import datetime
import Player
import Player_year
import csv
import Team
from fuzzywuzzy import fuzz
import xlrd
import Const
from Season import Season
import Match
import Round


FILENAME1 = "2019_players_info.csv"
FILENAME2 = "SC_PRE_2019.xlsm"


player_list = []
team_list = []
game_stat_list = []
read_in_dict = {}    # for 2019 players
read_in_dict2 = {}   # for jlt 2019

# ---------- File Headings --------------#
# For JLT 19
jlt_head = ["Player","Club","Rd","DT","SC","TOG","Opp","Date"]
season_ident = "JLT,2019"



#--------------- Functions --------------------#

#Searches by price CONTAINS ERROR
def binarySearch(name: str, price: int, player_list: list) -> int:
    first = 0
    last = len(player_list)-1
    found = False

    while first<=last and not found:
        midpoint = (first + last)//2
        if player_list[midpoint].scPrice == price:
            if player_list[midpoint].scPrice == price and fuzz.partial_ratio(player_list[midpoint].fullname, name) > 60:
                #print(name, player_list[midpoint].fullname, price)
                found = True
            else:
                #print(name, player_list[midpoint].fullname, price)
                exit(1)
        else:
            if price < player_list[midpoint].scPrice:
                last = midpoint-1
            else:
                first = midpoint+1

    return midpoint



def linear_search(name: str, price: int, player_list: list) -> int:
    i = 0;
    for player in player_list:
        #print("LINEARSEASRCH")
        #print("scPrice = {0} price = {1}".format(player.scPrice,price))
        if player.scPrice == price and fuzz.partial_ratio(player.fullname,name) > 60:
            #print(name, player.fullname, price)
            return i
        else:
            i+=1;
    return(-1)
    #print("DID NOT WORK FOR {0}".format(name))

def player_to_team(team_list: list, player: Player):
    i = 0;

    for team in team_list:
        if team.name == player.team:
            # Assumption player is not already in team is correct
            # add player to team list
            team_list[i].players.append(player)
            return
        else:
            i+=1;

    #create new team in team list
    newteam = Team.Team(player_list[j].team)
    team_list.append(newteam)
    team_list[i].players.append(player)
    #print("Newteam with first player",  player_list[j].team, player.fullname)
    return


            #print(player.fullname, "predicted to average", player.predict_2019)


def search_match_in_season(team_list: list,match):
    pass



# ----------------- Main ------------------------ #

# Change long term so player_game is read in, creates player if required, creates team if required
# same as how a match creates a round and a season
# update with footywire info
# read in all data using set headings

# Read in players & JLT scores

# -------- Read player info 2019 from footywire csv---------------#
with open(FILENAME1) as csv_file1:
    csv_reader1 = csv.reader(csv_file1, delimiter=',')
    i = 0;
    for row in csv_reader1:
        if i == 0:
            j = 0;
            for cell in row:
                for title in Const.titles:
                    if title == cell:
                        #print(cell,j)
                        read_in_dict[title] = j;
                j += 1;

            i+=1
            continue
        else:
            newplayer = Player.Player(row[read_in_dict["firstname"]],row[read_in_dict["secondname"]])
            player_list.append(newplayer)
            newplayer.update_info_current(row[read_in_dict["games"]],row[read_in_dict["birthdate"]],row[read_in_dict["position"]],row[read_in_dict["scPrice"]],row[read_in_dict["height"]],row[read_in_dict["weight"]])
            i+=1



    # ------- Read in Player 2019 info from excel file ----------- #

    # Clean up data reading

    # To open Workbook
    wb = xlrd.open_workbook(FILENAME2)
    SeasonData = wb.sheet_by_name("Players19")
    newyear = None;

    # For row 0 and column 0
    for i in range(SeasonData.nrows):
        if i == 0:
            i+=1
            continue

        name = SeasonData.cell_value(i, 2)
        index1 = name.find("(")
        if index1 != -1:
            name = name[:index1]

        # Get Price String
        price = SeasonData.cell_value(i, 9)
        #price = int(price)
        price = int(price)
        #print(price)

        # Could do binary but not worth the effort
        j = linear_search(name, price, player_list)
        player_list[j].team = SeasonData.cell_value(i, 4)

        player_to_team(team_list, player_list[j])

        for year in Const.year_to_col:
            season_tmp = SeasonData.cell_value(i, Const.year_to_col[year])
            if season_tmp != "":
                newyear = Player_year.Player_year(int(year), SeasonData.cell_value(i, Const.year_to_col[year]), SeasonData.cell_value(i, Const.year_to_col[year] + 5))
                player_list[j].year_dict[year] = newyear

    player_list.sort(key=lambda x: x.scPrice)
    team_list.sort(key=lambda x: x.name)

    for player in player_list:
        player.predict_year()

    # get team info
    for team in team_list:
        team.get_team_info()


    # Read JLT match

    SeasonData2 = wb.sheet_by_name("JLT 19")
    # create object season to be filled with JLT matches
    season_dict = {}
    #season_ident = str(season_ident[0]),str(season_ident[1])
    season_dict[season_ident] = Season(season_ident)

    # Loop through rows of data
    i = 0;
    for i in range(SeasonData2.nrows):
        if i == 0:
            for j in range(SeasonData2.ncols):

                for title in jlt_head:
                    if title == SeasonData2.cell_value(i,j):
                            #print(SeasonData2.cell_value(i,j),j)
                            read_in_dict2[title] = j;
                continue
        else:

            tmp_player = SeasonData2.cell_value(i,read_in_dict2["Player"])
            tmp_team = SeasonData2.cell_value(i,read_in_dict2["Club"])
            tmp_opp = SeasonData2.cell_value(i,read_in_dict2["Opp"])
            rd_tmp = SeasonData2.cell_value(i,read_in_dict2["Rd"])
            date_tmp = xlrd.xldate.xldate_as_datetime(SeasonData2.cell_value(i,read_in_dict2["Date"]), wb.datemode)
            #print(tmp_player, tmp_team, tmp_opp, date_tmp)

            # check if season exists (assume yes for JLT)
            # check if round exists in season, if not add
            cur_round = season_dict.get(season_ident).rounds_dict.get(rd_tmp)
            if cur_round is None:
                cur_round = Round.Round(rd_tmp)

            Match.JLT_Match(tmp_team, tmp_opp, tmp_player, cur_round, date_tmp,season_dict[season_ident])



    season_dict[season_ident].print_season()






    # match players through team lists (faster)
    # fill player_stat for each match and











