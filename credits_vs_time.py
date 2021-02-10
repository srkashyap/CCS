
import math
import random
import datetime
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


# In[23]:


df1 = pd.read_excel('spring_2017.xlsx')


# In[88]:


len(df1['STUDENTSOURCEKEY'].unique())


# In[89]:


df1.columns


# In[90]:


df1 = df1[['STUDENTSOURCEKEY',
       'PS_RPT_REGISTRATION_V.TERMSOURCEKEY',
       'PS_RPT_REGISTRATION_V.CLASSNUMBERSECTION', 'CLASSMEETINGPATTERN',
       'CREDITSATTEMPTED', 'CLASSSTARTTIME', 'CLASSENDTIME',]]


# In[91]:


# df_byk = df1.groupby(['STUDENTSOURCEKEY'])


# In[92]:


data = df1[~df1.CLASSMEETINGPATTERN.isin(['Arranged','To Be Determined','Unknown','Unspecified'])]


# In[93]:


data['CLASSSTARTTIME'] = pd.to_datetime(data['CLASSSTARTTIME'],format='%I:%M%p')
data['CLASSENDTIME'] = pd.to_datetime(data['CLASSENDTIME'],format='%I:%M%p')


# In[94]:


data['TIMES'] = (data['CLASSENDTIME'] - data['CLASSSTARTTIME']).dt.total_seconds()/60


# In[95]:


data = data.drop_duplicates()
data


# In[96]:


len(data['STUDENTSOURCEKEY'].unique())


# In[97]:


students = data.groupby(['STUDENTSOURCEKEY'])
students.head(20)


# In[98]:


count = 0
c = 0
main = defaultdict(int)
for i,j in students:
    sub = defaultdict(int)
    
    for m,n in j.iterrows():
#         print(n['CLASSMEETINGPATTERN'].split(','))  
#         print(n['TIMES'],i)
        for k in n['CLASSMEETINGPATTERN'].split(','):
            sub[k] += n['TIMES']
    val = sum(j['CREDITSATTEMPTED'])
#     print(i,val)
    sub['Credits'] = val
    main[i] = sub
#     count+=1
#     if count ==18:
#         break
# #     break
# # main


# In[99]:


fin = pd.DataFrame.from_dict(main)
fin


# In[100]:


final = fin.T.fillna(0)


# In[101]:


final[['Monday', 'Wednesday', 'Friday', 'Thursday', 'Tuesday', 'Saturday']]


# In[102]:


final = final[['Monday','Tuesday', 'Wednesday',  'Thursday','Friday', 'Saturday','Credits']]
final


# In[81]:


# m.to_excel('credits_vs_count.xlsx', sheet_name='Sheet_name_1')


# In[103]:


# final.to_excel('final.xlsx', sheet_name='Sheet_name_1')



x1 = list(final[final['Credits']<=9].mean())[:5]
x2 = list(final[(final['Credits']>=10) & (final['Credits']<=12)].mean())[:5]
x3 = list(final[(final['Credits']>=13) & (final['Credits']<=15)].mean())[:5]
x4 = list(final[final['Credits']>=15].mean())[:5]


x_1 = [750-a for a in x1]
x_2 = [750-a for a in x2]
x_3 = [750-a for a in x3]
x_4 = [750-a for a in x4]




bars = ['Monday','tuesday','wednesday','thursday','friday']


plt.plot(x_1)
plt.plot(x_2)
plt.plot(x_3)
plt.plot(x_4)
plt.xticks(np.arange(5),bars)
plt.legend(['<9','10-12','13-15','>15'])
plt.show()
