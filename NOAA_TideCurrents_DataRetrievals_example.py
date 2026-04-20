#!/usr/bin/env python
# coding: utf-8

"""
NOAA_TideCurrents_DataRetrievals_example.py

Example workflow for downloading NOAA Tides & Currents 6-minute water-level
data, saving the result to CSV, and generating a quick-look figure.

This script is intended to demonstrate a clear and reproducible scientific
workflow using the helper functions in LIB_NOAATideCurrentsDataDownload.py.
"""

import matplotlib.pyplot as plt
from LIB_NOAATideCurrentsDataDownload import downloadNOAA_WSE


def main():
    """
    Run an example NOAA data download, export, and visualization workflow.
    """
    # ------------------------------------------------------------------
    # User-configurable inputs
    # ------------------------------------------------------------------
    NOAAstation = "8761724"       # Grand Isle station ID
    NOAAbegindate = "20250101"    # Start date in YYYYMMDD format
    NOAAenddate = "20251231"      # End date in YYYYMMDD format
    NOAADatum = "MLW"             # Vertical datum used by NOAA
    NOAAUnit = "metric"           # Output units: 'metric' or 'english'
    NOAATimezone = "GMT"          # NOAA API time zone option

    # ------------------------------------------------------------------
    # Download the NOAA water-level data
    # ------------------------------------------------------------------
    dfNOAA = downloadNOAA_WSE(
        NOAAstationNo=NOAAstation,
        NOAAbegin_date=NOAAbegindate,
        NOAAend_date=NOAAenddate,
        datum=NOAADatum,
        timezone=NOAATimezone,
        unit=NOAAUnit,
        format="csv",
        debugFlag=True,
    )

    # ------------------------------------------------------------------
    # Build consistent output file names
    # ------------------------------------------------------------------
    output_base = (
        f"NOAA{NOAAstation}_dt_from_{NOAAbegindate}_to_{NOAAenddate}_datum_{NOAADatum}"
    )
    csv_file = f"{output_base}.csv"
    fig_file = f"{output_base}.png"

    # ------------------------------------------------------------------
    # Save the downloaded dataframe to CSV
    # ------------------------------------------------------------------
    dfNOAA.to_csv(csv_file)
    print(f"Saved CSV file: {csv_file}")
    print(f"Number of records downloaded: {len(dfNOAA)}")

    # ------------------------------------------------------------------
    # Plot the water-level time series
    # ------------------------------------------------------------------
    plt.figure(figsize=(12, 4))
    plt.plot(dfNOAA["Water Level"], linewidth=0.8)
    plt.ylabel(f"Water Level (m, {NOAADatum})")
    plt.xlabel("Datetime")
    plt.title(
        f"NOAA Station {NOAAstation} Water Level\n"
        f"{NOAAbegindate} to {NOAAenddate}"
    )
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_file, dpi=300)
    print(f"Saved figure file: {fig_file}")

    # Optional: show the first few rows for quick inspection
    print("\nPreview of downloaded data:")
    print(dfNOAA.head())


if __name__ == "__main__":
    main()#!/usr/bin/env python
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




