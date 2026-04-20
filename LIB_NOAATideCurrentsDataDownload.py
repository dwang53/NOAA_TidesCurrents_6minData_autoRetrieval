import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import urllib
import os,sys


def genNOAALink(stationNo,begin_date,end_date,datum,timezone,unit,format):
    outLink=('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=water_level&application=NOS.COOPS.TAC.WL&begin_date='+begin_date+'&end_date='+end_date
             +'&datum='+datum+'&station='+stationNo+'&time_zone='+timezone+'&units='+unit+'&format='+format)
    return outLink


def get_monthly_periods(start_date, end_date):
    from datetime import datetime, timedelta
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d")
    
    # Initialize the current date to the start date
    current = start
    periods = []
    
    while current < end:
        # Get the last day of the current month
        next_month = current.replace(day=28) + timedelta(days=4)  # this will never fail
        last_day_of_month = next_month - timedelta(days=next_month.day)
        
        # If the end date is in the current month
        if end.year == current.year and end.month == current.month:
            periods.append([current.strftime("%Y%m%d"), end.strftime("%Y%m%d")])
            break
        else:
            periods.append([current.strftime("%Y%m%d"), last_day_of_month.strftime("%Y%m%d")])
        
        # Set the current date to the first day of the next month
        current = (last_day_of_month + timedelta(days=1)).replace(day=1)
    
    return periods

# Example usage
#start_date = "20230105"
#end_date = "20230425"
#monthly_periods = get_monthly_periods(start_date, end_date)
#print(monthly_periods)



def downloadNOAA_WSE(NOAAstationNo,NOAAbegin_date,NOAAend_date,datum='MLLW',timezone='GMT',unit='metric',format='csv',debugFlag=False):
    ListDateTimes=get_monthly_periods(NOAAbegin_date, NOAAend_date)
    print('Downloading the NOAA data in',timezone,'time zone!')
    dowloadLink=genNOAALink(NOAAstationNo,NOAAbegin_date,NOAAend_date,datum,timezone,unit,format)
    print('Downloading',dowloadLink)
    if len(ListDateTimes)==0:
        print('ERROR in downloadNOAA_WSE!!!, Illigal Start and End Date inputs!')
        return

    DfNOAA_ALL=pd.DataFrame()
    for datetimepairs in ListDateTimes:
        dowloadLink=genNOAALink(NOAAstationNo,datetimepairs[0],datetimepairs[1],datum,timezone,unit,format)
        try:
            dfNOAA=pd.read_csv(dowloadLink)
            dfNOAA['datetime']=pd.to_datetime(dfNOAA['Date Time'])
            #dfNOAA['20d']=dfNOAA['20d']-pd.Timedelta(5,'hour')#Time zone shift
            dfNOAA=dfNOAA.set_index(['datetime'])
            DfNOAA_ALL=pd.concat([DfNOAA_ALL,dfNOAA])
        except:
            if debugFlag:
                print('WARNNING in downloadNOAA_WSE! Skip data period',datetimepairs[0],'to',datetimepairs[1])
    return DfNOAA_ALL

if __name__ == "__main__": 
    NOAAstation='8764314'
    NOAAbegindate='20150401'
    NOAAenddate='20241231'
    
    #NOAAfname='https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=water_level&application=NOS.COOPS.TAC.WL&begin_date=20230101&end_date=20230201&datum=MLLW&station=8764314&time_zone=GMT&units=metric&format=csv'
    dfNOAA_EugeneIsland=downloadNOAA_WSE(NOAAstation,NOAAbegindate,NOAAenddate)
    dfNOAA_EugeneIsland