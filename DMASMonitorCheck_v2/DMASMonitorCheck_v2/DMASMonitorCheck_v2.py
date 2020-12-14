"""
 -*- coding: utf-8 -*-

Created on Mon Nov 18 18:02:58 2019

@author: Jacob Kukovica; jkukovic@uvic.ca

DMAS Monitor Check - Version 2

Tired of those big DMAS emails cluttering your inbox? Too lazy to read through
the whole table to see if there was a change in the systems? Well this code is
for you!!!

DMASMonitorCheck_v1.py is programmed to log into your UVIc email, read the latest
DMAS alert that was received (be it File Archiving warning or Data Monitoring
warning) and compare it to the previous email that was received. If you have a
backlog of these emails, it is programmed to start from the beginning and give
you all the differences between all the emails that are put into a specific
folder.

Once 2 emails have been compared, the code will send you an email with the
subject that says if it was from a "File Archiving" or "Data Monitoring" warning
and the date/time of the previous alert email. For example, a subject may read:
    
    [MONITOR] DMAS Alert Change from: 2019-11-19 13:22:57

The email will be sent directly to your inbox and the DMAS Alert email will be
marked as read. The body of the email will contain a table with the
differences between the 2 newest emails. THIS WILL NOT TELL YOU IF A DEVICE WAS
ADDED OR REMOVED!!! IT WILL ONLY TELL THE DIFFERENCE!!!

As a help, a line of text before the table will say if the change was +ve, -ve,
or 0. +ve results hint to a device being added to the list, -ve hint to device
being removed and back on line, 0 hints to no change. This is only a hint! Say
we had 2 devices added and 2 removed, the result would be 0 but there would be
4 stations recorded as different. Manual checking would then be necessary.
    
EXTERNAL SET UP IN OUTLOOK AND/OR TASK MANAGER
    
For this code to run effectively (and more autonomously), there are a few
things that need to be established in Outlook and Task Manager:

    1.   Create 3 subfolders in the inbox of your UVIc email:
         - DMAS Alerts
         - DMAS Alerts - Archive
         - DMAS Alerts - Monitoring
         
         The code is meant to check the DMAS Alert folder to see if there was a
         new alert from either alert system. If there is no new email in that
         folder, the code just exits. If there is a new email, it will move it
         into the respective Monitor or Archive folder and do the comparison
         with the emails within that folder. The code could technically work by
         reading the emails in your inbox instead of the DMAS Alert folder,
         but this was done for reading efficiency and ensuring no alert is
         missed.
         
     2.  Set a rule to look for emails from either alert system in Outlook. The
         rule should be set to:
         - Apply this rule after the message arrives
           from dmas@ncmon.neptune.uvic.ca
              and with 'File Archiving Alert' or 'Data Monitoring Alert' in the
              subject
           move it to the 'DMAS Alerts' folder
           
     3.  Set either a rule or an automated task to run the script.
     
         Technically, this code could run in Outlook with a VBA script that 
         opens Python and runs the code after the previous rule moves it to the
         DMAS Alerts folder; however, my VBA coding is terrible and
         all the tutorials in the internet couldn't get this to work for me.
         This would be the ideal set up to have. Simply add a rule line that
         says 'run a script' after the email is moved and all good to go.
         
         With this not working, you can have a Windows Task in Task Manager run
         the python script on a schedule whenever you want. This is what I have
         done; however, this may be modified seeing as I noticed the emails
         always arrive around 5:26 AM PST. So for efficiency, the task can be
         set to run all the time (logged in or not) every 10 minutes between
         5 AM and 6 AM. Or something like that.
         
         Because this will be running Python in the Command Prompt, ensure that
         Python is installed specifically in Windows (not just Anaconda or
         Spyder) and the listed modules are installed.

With all that said, have fun!
"""


