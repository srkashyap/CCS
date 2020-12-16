
# coding: utf-8

# In[399]:


import math
import random
import datetime
import seaborn as sns

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[44]:


df1 = pd.read_excel('2199 SCHEDULES 10232020.xlsx')


# In[52]:


drops = ['Arranged','To Be Determined','Unknown','Unspecified']
drop_indexes = []
for i,j in df1.iterrows():
    if j['CLASSMEETINGPATTERN'] in drops:
        drop_indexes.append(i)
df0 = df1.drop(drop_indexes)


# In[163]:


df0 = df0.drop_duplicates()


# In[36]:


cls_lst = np.zeros((1440,0)) 


# In[37]:


x = pd.to_datetime(df0.CLASSSTARTTIME[3])
y = pd.to_datetime(df0.CLASSENDTIME[3])


# In[164]:


df0.columns


# In[165]:


df0['STUDENTSOURCEKEY'].unique()


# In[166]:


students = df0.groupby(by = ['STUDENTSOURCEKEY'])


# In[274]:


st = np.zeros((1440,6))
days_map=['monday','tuesday','wednesday','thursday','friday','saturday']


# In[283]:


res = np.zeros((960,6))


# In[284]:


for i,j in students:
#     print(i,j.shape)
    fin = np.zeros(np.shape(res))
    for m,n in j.iterrows():
        day=n['CLASSMEETINGPATTERN']
        if (',' not in day) and ('-' not in day) and ('to' not in day):
            day=(day.lower())
            dates=pd.date_range(n["CLASSSTARTTIME"], n["CLASSENDTIME"], freq="1min")
            st = dates.hour-7
            st = ((st)*60)+ dates.minute
#             print('hi',i,(st,day))
#                 print(dates)
            coords = np.array([st,days_map.index(day)])
            np.put(fin, np.ravel_multi_index(coords.T, fin.shape), 1)
    res+=fin                          
print(res[400:450,:])


# In[286]:


np.shape(res)


# In[ ]:


date_int = df0.date_range(row["starttm"], row["endtm"], freq="5min")


# In[356]:


np.shape(res)


# In[400]:


fig, ax = plt.subplots(dpi = 100)
im = ax.imshow(res,aspect='auto')
# ax.pcolor(res,cmap='YlGnBu')

ax.set_xticks(np.arange(6))
# ax.set_yticks(np.arange(5))

ax.set_xticklabels(days_map,fontsize = 7)
# ax.set_yticklabels(np.arrange(960))
# plt.imshow(res)
# plt.colorbar()
heatmap = plt.pcolor(res)
plt.colorbar(heatmap)

plt.title('heatmap for classes throughout the week')
ax.legend()
plt.show()


# In[450]:


fig, ax = plt.subplots(figsize = (15,9))
ax = sns.heatmap(res,cmap="YlGnBu")

plt.xlabel("Days",fontsize = 15)
plt.ylabel("Time",fontsize = 15)



ax.set_xticks(np.arange(6))
ax.set_yticks(np.arange(9))
y_label=np.arange(960)
print(y_label)
ax.set_xticklabels(days_map,fontsize = 15)
ax.set_yticklabels(y_label)

plt.title('heatmap for classes throughout the week')
ax.legend()
plt.show()

