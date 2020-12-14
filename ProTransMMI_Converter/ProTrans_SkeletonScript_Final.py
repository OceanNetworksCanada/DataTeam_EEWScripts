# -*- coding: utf-8 -*-
"""
MMI Conversion Script - Skeleton

This script is the main mathematics behind converting the JMA stream to an MMI
value and plotting it to a graph.

This is not as visually pleasing as a full GUI but the intention is to have
the functions of this script easily incorporated into the main GUI application
or other applications as needed. Demo to follow.

Variables:
    -token: String variable for the Oceans2.0 user token
            This is found by making an acount to ONCs Oceans2.0 at:
                https://data.oceannetworks.ca/home
            From here, go to the users profile in the upper right corner, then
            clicking on Web Services API. From there, copy the 32 digit code
            and replace the 'INSERT YOUR TOKEN HERE' (if not already done)
            Oceans2.0 tokens are unique to each individual user's account. Be
            aware that if you refresh the token on your account, it will need
            to be updated here.
            
    -lastT: String variable that contains the last timestamp of retrieved data
            Starts by getting 20 seconds of data. This can be changed by
            changing the '20' in the string to the desired number of seconds
            
    -first: Boolean variable to check if this is the first iteration/new
            iteration.
    
    -count: Counter variable for how many refreshes have occured
    
    -its:   Number of iterations until new CSV file is written
    
    -interval: Interval (in milliseconds) to refresh the stream and get new
               data
               This can be changed depending on your internet connection.
               During testing, 20s (20000) was optimal due to poor home
               internet connection.
               Do not go less than 1s (1000). The app in its current state
               requests the most recent data from our system and then downloads
               that stream. JMAs (currently) are updated every 1s so there is
               no need to go faster.
     
    -csvName: String variable to hold the name of the CSV file. This is set to
              be the time of the first data entry + '_StartTimeMMILog.csv'.
              CSV files will be saved to the parent directory of the script.
              
Outputs:
    -matplotlib animated plot with the JMA value on the top (cm/s/s) and the
     converted MMI value on the bottom
     
    -timestamped (UTC) CSV files written to the parent directory
    
Notes:
    -To stop the script, simply close the figure window
    -This is a prototype function that works with our current Oceans2.0 data.

@author: Jacob Kukovica, Scientific Data Specialist, Ocean Networks Canada
"""

#%% Import Python Modules

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import requests
import datetime
from pandas import DataFrame

#%% Retrieve Data from Oceans2.0
# get a token (account from Oceans2.0)

token = 'INSERT YOUR TOKEN HERE'

devCode = 'PUT DEVICE CODE HERE'

#%% Define Plot
fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

#%% Define global/control variables
global lastT, first, count, its, csvName
lastT = '-PT20S' #  Only change the digit (20) for more/less initial data
first = True     
count = 0       
its = 2          #  Can be changed by user. Default = 2 
interval = 20000 #  Can be changed. Default = 20000. Do not go lower than 1000
csvName = ''

#%% Main Matplotlib Plot Animation Function
def animate(i):
        global lastT, first, count, its, csvName
        url = ('https://data.oceannetworks.ca/api/rawdata?method=getByDevice&'
       'deviceCode=' + devCode + '&'+
       'token='+token+'&dateFrom='+lastT)
        count += 1

        #   Gets data from URL of sepecific instrument deviceCode
        r = requests.get(url)
        
        if r.status_code ==200:
            results = r.json()
        
        #   Remove the JMA lines from Data and Convert
        jmaLines = [s for s in results['data']['readings'] if "JMA Intensity" in s]
        
        times_New = []
        jma_New = []
        mmi_New = []
        
        
        for sub in jmaLines:
            times_New.append(sub[:sub.find(' ')])
            temp_jma = sub[sub.rfind(' ')+1:]
            mmi_con = 2.1*np.log10(float(temp_jma)*100) + 2.3 # MMI conversion factor
            jma_New.append(float(temp_jma))
            mmi_New.append(mmi_con)
        
        lastT = datetime.datetime.strptime(times_New[-1],'%Y%m%dT%H%M%S.%fZ').strftime('%Y-%m-%dT%H:%M:%S.%f')
        lastT = lastT[:-3] + 'Z'
        
        timeAxis = np.arange(0,len(times_New),1)
            
        #%% Plot the results
        ax1.cla()
        ax1.plot(timeAxis, jma_New)
        ax1.set_xlabel('Time')
        ax1.set_ylabel('JMA (cm/s/s)')
        ax1.grid(True)
        ax2.cla()
        ax2.plot(timeAxis, mmi_New)
        ax2.set_xlabel('Time')
        ax2.set_ylabel('MMI')
        ax2.grid(True)
        
        fig.suptitle("JMA to MMI Conversion from " + times_New[0] + " to " + times_New[-1])
        
        print(times_New)
        
        #%% Writes data to CSV logs
        
        #   Makes new file
        if first == True:
            namer = datetime.datetime.strptime(times_New[0],'%Y%m%dT%H%M%S.%fZ').strftime('%Y_%m_%dT%H_%M_%S')
            csvName = namer + '_StartTimeMMILog.csv'
            data = [times_New, jma_New, mmi_New]
            df = DataFrame(data).transpose()
            df.columns = ['Time (UTC)', 'JMA (cm/s/s)', 'MMI']
            df.to_csv(csvName, index = False, header = True)
            first = False
            if count == its:
                first = True
                count = 0
                
        #   Checks if making a new file or appending to old
        elif first == False:
            times_New.pop(0)
            jma_New.pop(0)
            mmi_New.pop(0)
            data = [times_New, jma_New, mmi_New]
            df = DataFrame(data).transpose()
            df.to_csv(csvName, mode = 'a', index = False, header = False)
            if count == its:
                first = True
                count = 0

#%% Run Animated Figure            
ani = animation.FuncAnimation(fig, animate, interval = interval)
plt.show()    

    
 