#Version 2:
#    -adds functionality of looking for WARN Earthquake detections and 
#        reformatting the email to give the user more of a ShakeAlert esque
#        email.
#        
#    REQUIRES RUN UPDATE TO WORK WITH SCHEDULER!
#       -Add DMAS - WARN Detection folder in Inbox
#    
#    Like what was mentioned above, if your VBA skills are good enough to run
#    a bat file when you recieve an email (rule triggering) that is the fastest
#    and most optimal way to go.
#    
#    For this, ensure that you have downloaded into the python environment:
#        -ONC
#        -cartopy
#        -exchangelib
#        
#    Installing Cartopy:
#        This is a tricky software package to install because of
#        the requirement of GEOS and PROJ for the map making. The best way I
#        found is to install these packages is to:
#            1. Open into the Anaconda environment in the a conda prompt
#            2. Go conda install -c conda-forge basemap
#                -basemap is an obsolete package that cartopy is replacing but 
#                it streamlines the install process for the PROJ.4 and GEOS pack
#            3. Once those 2 packages are installed (need GEOS >=3.3.3 and PROJ >= 4.9.0),
#               pip install cartopy
#                   -if the above are installed properly, cartopy should install
#                   
#    Update the Task Scheduler option to run off of a .bat file:
#       This .bat file must be in the same directory as the DMASMonitorCheck_v2.py file        

#       .bat file format:
#        
#        -create a .bat file with the following
#            set root=C:\Users\[YourUserName]\AppData\Local\Continuum\anaconda3
#            call %root%\Scripts\activate.bat %root%
#            call conda activate [yourEnvironmentName]
#            python C:\Users\jkukovic\PythonScripts\DMASMonitorCheck_v2.py
#                    
#        - python call at the end is to the location and filename of this file
#                    
#        -create a task that runs this .bat file and ensure "Run with Highest Permissions" is selected
#        -Select to run daily every 5 mins to ensure a detection is caught
#        
#    Additional files:
#        -Move the script to the desired folder where it will run
#        -Create a '_Maps' folder in that location
#        -Move the attached EEW_Base.png image into that folder

#    Autorunning
#       Task scheduler doesn't like to send larger emails with attachments from the looks of it
#       My work around is to have the .bat file run in an infinite loop in the background of my computer (create a shortcut to the dektop then have it run 'minimized' infinitely).
#       Ideally, I plan to have this running on my computer at home to offset the processes this computer needs to do

#%%
#   Local imports
from bs4 import BeautifulSoup
from onc.onc import ONC
from datetime import datetime, timedelta
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt

import os
import time



import cartopy.crs as ccrs
import cartopy.crs as ccrs #    I know this is imported twice but it avoids errors for some reason when imported the second time



#   External install/import (pip install exchangelib)
from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, HTMLBody, FileAttachment



#   Assign credentials for email account. Include '@uvic.ca' in username and smtp address
creds = Credentials(username = '[username@uvic.ca]',password = '[YourEmailPassword]')
a = Account(primary_smtp_address='[YourFullUVIcEmail]',credentials=creds,autodiscover = True, access_type = DELEGATE) 


onc = ONC("[YourONCToken]")


"""
EmailChecker

Function for performing the comparison between old/new emails.
    Arguments:
        folder - The folder location for either the "DMAS Alerts - Archive" or
                 the "DMAS Alerts - Monitor" folder where comparison will be
                 performed.
                 
        tag    - String containing the "[ARCHIVE]" or "[MONITOR]" tag for the
                 return email subject line.
"""

