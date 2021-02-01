
# coding: utf-8

# In[301]:


import math
import random
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import copy


# In[333]:


#NSSE DATA PROCESSING **************************************

def preprocess_nsse(data):
    drop_columns = ['tmprep','tmcocurr', 'tmworkon', 'tmworkoff', 'tmservice', 'tmrelax', 'tmcare','tmcommute']
    drop_indexes = []
    for k in drop_columns:
        for i,j in data.iterrows():
            if j[k] == '#NULL!':
                drop_indexes.append(i)
    df = data.drop(drop_indexes)
    return df
def percentages_calc(dataframe,column):
    percents_ = []
    for val in range(1,9):
        try:
            percents_.append((dataframe[column].value_counts()[str(val)]/dataframe.shape[0]))
        except:
            pass
#         break
    return percents_
def act_probs(dataframe):
    drop_columns = ['tmprep','tmcocurr', 'tmworkon', 'tmworkoff', 'tmservice', 'tmrelax', 'tmcare','tmcommute']
    percents = defaultdict(int)
    for i in drop_columns:
#         print(i,'*************')
#         print(dataframe.columns)
        percents[i] = percentages_calc(dataframe,i)
#         break
    return percents


# In[305]:


#CLEANING AND PREPROCESSING COLLEGE DATA
#1. DROPPING THE SPECIFIED VALUES
#2. FORMING A NEW COLUMN CONSISTING OF TIME SPENT IN CLASS IN MINUTES. IT WILL BE LATER USED.
def preprocess_college(df0):
   drops = ['Arranged','To Be Determined','Unknown','Unspecified']
   drop_indexes = []
   for i,j in df0.iterrows():
       if j['CLASSMEETINGPATTERN'] in drops:
           drop_indexes.append(i)
   df0 = df0.drop(drop_indexes)
   df0.reset_index(inplace=True)
   times = []
   for i in range(len(df0)):
       if df0.CLASSSTARTTIME[i] != 'Unknown' and df0.CLASSENDTIME[i] != 'Unknown':
           end = pd.to_datetime(df0.CLASSENDTIME[i]) 
           start = pd.to_datetime(df0.CLASSSTARTTIME[i])
           time = pd.Timedelta(end - start) / np.timedelta64(1, 'm')
           times.append(time)
       else:
           print('x')
           times.append(0)
   df0['timeofclass'] = times
   return df0


# In[290]:


def class_times(df_0):
    df_2 = df_0 
    student_keys = df_2.STUDENTSOURCEKEY.unique()
    key = random.choice(student_keys)
    df_1 = df_2.loc[df_2['STUDENTSOURCEKEY'] == key]
    tot_creds = df_1['CREDITSATTEMPTED'].sum()
    class_dict = defaultdict(int)
    for it,jt in df_1.iterrows():
        x = jt['CLASSMEETINGPATTERN'].replace('-',',')
        x = x.split(',')
        for days in x:
#             jt['timeofclass']
            print(days,'Kashyap')
            class_dict[days] += jt['timeofclass'] 
    return class_dict,tot_creds


# In[311]:


def class_times(table):
    table1 = copy.deepcopy(table) 
#     df2.reset_index(inplace=True)
    student_keys = table1.STUDENTSOURCEKEY.unique()
    key = random.choice(student_keys)
#     print(key)
#     df2.set_index('STUDENTSOURCEKEY',inplace=True)
#     df1 = df2.loc[key]
    table2 = copy.deepcopy(table1.loc[table1['STUDENTSOURCEKEY'] == key])
    tot_creds = table2['CREDITSATTEMPTED'].sum()
    class_dict = defaultdict(int)
    for it,jt in table2.iterrows():
        x = jt['CLASSMEETINGPATTERN'].replace('-',',')
        x = x.split(',')
        for days in x:
#             j['timeofclass']
#             print(jt['timeofclass'],'*********')
            class_dict[days] += jt['timeofclass'] 
#             break
#         break
    return class_dict,tot_creds


# In[252]:


# days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
# acts = pd.read_excel('activities.xlsx')
# com_probabilities = acts["commute_probs"].tolist()
# w_probabilities = nsse_probs['tmworkoff']
# s_probabilities = nsse_probs['tmrelax']


# In[253]:


# acts = pd.read_excel('activities.xlsx')
# # com_times = acts["commute_times"].tolist()
# com_probabilities = acts["commute_probs"].tolist()
# # w_times = acts["work_times"].tolist()
# w_probabilities = acts["work_probs"].tolist()
# s_times = acts["social_times"].tolist()
# s_probabilities = acts["social_probs"].tolist()


