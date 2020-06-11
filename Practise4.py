#Perfect

import math
import numpy as np
import scipy.stats as stats
from scipy import signal
import matplotlib.pyplot as plt
import pylab as pl

mean ={
    '2019':0,
    '2018':0,
    '2017':0,
    '2016':0,
    '2015':0,
}

stdev ={
    '2019':0,
    '2018':0,
    '2017':0,
    '2016':0,
    '2015':0,
}

year = 2019
total_rounds = 22
rd = 1

years = ['2019','2018','2017','2016','2015']

# --------- Function ---------- #


def sort_dict_array(dic :dict):
    for key in dic:
        dic[key].sort

def get_means(mean: dict, scores: dict):
    for year_key in mean:
        mean[year_key] = np.mean(scores[year_key])

def get_stdev(stdev: dict,scores: dict):
    for year_key in stdev:
        stdev[year_key] = np.std(scores[year_key])

# Weighted average of Stand Deviations within seasons
def weight_std(stdev:dict,scores:dict)->float:
    sum = 0
    div = 0
    for key in stdev:
        print(w_std(int(key)), stdev[key])
        sum += w_std(int(key)) * stdev[key] *len(scores[key])
        div += w_std(int(key)) *len(scores[key])

    return sum/div

def w_std(x:int) -> float:
    return math.exp(-(year-x)/2) #ARBRITARY PARAMATER

# This confidence in supercoach prediction need fine tuning
# Confidence/Standard Deviation in prediction of score this year
def get_seas_conf(mean:dict,pred_ave:float)->float:
    all_data =[]
    for key in mean:
        all_data.append(mean[key])
    all_data.append(pred_ave)
    conf = np.std(all_data)
    return conf

# Confidence/Standard Deviation in prediction of score within game
def get_game_conf(std_pred_seas:float, std_wt_season:float)->float:
    # Technical equation is std_seas/num_game
    # This is not entirly apt because uncertainty/std_dev entering a season is greater than by the end
    # can you add together standard deviations? std_model + unc_expected = total_uncertianty
    #  Total Uncertainty = Uncertinanty of average and uncertainty of game within season
    return math.sqrt(math.pow(std_pred_seas,2) + math.pow(std_wt_season,2)) #ARBRITARY PARAMATER


pred_ave = 125
new_score = 100
num_rounds = 22

st_dev_perc = 68.27
scores = {
    '2019':[new_score],
    '2018': [95,139,154,141,113,115,110,137,109,152,134,98,113,136,155,99,113,157,167,121,162,150,130],
    '2017': [ 82,135,105,113,71,83,58,82,92,120,98,116,93,105,80,77,125,103,114,93,97 ],
    '2016': [109,96,86,54,81,61,114,107,63,80,88,106,127,91,104,103,116,94,107,106,116,96],
    '2015': [ 73,114,98,91,119,87,89,60,93,105,78,86,108,64,95,89,90,125,57,91 ]
}

sort_dict_array(scores)
get_means(mean,scores)
get_stdev(stdev,scores)
std_wt_season = weight_std(stdev, scores)   # Weighted average of Stand Deviations within seasons
std_pred_seas = get_seas_conf(mean, pred_ave)
std_game = get_game_conf(std_pred_seas, std_wt_season)


#print(mean)
print("stdev",stdev)
print("std_wt_season",std_wt_season)
print("std_pred_seas",std_pred_seas)
print("std_game",std_game)

# Vector for plotting
x = np.arange(0,int(pred_ave + 5*std_game),1)


# Gaussian for Yearly averages
g_year_ave = stats.norm(pred_ave, std_pred_seas)
pdf_year_ave = g_year_ave.pdf(x)

# Gaussian of games upcoming
g_game = stats.norm(pred_ave, std_game)
pdf_game = g_game.pdf(x)

# Gaussian of new score given predicted varience
g_score = stats.norm(new_score, std_wt_season)
pdf_score = g_score.pdf(x)

# Create Gaussian of New_score
# Get Varience from new score
var = 0
for mean in x:
    var += g_score.pdf(mean) * math.pow((mean - pred_ave),2)

std_update = math.sqrt(var)

p_new_score = 0
# Get probability of the new_score for all possible average
for mean in x:
    tmp_gauss = stats.norm(mean,std_game)
    p_new_score += g_year_ave.pdf(mean)*tmp_gauss.pdf(new_score)

bays=[]
# iterate through possible averages
for score in x:
    # generate Gaussian Distribution of this average i with weighted standard deviation
    g_tmp = stats.norm(score, std_game)
    # Probability of new score given average i
    p_score_ave = g_tmp.pdf(new_score) * g_year_ave.pdf(score)

    bays.append(p_score_ave/p_new_score)

#normalise
prob_sum = np.sum(bays)
bays = np.divide(bays,prob_sum)

# Get Mean
mean_b =0
i = 0
std_b = 0
for mean in x:

    mean_b = mean_b + mean * bays[i]
    #print("mean_b2 = ",mean_b2,"mean = ", mean, "  bays prob = ", bays2[i])
    std_b += bays[i]*math.pow((mean - pred_ave),2)
    i+=1

std_b = math.sqrt(std_b)

g_bays = stats.norm(mean_b,std_b)
pdf_bays = g_bays.pdf(x)

#update std_game
std_game2 = get_game_conf(std_b, std_wt_season)
g_bay_game = stats.norm(mean_b,std_game2)
pdf_bay_game = g_bay_game.pdf(x)


# NOt bad but not relevant for sequential steps, onlyimportant if wanting to take risks at end which is niche
# Include so num rounds is viable
# Rest of season average
#new_std = math.sqrt(math.pow(std_game2,2) + math.pow(std_b,2))/math.sqrt(num_rounds-rd)
#g_rest_seas = stats.norm(mean_b,new_std)
#pdf_rest_seas = g_rest_seas.pdf(x)


# Plot
plt.plot(x,pdf_year_ave, color='r',label = 'Yearly Average')
plt.plot(x,pdf_game, color='b',label = 'Game Prediction')
plt.plot(x,pdf_bays, color='y',label = 'New Yearly Average')
plt.plot(x,pdf_bay_game, color='c',label = 'New Game Prediction')
#plt.plot(x,pdf_rest_seas, color='g',label = 'Rest of Season Average')

plt.legend(loc='upper left')
plt.show()
