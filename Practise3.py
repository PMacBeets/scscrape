import math
import numpy as np
import scipy.stats as stats
from scipy import signal
import matplotlib.pyplot as plt
import pylab as pl
# --------- Function ---------- #
def w_std(x:int) -> float:
    return math.exp(x/2)

# replace with a log function or something
stdev_w = [10,7,5,4]

pred_ave = 125
new_score = 81
num_rounds = 22

st_dev_perc = 68.27
y_2019 = [new_score]
y_2018 = [95,139,154,141,113,115,110,137,109,152,134,98,113,136,155,99,113,157,167,121,162,150,130]
y_2017 = [ 82,135,105,113,71,83,58,82,92,120,98,116,93,105,80,77,125,103,114,93,97 ]
y_2016 = [109,96,86,54,81,61,114,107,63,80,88,106,127,91,104,103,116,94,107,106,116,96]
y_2015 = [ 73,114,98,91,119,87,89,60,93,105,78,86,108,64,95,89,90,125,57,91 ]

all_data = y_2018 + y_2017 + y_2016 + y_2015
min_s = min(all_data)
max_s = max(all_data)

#x = np.linspace(min_s,max_s,num=1000)
ng_2019 = len(y_2019)
ng_2018 = len(y_2018)
ng_2017 = len(y_2017)
ng_2016 = len(y_2016)
ng_2015 = len(y_2015)

y_2018.sort()
y_2017.sort()
y_2016.sort()
y_2015.sort()

mean_2018 = np.mean(y_2018)
std_2018 = np.std(y_2018)
mean_2017 = np.mean(y_2017)
std_2017 = np.std(y_2017)
mean_2016 = np.mean(y_2016)
std_2016 = np.std(y_2016)
mean_2015 = np.mean(y_2015)
std_2015 = np.std(y_2015)

# Add num games and weighting for this years statss
std_season = (stdev_w[0] * std_2018 + stdev_w[1] * std_2017 + stdev_w[2] * std_2016 + stdev_w[3] * std_2015)/(stdev_w[0] + stdev_w[1] + stdev_w[2] + stdev_w[3])
print("Predicted Standard Distribution of scores within a season is: ",std_season)

# Get standard deviation of yearly averages
year_mean = [pred_ave, mean_2018, mean_2017, mean_2016, mean_2015]
year_mean.sort()
std_years = np.std(year_mean)

# Vector for plotting
x = np.arange(0,int(pred_ave + 5*std_years),1)

# Gaussian for Yearly averages
g_year_ave = stats.norm(pred_ave, std_years)
pdf_year_ave = g_year_ave.pdf(x)

# Gaussian for upcoming games given predicted average and deviation
g_future = stats.norm(pred_ave,std_season)
pdf_future = g_future.pdf(x)

# Gaussian of new score given predicted varience
g_score = stats.norm(new_score, std_season)
pdf_score = g_score.pdf(x)


# Create Gaussian of New_score
# Get Varience from new score
var = 0
for mean in x:
    var += g_score.pdf(mean) * math.pow((mean - pred_ave),2)

std_update = math.sqrt(var)

print("standard deviation changed from: ", std_season," to:",std_update)

# Gaussian of new score given updates varience
g_score = stats.norm(new_score, std_update)
pdf_score_up = g_score.pdf(x)

# Convoluted Gaussian from predicted varience
conv_pred = signal.fftconvolve(pdf_score,pdf_year_ave,'same')

# Convoluted Gaussian from updated varience
conv_update = signal.fftconvolve(pdf_score_up,pdf_year_ave,'same')

# Baysian update is Same as Convolution for any value of n
#update mean
m = pred_ave
mm = new_score
o = std_season
oo = std_update
n = 0

mmm = (pow(o,2)*mm + n*pow(oo,2)*m)/(n*pow(oo,2)+pow(o,2))
std_bay = math.sqrt(pow(o,2)* pow(oo,2)/(n*pow(oo,2) + pow(o,2)) )

# Baysian Gaussian from updated varience - Same as 'Gaussian of new score given updated varience'
g_bays = stats.norm(mmm, std_bay)
pdf_bays = g_bays.pdf(x)

bays2=[]
# iterate through possible averages
for mean in x:
    # generate Gaussian Distribution of this average i with weighted standard deviation
    g_tmp = stats.norm(mean, std_update)

    # Probability of new score given average i
    p_score_ave = g_tmp.pdf(new_score) * g_year_ave.pdf(mean)

    bays2.append(p_score_ave/g_year_ave.pdf(new_score))
#normalise
prob_sum = np.sum(bays2)
bays2 = np.divide(bays2,prob_sum)


mean_b2 =0
i = 0;
std_b2 = 0
for mean in x:

    mean_b2 = mean_b2 + mean * bays2[i]
    #print("mean_b2 = ",mean_b2,"mean = ", mean, "  bays prob = ", bays2[i])
    std_b2 += bays2[i]*math.pow((mean - pred_ave),2)
    i+=1

std_b2 = math.sqrt(std_b2)

print(mean_b2,std_b2)

#mean_b2 = np.mean(bays2)
#std_b2 = np.std(bays2)
g_bays2 = stats.norm(mean_b2,std_b2)
pdf_bays2 = g_bays2.pdf(x)


plt.plot(x,pdf_future, color='r',label = 'Gaussian for upcoming games')
plt.plot(x, pdf_year_ave, color = 'b', label = "Gaussian for Yearly averages")
plt.plot(x,pdf_score, color = 'm', label = 'Gaussian of new score given predicted varience')
plt.plot(x,pdf_score_up, color = 'y', label = 'Gaussian of new score given updated varience')
#plt.plot(x,conv_pred, color = 'g', label = 'Convoluted Gaussian from predicted varience')
#plt.plot(x,conv_update, color = 'c', label = 'Convoluted Gaussian from updated varience')
plt.plot(x,pdf_bays, color = 'c', label = 'Baysian Gaussian from updated varience')
plt.plot(x,bays2, color = 'k', label = 'Baysian Gaussian caluculated individually')
plt.plot(x,pdf_bays2, color = 'g', label = 'Baysian Gaussian caluculated into pdf')
plt.legend(loc='upper left')
plt.show()