# In[254]:


# days = ['Monday','Tuesday','Wednesday','Thursday','Friday']


# In[255]:


def allocation(days,class_dict,tot_creds):
    my_dict = defaultdict(lambda : list())
    dict_bottom = defaultdict(lambda : list())
    
    tot_hw = tot_creds * 2 * 60
    tot_hw_rem = tot_hw
    for i,j in enumerate(days):
        #starting count timer = 0
        timer = 0
        
        #1sleep time generation
        sleep_time = math.floor(random.normalvariate(8.8,0.8)*60)
        my_dict['sleep'].append(sleep_time)  #calculated in hrs and converted to mins
        #update sleep time
        timer += sleep_time
        dict_bottom['class_time'].append(sleep_time)

        #2 class_time imported from the excel data
        class_time = class_dict[j]
        my_dict['class_time'].append(class_time)
        timer += class_time
        dict_bottom['eat_time'].append(dict_bottom['class_time'][i]+class_time)
       
        #3 eat time mean = 84 mins and sd = 5
        eat_time = math.floor(random.normalvariate(84,5))
        my_dict['eat'].append(eat_time)  #calculated in mins
        timer += eat_time
        dict_bottom['commute'].append(dict_bottom['eat_time'][i]+eat_time)

        #5 commute time in mins
        c_times = [0,5,10,15,20,25,30,32]
        c_probabilities = [0.196,0.462,0.188,0.077,0.038,0.015,0.006999999999999895,0.017]
        commute_time = int(np.random.choice(c_times,replace=True, p = c_probabilities)/5)*60
        my_dict['commute'].append(commute_time)
        timer += commute_time
        dict_bottom['work'].append(dict_bottom['commute'][i]+commute_time)

        #6 work on campus
        w_times = [0,5,10,15,20,25,30,32]
#         w_probabilities = [0.742,0.031,0.092,0.067,0.039,0.015,0.008,0.006]
        
#         w_times = [0,3,7.5,12.5,17.5,22.5,37.5,35]    #off campus
#         w_probabilities = [0.59,0.044,0.058,0.097,0.085,0.053,0.029,0.044]   #off campus
        
        work_time = int(np.random.choice(c_times,replace=True, p = w_probabilities)/5)*60

        my_dict['work'].append(work_time)
        timer += work_time
        dict_bottom['social'].append(dict_bottom['work'][i]+work_time)

        #7 socializing time in mins
        s_times = [0,5,10,15,20,25,30,32]
#         s_probabilities = [0.018,0.186,0.268,0.23,0.14,0.062,0.028,0.068]
        time_socializing = int(np.random.choice(s_times,replace=True, p = s_probabilities)/5)*60
        my_dict['social'].append(time_socializing)
        timer += time_socializing
        dict_bottom['hw'].append(dict_bottom['social'][i]+time_socializing)
        
        #8 HW allocation
        
        if tot_hw_rem >= 180:
            hw = 180
        elif 0 < tot_hw_rem < 180:
            hw = tot_hw_rem
        else:
            hw = 0
            
        my_dict['hw'].append(hw)  
        tot_hw_rem -= hw
        timer += hw 
        dict_bottom['residuals'].append(dict_bottom['hw'][i]+time_socializing)

        #9 residual time in mins
        my_dict['residuals'].append(1440-timer)
        #print(my_dict)
        cummulative = []
        for i in my_dict.keys():
            cummulative.append(sum(my_dict[i]))
        
        cumm_class = []
        for i in my_dict.keys():
            cumm_class.append(sum(my_dict[i]))
        
    return my_dict,dict_bottom,cummulative,cumm_class


# In[256]:


