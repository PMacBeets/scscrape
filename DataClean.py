
import datetime
import Player
import csv
import re
import Player_Stat

FILENAME = 'scscrape/spiders/supercoach_players.csv'
YEAR_ARRAY = 7

#index of the relative
AF_IN = 0
SC_IN = 1
DATE_IN = 2
INFO_IN = 3
OPP_IN = 4
RES_IN = 5
ROUND_IN = 6

#index player profile
INF1_IN = 0
INF2_IN = 1
INFD_IN = 2
NAME_IN = 4
SCP_IN = 5

month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

monthdict = {
        'January': "1",
        'February': '2',
        'March': '3',
        'April': '4',
        'May': '5',
        'June': '6',
        'July': '7',
        'August': '8',
        'September': '9',
        'October': '10',
        'November': '11',
        'December': '12'
    }


# ----------------- Functions ------------------- #

def process_player_info(player_info)-> dict:

    tmp_data = player_info[INF1_IN]

    height = None
    weight = None
    games = None
    birthdate = None
    age = None
    position = None

    if "Games" in tmp_data:
        # Get Games
        index1 = tmp_data.index("Games:")
        index2 = tmp_data.index("Born:")
        games = re.findall('\d+', tmp_data[index1:index2])
        games = games[0]

        # Get Birthdate
        index1 = tmp_data.index("Born:") + 6
        index2 = tmp_data.index(",") + 6
        birthdate = tmp_data[index1:index2]
        birthdate = birthdate.replace(",","")
        month = re.findall('\w+', birthdate)
        birthdate = birthdate.replace(month[0], monthdict[month[0]])
        birthdate = birthdate.replace(" ", ",")


        #index2 = birthdate[1].index(",")
        #birthdate[1] = birthdate[1][:index2]
        #birthdate = datetime.date(int(birthdate[2]), int(birthdate[0]), int(birthdate[1]))
        #age = datetime.date.today() - birthdate



    tmp_data = player_info[INF2_IN]
    if "Height:" in tmp_data:
        index1 = tmp_data.index("Height:")
        index2 = tmp_data.index("Weight:")
        index3 = tmp_data.index("Position:") + 20
        height = re.findall('\d+', tmp_data[index1:index2])
        height = height[0]
        weight = re.findall('\d+', tmp_data[index2:index3])
        weight = weight[0]



    if "Position" in tmp_data:
        index3 = tmp_data.index("Position:") + 20
        position = re.findall('\w+', tmp_data[index3:])
        position = str(position)
        position = position.replace(" ", "")
        position = position[1:-1]
        position = position.replace("'","")



    #tmp_data = player_info[INFD_IN]
    #index1 = tmp_data.index(",")
    #draft_pick = re.findall('\d+', tmp_data[index1:])

    tmp_data = player_info[NAME_IN]
    fullname = tmp_data.split(' ', 1)

    tmp_data = player_info[SCP_IN]
    index1 = tmp_data.index("$")
    sc_price = re.findall('\d+', tmp_data[index1:])
    sc_price = int(str(sc_price[0])+ str(sc_price[1]))

    thisdict = {
        "games": games,
        "birthdate": birthdate,
        "height": height,
        "weight": weight,
        "position": position,
        "firstname":fullname[0],
        "secondname":fullname[1],
        "fullname": fullname[1] + ', ' + fullname[0],
        "sc_price": sc_price
        #"draft_pick": draft_pick[0] # which draft more info required
    }

    print(thisdict)


    return thisdict