def EmailChecker(folder,tag):
    #   Assign blank variables
    data_old = []
    data_new = []
    date_new = []
    date_old = []
    loop = 0
    
    
    #   Check if the new email is the first for the folder
    if folder.total_count > 1:
        t = 2
    elif folder.total_count <= 1:
        t = 1
        
    #   Sort the emails in the folder from newest to oldest and grab the 2
    #   most recent emails.
    for item in folder.all().order_by('-datetime_received')[:t]:
        data = []
        soup = BeautifulSoup(item.body,'lxml')  # Extracts email body/HTML text
        table = soup.table #    Finds the table contained in the body
        trows = table.find_all('tr') #  Reconstructs the table
        headerow = [td.get_text(strip=True) for td in trows[0].find_all('th')] # Grabs the header info
        if headerow: # if there is a header row, include first
            data.append(headerow)
            trows = trows[1:]
        for tr in trows: #  assigns each row to the table
            cols = tr.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        #   Grabs the new and old data to compare in a DataFrame
        if loop == 0:
            data_new = pd.DataFrame(data[1:],columns=data[0])
            date_new = item.datetime_sent
            if t == 1: # Makes blank DataFrame if this is the first email in the folder
                data_pass = pd.DataFrame(data[1:],columns = data[0])
                date_old = date_new
        elif loop == 1:
            data_old = pd.DataFrame(data[1:],columns=data[0])
            date_old = item.datetime_sent
        
        loop += 1
    # Determines the net change between the emails based on the number of rows
    netc = []    
    newsts = len(data_new)
    oldsts = len(data_old)
    
    
    #Determines the net change to give reference if its a sytem being added or removed
    if newsts < oldsts:
        netc = "Net Change = "+str([newsts-oldsts])+" Therefore most likely stations back online."
    elif newsts > oldsts:
        netc = "Net Change = "+str([newsts-oldsts])+". Therefore most likely more stations are off online."
    elif newsts == oldsts:
        netc = "Net Change = "+str([newsts-oldsts])+". Most likely no change."
    
    #   Compares the tables
    if t > 1: # Perform the comparison if there are more than 1 emails in the folder
        differ = pd.concat([data_new,data_old])
        differ = differ.reset_index(drop=True)
        
        differ_gpby = differ.groupby(list(differ.columns))
        
        idx = [x[0] for x in differ_gpby.groups.values() if len(x)==1]
        
        #   Puts the table in HTML for message
        dif = differ.reindex(idx)
        dif_html = pd.DataFrame.to_html(dif)
    elif t == 1:
        #   Assigns all values of emauil added if this is the first email
        dif_html = pd.DataFrame.to_html(data_pass)
        
    
    #   Constructs the response email body
    tit = HTMLBody("<html><body><p>"+netc+"</p>"+dif_html+"</body></html>")
    
    #   Composes change email to return (can go to any email)
    m = Message(
        account=a,
        subject = tag+"DMAS Alert Change from: "+str(date_old),
        body = tit,
        to_recipients = [Mailbox(email_address='jkukovic@uvic.ca')]
        )
    
    #   Send away!
    m.send()

"""
EmailChecker_WARN

Function for performing the comparison between old/new emails.
    Arguments:
        folder - The folder location for either the "DMAS Alerts - Archive" or
                 the "DMAS Alerts - Monitor" folder where comparison will be
                 performed.
                 
        tag    - String containing the "[ARCHIVE]", "[MONITOR]", or "[DETECTION]"
                 tag for the return email subject line.
                 
        curdir - Returns the current directory for file saving calls
"""



