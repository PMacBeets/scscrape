FILENAME = "SupercoachTeam.xls"

year_to_col = {
    "2018": 12,
    "2017": 13,
    "2016": 14,
    "2015": 15,
}
year_to_w = {
    "2018": 2,
    "2017": 1.75,
    "2016": 1.4,
    "2015": 1,
}
MN = 5200
YEAR = 2018
NUMTEAMS = 18
NUMROUNDS = 23
years = [2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009]
positions = ["Defender","Midfield","Ruck","Forward"]
pos_num_dict = {
    "Defender" : (6,8),
    "Midfield": (8,11),
    "Ruck": (2,3),
    "Forward": (6,8)
}
titles = ["fullname","firstname","secondname","games","birthdate","position","scPrice","height","weight"]
teams_dict = {
        'Adelaide':0,
        'Brisbane':1,
        'Carlton':2,
        'Collingwood':3,
        'Essendon':4,
        'Fremantle':5,
        'GWS':6,
        'Geelong':7,
        'Gold Coast':8,
        'Hawthorn':9,
        'Melbourne':10,
        'North Melbourne':11,
        'Port Adelaide':12,
        'Richmond':13,
        'St Kilda':14,
        'Sydney':15,
        'West Coast':16,
        'Western Bulldogs':17
}
teams_bye_dict = {
        'Adelaide':14,
        'Brisbane':13,
        'Carlton':14,
        'Collingwood':13,
        'Essendon':12,
        'Fremantle':12,
        'GWS':14,
        'Geelong':13,
        'Gold Coast':14,
        'Hawthorn':12,
        'Melbourne':13,
        'North Melbourne':14,
        'Port Adelaide':12,
        'Richmond':14,
        'St Kilda':12,
        'Sydney':13,
        'West Coast':13,
        'Western Bulldogs':12
}
