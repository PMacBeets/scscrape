
import Const
import DataContainer
import ScTeam
import runspider


THISYEAR = 2019



# --------- Function ---------- #

def add_all_teams(data: DataContainer):
    for key in Const.positions:
        data.add_team(key)

# --------- Main ---------- #

my_scteam = ScTeam.ScTeam("OOORRazziooOOO")

my_scteam.read_in_sc_team()

update_players = my_scteam.read_in_2019()
my_scteam.print_player_year()
print(update_players)
# Only run footywire spider if update is need
# Only update the players that need updating
footywire_names = my_scteam.footy_wire_update(update_players)
# cut footywire names to shorten lookup time
print(footywire_names)
footywire_names = footywire_names[5:6]
print(footywire_names)

runspider.run_footywire_spider(footywire_names)
# update byes
# update averages