def EmailChecker_WARN(folder,tag,curdir):
    #   Get the folder
    
    #   Assign Blank Detection statistics dictionary
    DetectStats = {"Origin Time" : "",
                   "Issue Time" : "",
                   "Correlator Issuer" : "",
                   "Epicenter" : "",
                   "Magnitude" : ""}
    
    #   Empty dictionary for epicenter detected stations
    StatLocals = {}    
    
    #   Sort the emails in the folder from newest to oldest and grabs the most
    #   recent detection warning
    for item in folder.all().order_by('-datetime_received')[:1]:
        data = []
        soup = BeautifulSoup(item.body,'lxml')  # Extracts email body/HTML text
        
        parse = soup.text.split("\n")   # Extracts the body text
        
        #   Get the detection stats for the new email
        DetectStats["Origin Time"] = parse[parse.index("OriginTime") + 1]
        DetectStats["Issue Time"] = parse[3]
        DetectStats["Correlator Issuer"] = parse[2]
        DetectStats["Epicenter"] = parse[parse.index("Epicentre") + 1]
        DetectStats["Magnitude"] = parse[parse.index("Magnitude") + 1]
        
        #   Grab the most recent event from the detection list that is associated with the email
        url='https://data.oceannetworks.ca/EventDefinitionService?operation=12&eventDefinitionId=17&sort=timestamp&dir=desc&startIndex=0&results=60'
        response = requests.get(url)
        data = response.json()
        
        #   Unpack the HTML
        payloadNow = data['payload']['records'][0]['payload']
        
        #   Get the list of stations that was in the payload of the event list
        stFrnt = payloadNow[(payloadNow.find('Sensors=[')+9):]
        stsens = stFrnt[:stFrnt.find(']')]
        
        #   Maps the stations to a list
        stationList = list(map(int, re.findall(r'\d+',stsens)))
        
        #   Gets the station information for the dictionary
        for stat in stationList:
            filters = {'deviceId': str(stat)}
            result = onc.getLocations({'deviceCode': (onc.getDevices(filters))[0]['deviceCode']})
            detect = {stat : {"lat" : result[0]['lat'],
                              "lon" : result[0]['lon'],
                              "name": result[0]['locationCode']}}
            StatLocals.update(detect)
        
        #   Gets the event epicenter
        lat, lon = DetectStats['Epicenter'].split(',')
        lat = float(lat)
        lon = float(lon)
        
        #   Plots the base image onto the figure
        plt.figure(figsize = (9, 6))
        fname = curdir + '/_Maps/EEW_Base.png'
        
        img_extent = (-131.75, -123, 46, 52.2)
        img = plt.imread(fname)
        
        ax = plt.axes(projection = ccrs.Mercator())
        
        origin = datetime.strptime(DetectStats['Origin Time'], '%Y-%m-%dT%H:%M:%S+00:00')
        pst_origin = origin - timedelta(hours = 8)
        
        issue = datetime.strptime(DetectStats['Issue Time'], '%Y-%m-%dT%H:%M:%S+00:00')
        pst_issue = issue - timedelta(hours = 8)
        
        
        plt.title("Earthquake Occurred at: " + pst_origin.strftime('%Y-%m-%d, %H:%M:%S') + "(PST)\nMagnitude (M): " + DetectStats['Magnitude'] + ". Epicenter = " + DetectStats['Epicenter'])
        
        # set a margin around the data
        ax.set_xmargin(0.05)
        ax.set_ymargin(0.10)
        
        # add the base image
        ax.imshow(img, origin = 'upper', extent = img_extent, transform = ccrs.Mercator())
        ax.coastlines(resolution='10m', color='black', linewidth=1)
        
        #   Plot the epicenter
        ax.plot(lon, lat, 'k*', markersize=12, transform=ccrs.Mercator(), label = "Epicenter")
        ax.annotate("M"+ DetectStats['Magnitude'], (lon + 0.1, lat))
        
        #   Creates list of the detection stations for the email
        cnt = 0
        statDetect = "Detection Stations: "
        
        
        # mark detectionstations
        for key in StatLocals:
            if cnt == 0:
                ax.plot(StatLocals[key]['lon'], StatLocals[key]['lat'], 'r^', markersize=8, label = "Epicenter Detection Station", transform=ccrs.Mercator())
                ax.annotate(StatLocals[key]['name'], (StatLocals[key]['lon'], StatLocals[key]['lat']))
                statDetect += StatLocals[key]['name']
                cnt = 1
            else:
                ax.plot(StatLocals[key]['lon'], StatLocals[key]['lat'], 'r^', markersize=8, transform=ccrs.Mercator())
                ax.annotate(StatLocals[key]['name'], (StatLocals[key]['lon'], StatLocals[key]['lat']))
                statDetect += ", " + StatLocals[key]['name']
        ax.legend()
        
        location = curdir + '/_Maps/' + 'Map' + issue.date().strftime('%Y-%m-%d') + '.png'
        
        #   Save the figure
        plt.savefig(location)
    
    #   Grab the saved image for the email    
    with open(location, "rb") as fp:
        map_attach = FileAttachment(name = location, content = fp.read())

    #   Create strings for HTML body text
    cor_iss = "Correlator Issuer: " + DetectStats['Correlator Issuer']
    mag_epi = "Magnitude: M" + DetectStats['Magnitude'] + ". Epicenter: " + DetectStats['Epicenter']
    iss_time = "Issue Time: "+ issue.strftime('%Y-%m-%d, %H:%M:%S') + " (UTC). " + pst_issue.strftime('%Y-%m-%d, %H:%M:%S') + " (PST)"
    or_time = "Origin Time: "+ origin.strftime('%Y-%m-%d, %H:%M:%S') + " (UTC). " + pst_origin.strftime('%Y-%m-%d, %H:%M:%S') + " (PST)"


    
    #   Constructs the response email body
    tit = HTMLBody('<html><body><p>' + iss_time + '</p><p>' + or_time + '</p><p>' + mag_epi + '</p><p>' + cor_iss + '</p><p>' + statDetect + '</body></html>')
    
    #   Composes change email to return (can go to any email)
    m = Message(
        account=a,
        subject = tag + " M" + DetectStats['Magnitude'] + " Earthquake Warning Issued: " + pst_issue.strftime('%Y-%m-%d, %H:%M:%S') + " (PST)",
        body = tit,
        to_recipients = [Mailbox(email_address='jkukovic@uvic.ca')]
        )
    m.attach(map_attach)
    
    #   Send away!
    m.send()







