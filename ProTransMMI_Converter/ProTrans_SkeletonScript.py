# -*- coding: utf-8 -*-
"""
MMI Conversion Script - Skeleton

This script is the main mathematics behind converting the JMA stream to an MMI
value and plotting it to a graph.

This is not as visually pleasing as a full GUI but the intention is to have
the functions of this script easily incorporated into the main GUI application
or other applications as needed.


@author: Jacob Kukovica, Scientific Data Specialist, Ocean Networks Canada
"""

#%% Import Python Modules

from onc.onc import ONC
import matplotlib.pyplot as plt
import math as m
import datetime
import numpy as np
# from pandas import DataFrame
# import time

#%% Retrieve Data from Oceans2.0

token = ONC('ONC_TOKEN_HERE')


timeNow = datetime.datetime.utcnow()-datetime.timedelta(seconds=5)

totalTime = 60 #    How much time you want displayed on the graph in seconds

dateForm = "%Y-%m-%dT%H:%M:%S.000Z"
dateForm_Plot = "%H:%M:%S.%f"

dateFrom = timeNow - datetime.timedelta(seconds = totalTime)
dateTo = timeNow

dateFrom = dateFrom.strftime(dateForm)
dateTo = dateTo.strftime(dateForm)

#%% Enter live time loop

start = True
count = 0 # Counter variable for iterations to file

times = []
jma = []
mmi = []

# while start == True:
filters = {
    'deviceCode': 'PUT DEVICE CODE HERE',
    'dateFrom': dateFrom,
    'dateTo': dateTo}

results = token.getDirectRawByDevice(filters, allPages = False)

#%% Remove the JMA lines from Data and Convert
jmaLines = [s for s in results['data']['readings'] if "JMA Intensity" in s]

times_New = []
times_Plot = []
jma_New = []
mmi_New = []


for sub in jmaLines:
    times_New.append(sub[:sub.find(' ')])
    temp_jma = sub[sub.rfind(' ')+1:]
    mmi_con = 2.1*m.log10(float(temp_jma)*100) + 2.3
    jma_New.append(float(temp_jma))
    mmi_New.append(mmi_con)
    

    
times += times_New
jma += jma_New
mmi += mmi_New

timeAxis = np.arange(0,len(times_New),1)
    
#%% Plot the results

fig, axs = plt.subplots(2,1)



axs[0].plot(timeAxis, jma_New)
axs[0].set_xlabel('Time')
axs[0].set_ylabel('JMA (cm/s/s)')
axs[0].grid(True)
axs[1].plot(timeAxis, mmi_New)
axs[1].set_xlabel('Time')
axs[1].set_ylabel('MMI')
axs[1].grid(True)

fig.suptitle("JMA to MMI Conversion from " + times_New[0] + " to " + times_New[-1])
plt.show()

    
    # count += 1
    
    # if count == 3:
    #     data = [times, jma, mmi]
    #     df = DataFrame(data).transpose()
    #     df.columns = ['Time (UTC)', 'JMA (cm/s)', 'MMI']
    #     df.to_csv(times[0][:times[0].rfind('.')+1] + '_Log.csv', index = False, header = True)
    #     count = 0
    #     times = []
    #     jma = []
    #     mmi = []
    # time.sleep(7)    
    
    # dateFrom = times_New[-1]
    # dateTo = datetime.datetime.utcnow() - datetime.timedelta(seconds = 2)
    # dateTo = dateTo.strftime(dateForm)

    
 