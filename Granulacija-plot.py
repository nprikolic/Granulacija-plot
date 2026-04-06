from matplotlib import pyplot as plt
import numpy as np

p_x=[0.063,0.09,0.25,0.71,2,4,8,11.2,16,24.2,31.5,45]
p_x_txt=["0.063","","0.25","0.71","2","4",
         "8","11.2","16","24.2","31.5","45"]

def f(x):
    return np.round(np.power(x,.5),decimals=2).astype('float') 
def r(x):
    return np.round(np.emath.logn(.5, x),decimals=2).astype('float') 

plt.figure(figsize=(7,5),dpi=300)
plt.gca().set_xscale("function", functions=(f,r))
plt.xlim([0.063, 45])
plt.ylim([0, 100])
plt.xticks(p_x,p_x_txt)
plt.xticks(rotation=45, ha='right')
plt.grid(which='major',axis='both',linewidth=1,color='black')

plt.xlabel("СТРАНА КВАДРАТНОГ ОТВОРА СИТА У mm (d⁰-⁴⁵)"
           ,size=12)
plt.ylabel("ПРОЛАЗАК КРОЗ СИТО У % МАСЕ"
           , size=12)



for i in range(len(p_x)):
    if i%2==0:
        for j in range(0,100,2):
            plt.plot([p_x[i],p_x[i+1]],[j,j],
                     color='black',
                     linewidth=.4)
            

p_y=[5,6,10,20,79,99,99.5,100,100,100,100,100]
p_y2=[0,1,1.1,1.3,1.6,2,2.4,4.5,15,99,100,100]

plt.plot(p_x, p_y,linewidth=2, c="red", label='Мешавина А')
plt.plot(p_x, p_y2,linewidth=2, c="green", label='Мешавина Б')
plt.legend(loc="lower right")
