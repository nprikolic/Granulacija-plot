from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

p_x=[0.063,0.09,0.25,0.71,2,4,8,11.2,16,24.2,31.5,45]
p_x_txt=["0.063","","0.25","0.71","2","4",
         "8","11.2","16","24.2","31.5","45"]

def f(x):
    return np.round(np.power(x,.5),decimals=2).astype('float') 
def r(x):
    return np.round(np.emath.logn(.5, x),decimals=2).astype('float') 

plt.figure(figsize=(7,4),dpi=300)
plt.gca().set_xscale("function", functions=(f,r))
plt.xlim([0.063, 45])
plt.ylim([0, 100])
plt.xticks(p_x,p_x_txt)
plt.xticks(rotation=45, ha='right')
plt.grid(which='major',axis='both',linewidth=1,color='black')

plt.xlabel("СТРАНА КВАДРАТНОГ ОТВОРА СИТА У mm (d⁰-⁴⁵)"
            ,size=10)
plt.ylabel("ПРОЛАЗАК КРОЗ СИТО У % МАСЕ"
            , size=10)

for i in range(len(p_x)):
    if i%2==0:
        for j in range(0,100,2):
            plt.plot([p_x[i],p_x[i+1]],[j,j],
                      color='black',
                      linewidth=.4)

df=pd.read_excel("in.xlsx",header=None)
for i in range(1,len(df.columns)):
    try:
        ime=df.iloc[0,i]
        boja=df.iloc[1,i]
        lw=df.iloc[2,i]
        prolazi=df.iloc[3:,i]
        plt.plot(p_x,prolazi,linewidth=lw,
                 color=boja, label=ime)
    except:
        print("Nešto ne radi za kolonu", i)


plt.legend(loc="lower right")
plt.savefig("out.png", bbox_inches='tight')