def plot_daily(my_dict,dict_bottom):
    N = 5
    sleep_times = my_dict['sleep']
    class_times =my_dict['class_time']
    commute_times = my_dict['commute']
    eat_times = my_dict['eat']
    work_times = my_dict['work']
    time_socializing = my_dict['social']
    hw_time = my_dict['hw']
    residual_times = my_dict['residuals']

    ind = np.arange(N)  
    width = 0.75      

    plt.figure(figsize=(7,5))
    p1 = plt.bar(ind, sleep_times, width)
    p2 = plt.bar(ind, class_times,width,bottom = dict_bottom['class_time'])
    p3 = plt.bar(ind, commute_times, width,bottom = dict_bottom['commute'])
    p4 = plt.bar(ind, eat_times,width,bottom = dict_bottom['eat_time'])
    p5 = plt.bar(ind, work_times,width,bottom= dict_bottom['work'])
    p6 = plt.bar(ind, time_socializing,width,bottom= dict_bottom['social'])
    p7 = plt.bar(ind, hw_time,width,bottom = dict_bottom['hw'])
    p8 = plt.bar(ind, residual_times,width,bottom= dict_bottom['residual'])

    plt.ylabel('minutes')
    plt.title('day of the week')
    plt.xticks(ind, ('Monday','Tuesday','Wednesday','Thursday','Friday'))
    plt.yticks(np.arange(0,600,1440))
    plt.legend((p1[0], p2[0],p3[0],p4[0],p5[0],p6[0],p7[0],p8[0]), ('sleep','class', 'commute','eat','work','social','hw','Residuals'),
                               bbox_to_anchor=(1.1,0.7), loc="lower right", 
                              bbox_transform=plt.gcf().transFigure)
    plt.show()
    return


# In[257]:


def plot_weekly(my_dict,cummulative):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = my_dict.keys()
    sizes = cummulative
    explode = (0,0,0,0,0,0,0,0.2)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            startangle=120)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     plt.savefig('time.png',dpi = 1080)
    plt.show()
    return


# In[258]:


# n,m = class_times(df0)
# x,y,z1,z2 = allocation(days,n,m)
# # plot_daily(x,y)
# plot_weekly(x,z1)
# # plot_weekly(x,z2)
# # x,y,z1,z2
# x


# In[362]:


def simulate(students, acts,dats,gender):
    negatives_x = []
    negatives_y = []
    residual_times = []
    for i in range(students):
    #     print(i)
        n,m = class_times(dats)
        residual_times_ind = []
        for j in range(acts):        
            a,b,c1,c2 = allocation(days,n,m)
            residual_times.append(c1[-1])
            if c1[-1] <0:
                negatives_x.append(a)
                negatives_y.append(b)
    residuals = [residual for residual in residual_times if residual>=0]
    print(sum(residuals)/len(residuals))
    plt.figure(figsize=(6,4))
    plt.violinplot(residuals,vert=True)
    plt.ylabel('Residual times in minutes')
    plt.title('Residual times over the weekday for :' + gender + ' Students')
    plt.show()


# In[306]:


df0_college = pd.read_excel('spring_2017.xlsx')


# In[320]:


# PREPROCESSING COLLEGE DATA
df0 = preprocess_college(df0_college)
dfn= copy.deepcopy(df0)


# In[327]:


data = pd.read_excel('NSSE_2017_all.xlsx')
# data.reset_index(inplace=True)


# In[336]:


#SETTING PARAMETERS
students_to_be_selected = 50
activities_combination  = 20


# In[364]:


#SIMULATING FOR GENDERS
 # UNCOMMENT AND RUN FOR PRINTING GENDER WISE SIMULATION
tickers = ['Male','Female']
for sex in tickers:   
    data = pd.read_excel('NSSE_2017_all.xlsx')
    data.reset_index(inplace=True)
    data = data.loc[data['Gender'] == sex]
    nsse_ready = preprocess_nsse(data)
    nsse_probs =  act_probs(nsse_ready)
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    acts = pd.read_excel('activities.xlsx')
    com_probabilities = acts["commute_probs"].tolist()
    w_probabilities = nsse_probs['tmworkoff']
    s_probabilities = nsse_probs['tmrelax']
    simulate(students_to_be_selected,activities_combination,dfn.loc[dfn['GENDER'] == sex],sex)
    


# In[376]:


#SIMULATING FOR ETHNICITY
 # UNCOMMENT AND RUN FOR PRINTING GENDER WISE SIMULATION
tickers = ['WHI', 'HIS', 'ASI', 'FOR', 'UNK', 'AFR', 'IND', 'MUL', 'HPI']
for sex in tickers:   
    data = pd.read_excel('NSSE_2017_all.xlsx')
    data.reset_index(inplace=True)
    data = data.loc[data['Ethnicity'] == sex]
    nsse_ready = preprocess_nsse(data)
    nsse_probs =  act_probs(nsse_ready)
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    acts = pd.read_excel('activities.xlsx')
    com_probabilities = acts["commute_probs"].tolist()
    w_probabilities = nsse_probs['tmworkoff']
    s_probabilities = nsse_probs['tmrelax']
    simulate(students_to_be_selected,activities_combination,dfn.loc[dfn['GENDER'] == sex],sex)
    
