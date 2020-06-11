"""import statistics
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import scipy.stats as stats

h = [95,139,154,141,113,115,110,137,109,152,134,98,113,136,155,99,113,157,167,121,162,150,130]
h.sort()


fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed

pl.plot(h,fit,'-o')

pl.hist(h,normed=True)      #use this to draw histogram of your data

pl.show()"""
import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pylab as pl
st_dev_perc = 68.27
h = [95,139,154,141,113,115,110,137,109,152,134,98,113,136,155,99,113,157,167,121,162,150,130]

num_games = 22

h.sort()
mean = np.mean(h)
std = np.std(h)
std_mean = std/math.sqrt(num_games)
gauss = stats.norm(mean, std)
gauss_mean = stats.norm(mean, std_mean)
print(gauss)


av_list = []
mean_list = []
old_mean_list = []
new_score = 181
# for possible averages (2 stnd dev from mean)
for i in range(int(mean - 2 * std),int(mean + 2 * std)):
    tmp_gauss = stats.norm(i, std)
    new = tmp_gauss.pdf(new_score)
    old = gauss_mean.pdf(new_score)
    tup = (new / old * gauss_mean.pdf(i),i)
    old_mean_list.append(gauss_mean.pdf(i))
    print("average = ",i, "Chance of score given average = ",new,"   Chance of score given old average = ",old, "Chance of average given score", tup[0])
    mean_list.append(tup)


print(mean_list)
l_np = np.asarray(mean_list)
#plt.plot(l_np[:,1],l_np[:,0],color = 'r')
plt.plot(l_np[:,1],old_mean_list,color = 'b')



max_score = max(mean_list)
print("expected average given score of: ",new_score," is:",max_score)
    # predict probability of this average given the new score
#plt.show()# including h here is crucial


pdf = gauss.pdf(h)
cdf = gauss.cdf(h)



print("new score is: ",new_score,"Probability is: ", gauss.pdf(new_score))



# Plot Data
fig, ax1 = plt.subplots()
#plt.xlim(80,max(h))
ax1.plot(h, pdf)
ax1.set_ylim(bottom=0,top=.02)
ax2 = ax1.twinx()
binwidth = 1
ax2.hist(h,bins=range(min(h), max(h) + binwidth, binwidth))

plt.show()# including h here is crucial

"""fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed

pl.plot(h,fit,'-o')

pl.hist(h,normed=True)      #use this to draw histogram of your data

pl.show()"""