"""

Main Code

"""


a.root.refresh() # Refresh the Outlook folder to ensure counts are correct
fold_strt = a.inbox // "DMAS Alerts" # Grabs the location of "DMAS Alerts"
time.sleep(3)

fold_strt.refresh()
time.sleep(3)

cnt = fold_strt.total_count # Check how many emails are in that folder

os.makedirs("_Maps", exist_ok = True)

#   Get the main directory of the application
curdir = os.getcwd()


if cnt !=0: 
    for totfol in range(1,cnt+1): # Run the code for however many new emails there are
        
        """
        Order emails from oldest to newest in DMAS Alerts to ensure the
        function being performed in the Monitor/Archive folder is on the next
        newest email from the previous. This is in case multiple alerts were
        put into the DMAS Alert folder from the same system.
        
        As long as the original emails are in the DMAS Alert folder, they will
        be marked as unread. Only when they get moved into Monitor/Archive
        do they get marked as read.
        """
        
        for item in fold_strt.all().order_by('datetime_received'):
            # Moves the email into respective Monitor/Archive/WARN folder
            if item.subject == "Data Monitoring Alert":
                fold_m = a.inbox // "DMAS Alerts - Monitor"
                item.move(fold_m)
                item.is_read = True # Marks as read only after it is sorted
                item.save() # Saves mark as read condition
                fold_m.refresh()
                tag = "[MONITOR] "
                EmailChecker(fold_m,tag) # Perform sort
            elif item.subject == "File Archiving Alert":
                fold_m = a.inbox // "DMAS Alerts - Archive"
                item.move(fold_m)
                item.is_read = True
                item.save()
                fold_m.refresh()
                tag = "[ARCHIVE] "        
                EmailChecker(fold_m,tag)
            elif item.subject == "WARN Earthquake Detection":
                fold_m = a.inbox // "DMAS - WARN Detection"
                item.move(fold_m)
                item.is_read = True
                item.save()
                fold_m.refresh()
                tag = "[DETECTION] " 
                EmailChecker_WARN(fold_m,tag,curdir)
            fold_strt.refresh() # Refresh DMAS Alert folder for email counts





    
