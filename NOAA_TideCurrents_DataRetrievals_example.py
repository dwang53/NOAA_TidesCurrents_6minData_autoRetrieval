#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import urllib
import os,sys
import requests


# In[2]:


#sys.path.append('NOAARetrievals')
from LIB_NOAATideCurrentsDataDownload import *


# In[13]:


NOAAstation='8761724' #Grand Isle
NOAAbegindate='20250101'#Startdate
NOAAenddate='20251231'#Enddate
NOAADatum='MLW'
NOAAUnit='metric'
dfNOAA=downloadNOAA_WSE(NOAAstation,NOAAbegindate,NOAAenddate,datum=NOAADatum,timezone='GMT',unit=NOAAUnit)
dfNOAA.to_csv('NOAA'+NOAAstation+'_dt_from_'+NOAAbegindate+'_to_'+NOAAenddate+'_datum_MLW'+'.csv')
dfNOAA


# In[14]:


plt.figure(figsize=(12,4))
plt.plot(dfNOAA[' Water Level'])
plt.ylabel('Water Level (m, '+NOAADatum+')')
plt.grid()
plt.tight_layout()
plt.savefig('NOAA'+NOAAstation+'_dt_from_'+NOAAbegindate+'_to_'+NOAAenddate+'_datum_MLW'+'.png',dpi=300)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




