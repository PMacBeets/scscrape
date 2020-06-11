import math
import numpy as np
import scipy.stats as stats
from scipy import signal
import matplotlib.pyplot as plt
import pylab as pl

# replace with a log function or something
stdev_w = [10,7,5,4]

pred_ave = 125
num_rounds = 22

st_dev_perc = 68.27
y_2018 = [95,139,154,141,113,115,110,137,109,152,134,98,113,136,155,99,113,157,167,121,162,150,130]
y_2017 = [ 82,135,105,113,71,83,58,82,92,120,98,116,93,105,80,77,125,103,114,93,97 ]
y_2016 = [109,96,86,54,81,61,114,107,63,80,88,106,127,91,104,103,116,94,107,106,116,96]
y_2015 = [ 73,114,98,91,119,87,89,60,93,105,78,86,108,64,95,89,90,125,57,91 ]

all_data = y_2018 + y_2017 + y_2016 + y_2015
min_s = min(all_data)
max_s = max(all_data)

#x = np.linspace(min_s,max_s,num=1000)

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

year_mean = [pred_ave, mean_2018, mean_2017, mean_2016, mean_2015]
year_mean.sort()
std_years = np.std(year_mean)

g_2018 = stats.norm(mean_2018, std_2018)
g_2017 = stats.norm(mean_2017, std_2017)
g_2016 = stats.norm(mean_2016, std_2016)
g_2015 = stats.norm(mean_2015, std_2015)

g_year_ave = stats.norm(pred_ave, std_years)

x = np.arange(int(pred_ave - 5*std_years),int(pred_ave + 5*std_years),1)

pdf_2018 = g_2018.pdf(x)
pdf_2017 = g_2017.pdf(x)
pdf_2016 = g_2016.pdf(x)
pdf_2015 = g_2015.pdf(x)
pdf_year_ave = g_year_ave.pdf(x)

# Graph all scores and annual Gaussian Distributions

fig, ax1 = plt.subplots()
ax1.plot(x, pdf_2018)
ax1.plot(x, pdf_2017)
ax1.plot(x, pdf_2016)
ax1.plot(x, pdf_2015)
ax1.plot(x, pdf_year_ave)

ax1.set_ylim(bottom=0,top=.05)

ax2 = ax1.twinx()
binwidth = 1
ax2.hist(y_2018,bins=range(min(y_2018), max(y_2018) + binwidth, binwidth))
ax2.hist(y_2017,bins=range(min(y_2017), max(y_2017) + binwidth, binwidth))
ax2.hist(y_2016,bins=range(min(y_2016), max(y_2016) + binwidth, binwidth))
ax2.hist(y_2015,bins=range(min(y_2015), max(y_2015) + binwidth, binwidth))


plt.show()

new_score = 20

g_score = stats.norm(new_score, std_season)
pdf_score = g_score.pdf(x)


# Gaussian of Predicted future season
g_future = stats.norm(pred_ave,std_season)
pdf_future = g_future.pdf(x)

plt.plot(x,pdf_future, color='r',label = 'Disribution of Scores')
plt.plot(x, pdf_year_ave, color = 'b', label = "Probability Distribution of average for remainder of year")


p_score = 0

#x2 = np.linspace(int(pred_ave - 3*std_years),int(pred_ave + 3*std_years),1000)
# Probability of new score given predicted average
# three standard deviations get 99% of the values
"""for mean in x:
    g_tmp =  stats.norm(mean, std_season)
    p_score += g_tmp.pdf(new_score) * g_year_ave.pdf(mean)"""

prob_ave = []
arr1 = []

print("probability of scoring the score ", new_score, " is: ", p_score)

# iterate through possible averages
for mean in x:
    # generate Gaussian Distribution of this average i with weighted standard deviation
    g_tmp = stats.norm(mean, std_season)

    # Probability of new score given average i
    p_score_ave = g_tmp.pdf(new_score) * g_year_ave.pdf(mean)
    arr1.append(g_tmp.pdf(new_score))
    #print("mean: p_score_ave = g_tmp.pdf(new_score) * g_year_ave.pdf(mean)",mean,p_score_ave, g_tmp.pdf(new_score), g_year_ave.pdf(mean))

    #print("Probability of score given mean of: ",mean, " is: ",p_score_ave)

    prob_ave.append(p_score_ave/g_year_ave.pdf(new_score))


prob_sum = np.sum(prob_ave)
prob_ave = np.divide(prob_ave,prob_sum)
#print("Sum of all area is: ",np.sum(prob_ave))

#print(prob_ave.size,pdf_year_ave.size)

conv_prob = signal.fftconvolve(prob_ave,pdf_year_ave,'same') #np.convolve(prob_ave,pdf_year_ave)
print("Sum of all convolved area is: ",np.sum(conv_prob))

plt.plot(x,prob_ave,color = 'g', label = " Shifted Probability Distribution of average for remainder of year")
plt.plot(x,conv_prob,color = 'c', label = "Convolved")
plt.plot(x,arr1,color = 'm', label = " Score given average")
plt.plot(x,pdf_score,color ='k',label='PDF of new_Score')
plt.legend(loc='upper left')


    # Proba

plt.show()