def process_year(year_data, year_info: dict, player: Player):
    print("Process Year")
    af_array = year_data[AF_IN].split(',')
    sc_array = year_data[SC_IN].split(',')
    date_array = year_data[DATE_IN].split(',')
    opp_array = year_data[OPP_IN].split(',')
    result_array = year_data[RES_IN].split(',')
    round_array = year_data[ROUND_IN].split(',')

    game_list = []

    #filter data
    del date_array[0]
    del round_array[0]

    #clean up rounds
    length = len(round_array)
    for i in range(length):
         round_array[i] = round_array[i].replace(u'\xa0', u' ')

    #check all have same length ect...
    if len(af_array) != length:
        exit(1)

    if len(sc_array) != length:
        exit(1)

    if len(date_array) != length:
        exit(1)

    if len(opp_array) != length:
        exit(1)

    if len(result_array) != length:
        exit(1)

    #create list of games

    for i in range(length):
        round =round_array[i]
        date = date_array[i]
        opponent = opp_array[i]
        result = result_array[i]
        af = af_array[i]
        sc = sc_array[i]
        age = date - player.birthdate
        game = Player_Stat.Player_Stat(round, date, opponent, result, af, sc, age)
        game_list.append(game)

    # NEXT create year object then attach to player object in array
    games_played = length
    #age_ave = game_list[0].age + 60 #days
    

    return game_list


def process_info(info_list) -> dict:

    # Get second string with proper info
    str(info_list)
    info_list = info_list.split(',')

    # remove heading title & get name, year and team
    if len(info_list) <= 1:
        return
    else:

        thisdict = {
            "full_name": get_name(info_list[1]),
            "year": get_year(info_list[1]),
            "team": get_team(info_list[1])
        }

    return thisdict


def get_name(string) -> tuple:
    index1 = string.index("for")
    index2 = string.index("(")
    full_name = string[index1 + 4: index2 - 1]
    full_name = full_name.split(' ', 1)

    return (full_name[0], full_name[1])

def get_year(string) -> int:
    year = string[: 4]

    return int(year)

def get_team(string) -> str:
    index1 = string.index("(")
    index2 = string.index(")")

    team = string[index1 + 1:index2]

    return team

def search_for_player(list: Player, fullname: str) -> int:
    """

    :param fullname:
    :return: int specifying index in list or negative number if not there
    """
    i = 0;
    # Change to binary search once working, if too slow
    for player in list:
        if(player.fullname == fullname):
            return i

        i+=1;

    else:
        return -1;



# ----------------- Main ------------------------ #


print("Running")

player_list = []

with open(FILENAME) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        #print(len(row))
        # For Processing Year Info
        if len(row)>=YEAR_ARRAY:
            year_info = process_info(row[INFO_IN])
            if year_info is not None:
                firstname = year_info["full_name"][0]
                secondname = year_info["full_name"][1]
                full_name = firstname + " " + secondname;

                # search if in player list
                index = search_for_player(player_list, full_name)
                if index >= 0:
                    # add_year at this index
                    process_year(row,year_info)
                else:
                    # Player should have been created in player info
                    print("ERROR: Should not come across new player")
                    exit()

        # Player Info
        else:
            if (row[0]=='info1'):
                continue
            else:
                #process player info, create new player and update all info
                info = process_player_info(row)
                newplayer = Player.Player(info["firstname"], info["secondname"])
                newplayer.update_info_current(info["games"],info["birthdate"],info["position"],info["sc_price"],info["height"],info["weight"])
                player_list.append(newplayer)



    #print(player_list)
    player_list.sort(key=lambda x: x.fullname)
    #print("SORTED\n")
    #print(player_list)

    with open('2019_players_info.csv', mode='w') as employee_file:
        writer = csv.writer(employee_file, delimiter=',', quotechar='"')

        writer.writerow(["fullname","firstname","secondname","games","birthdate","position","scPrice","height","weight"])

        for player in player_list:
            position = str(player.position)
            position = position.replace(" ", "")
            position = position[1:-1]
            position = position.replace("'", "")
            birthdate = str(player.birthdate)
            birthdate = birthdate.replace("-",",")
            writer.writerow([player.fullname,player.firstname, player.secondname, player.games, birthdate, position, player.scPrice, player.height, player.weight])









