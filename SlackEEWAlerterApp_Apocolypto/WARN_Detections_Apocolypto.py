# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:21:19 2020


@author: jacob
"""

from onc.onc import ONC
from datetime import datetime, timedelta
import requests
import re
import pytz

import os
import time

import folium

from selenium import webdriver


from slacker import Slacker

from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, HTMLBody, FileAttachment


#   Assign credentials for email account. Include '@uvic.ca' in username and smtp address
creds = Credentials(username = 'EMAIL TO DISTRIBUTE ALERTS FROM',password = 'Password')
a = Account(primary_smtp_address='SAME EMAIL ABOVE',credentials=creds,autodiscover = True, access_type = DELEGATE)


onc = ONC("USER_ONC_TOKEN")
slackToken = 'ONC_Data_SlackApp_Token '
slackToken_ONC = 'ONC_Main_SlackApp_Token '

slack_client = Slacker(slackToken)
slack_client_ONC = Slacker(slackToken_ONC)

os.makedirs("_Maps", exist_ok = True)

#   Get the main directory of the application
curdir = os.getcwd()


#   Get the most recent log in EventMaintenance
url='EventMaintenanceMostRecent_url"

response = requests.get(url)
data = response.json()

#   Unpack the HTML. Get relevant time stamps
payloadNow = data['payload']['records'][0]['payload']
detectionID = data['payload']['records'][0]['eventDetectedId']
issueTime = data['payload']['records'][0]['timestamp']
capid = payloadNow[(payloadNow.rfind('capId=')+6):payloadNow.rfind(', Epicentre')]
capid = capid[(capid.rfind('-')+1):]

stFrnt = payloadNow[(payloadNow.find('[{OriginTime=')+13):]        
updateOriginTime = int(stFrnt[:stFrnt.find(', m')])

#   Save the recent event to a file
with open(curdir + "/_Maps/1_StartID_2_OriginTime.txt",'w') as starts:
    starts.write(str(detectionID))
    starts.write("\n")
    starts.write(str(updateOriginTime))
    starts.write('\n')
    starts.write(capid)

print("The program has started. Most recent event ID: " + str(detectionID) + ". Origin on: " + str(updateOriginTime) + ". Awaiting quake...")

#   Get initial check on the RunLog

rls = os.stat(curdir + "/RunLog.txt")[8]


#   Base map
ma = folium.Map(tiles = "Stamen Terrain")
ma.fit_bounds([(46,-131.75),(52.2,-123)])
folium.Rectangle([(46,-131.75),(52.2,-123)], popup = folium.Popup("WARN Detection Boundary")).add_to(ma)

while True:
    #   Check if the RunLog file is changed
    rlc = os.stat(curdir + "/RunLog.txt")[8]

    
    if rlc != rls:
        #   Update rls
        rls = rlc
        
        time.sleep(1)
        
        #   Parse WARN API Payload XML
        with open(curdir + "/RunLog.txt", 'r') as wl:
            warn_payload = wl.read()
            
        warn_recent = warn_payload[(warn_payload.rfind('<?xml')):warn_payload.rfind('</alert>')+8]
        
        originDate = int(warn_recent[(warn_recent.rfind('<valueName>OriginTime</valueName>')+47):(warn_recent.rfind('<valueName>OriginTime</valueName>')+51)])
        
        g = str(datetime.now())
        
        if originDate == 2018:
            print("New Detection. Daily test event for " + str(g) + ". Ignoring and awaiting quake...")
        
        elif originDate != 2018:        
            #   Get event log info
            response = requests.get(url)
            data = response.json()
    
            #   Unpack the HTML. Get relevant time stamps
            payloadNow = data['payload']['records'][0]['payload']
            detectionID = data['payload']['records'][0]['eventDetectedId']
            issueTime = data['payload']['records'][0]['timestamp']
            capid = payloadNow[(payloadNow.rfind('capId=')+6):payloadNow.rfind(', Epicentre')]
            capid = capid[(capid.rfind('-')+1):]
            
            sender = warn_recent[(warn_recent.rfind('<sender>')+8):(warn_recent.rfind('</sender>'))]
            
            alert_ident = warn_recent[(warn_recent.rfind('<identifier>')+12):(warn_recent.rfind('</identifier>'))]
            alert_ident = alert_ident[(alert_ident.rfind('-')+1):]
            
            #   Empty dictionary for epicenter detected stations
            StatLocals = {}
            
            print("New Detection: " + str(detectionID))
            print("Issue Time: " + issueTime + ". Currently Processing...")
        
            #   Get data
            stFrnt = payloadNow[(payloadNow.find('[{OriginTime=')+13):]        
            stOriginTime = int(stFrnt[:stFrnt.find(', m')])
            
            ReformatOr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stOriginTime/1000))
            
            #   Get the timezones
            pst = pytz.timezone('Canada/Pacific')
            utc = pytz.timezone('UTC')
        
            #   Make datetimes
            orPDT = datetime.strptime(ReformatOr, '%Y-%m-%d %H:%M:%S')
            issueUTC = datetime.strptime(issueTime, '%Y-%m-%dT%H:%M:%S.%fZ')
            
            dif_utc_pst = (utc.utcoffset(orPDT) - pst.utcoffset(orPDT))

            orUTC = orPDT + timedelta(seconds = dif_utc_pst.total_seconds())
            issuePST = issueUTC - timedelta(seconds = dif_utc_pst.total_seconds())        
            
            dfrom = datetime.strftime(orUTC - timedelta(minutes = 1), '%Y-%m-%dT%H:%M:%S.000Z')
            dto = datetime.strftime(orUTC, '%Y-%m-%dT%H:%M:%S.000Z') 
            
            #   Check if false event
            t = issueUTC - orUTC
            detectType = True
            
            
            if t > timedelta(seconds = 120):
                FalseTag = "FALSE DETECTION SUSPECTED! Difference between Origin and Issue times = " + str(t)
                detectType = False
            
            #   Get stations
            stSens = stFrnt[(stFrnt.find('Sensors=[')+9):stFrnt.find('], M')]
            
            #   Get magnitude
            stMag = stFrnt[(stFrnt.find('Magnitude=')+10):stFrnt.find(', c')]
    
            #   Get epicenter
            stEpi = stFrnt[(stFrnt.find('Epicentre=')+10):stFrnt.find('}]')]
            
            
            #   Make Detection Tag
            if capid not in alert_ident:
                updateOriginTime = stOriginTime
                tag = "DETECTION - NEW EVENT"
            elif capid in alert_ident:
                tag = "DETECTION - UPDATE TO " + ReformatOr + " (PST) Event"
            
            #   Update text file
            with open(curdir + "/_Maps/1_StartID_2_OriginTime.txt",'w') as starts:
                starts.write(str(detectionID))
                starts.write("\n")
                starts.write(str(stOriginTime))
                starts.write("\n")
                starts.write(alert_ident)
           
            #   Find stations
            #   Maps the stations to a list
            stationList = list(map(int, re.findall(r'\d+',stSens)))
            
            #   Gets the station information for the dictionary
            for stat in stationList:
                filters = {'deviceId': str(stat)}
                
                try:
                    result = onc.getLocations({'deviceCode': (onc.getDevices(filters))[0]['deviceCode'],
                                               'dateFrom' : dfrom,
                                               'dateTo' : dto})
                    detect = {stat : {"lat" : result[0]['lat'],
                                      "lon" : result[0]['lon'],
                                      "name": result[0]['locationCode']}}
                    StatLocals.update(detect)
                except:
                    continue
            
            #   Determine and mark epicenter
            lat, lon = stEpi.split(',')
            lat = float(lat)
            lon = float(lon)
            
            folium.Marker(location = [lat, lon],
                  popup = folium.Popup("Epicenter: " + str(lat) + ", " + str(lon) + "\nMagnitude: " + stMag),
                  icon = folium.Icon(color = 'red')).add_to(ma)
            
            statDetect = "Detection Stations: "
            
            cnt = 0
            
            #   Determine and mark detection stations
            for key in range(len(stationList)):
                if cnt == 0:
                    try:
                        folium.Marker(location = [StatLocals[stationList[key]]['lat'],StatLocals[stationList[key]]['lon']],
                                      popup = folium.Popup("Station: " + StatLocals[stationList[key]]['name'] + ". Location: " + str(StatLocals[stationList[key]]['lat']) + ", " + str(StatLocals[stationList[key]]['lon'])),
                                      icon = folium.Icon(color = 'blue')).add_to(ma)
                        statDetect += StatLocals[stationList[key]]['name'] + " (" + str(stationList[key]) + ")"
                        cnt = 1
                    except:
                        statDetect += "PNSN Station " + str(stationList[key])
                        cnt = 1
                elif cnt == 1:
                    try:
                        folium.Marker(location = [StatLocals[stationList[key]]['lat'],StatLocals[stationList[key]]['lon']],
                                      popup = folium.Popup("Station: " + StatLocals[stationList[key]]['name'] + ". Location: " + str(StatLocals[stationList[key]]['lat']) + ", " + str(StatLocals[stationList[key]]['lon'])),
                                      icon = folium.Icon(color = 'blue')).add_to(ma)
                        statDetect += ", " + StatLocals[stationList[key]]['name'] + " (" + str(stationList[key]) + ")"
                    except:
                        statDetect += ", PNSN Station " + str(stationList[key])
                    
            
            location = curdir + '/_Maps/' + 'Map' + issueUTC.strftime('%Y-%m-%d T%H_%M_%S') + '.html'
            location_png = curdir + '/_Maps/' + 'Map' + issueUTC.strftime('%Y-%m-%d T%H_%M_%S') + '.png'
            
            ma.save(location)
            
            #   Creates a PNG file to go along with the HTML
            browser = webdriver.Chrome("C:/Users/jkukovic/WARN_API_CLIENT/chromedriver.exe") #  Update to parent directory containing the ChromeDriver
            browser.get(location)
            
            time.sleep(3)
            browser.save_screenshot(curdir + '/_Maps/' + 'Map' + issueUTC.strftime('%Y-%m-%d T%H_%M_%S') + '.png')
            browser.quit()
            
            #   Form text messages
            mag_epi = "Magnitude: M" + stMag + ". Epicenter: " + str(lat) + ", " + str(lon)
            iss_time = "Issue Time: "+ issueUTC.strftime('%Y-%m-%d, %H:%M:%S') + " (UTC). " + issuePST.strftime('%Y-%m-%d, %H:%M:%S') + " (PST)"
            or_time = "Origin Time: "+ orUTC.strftime('%Y-%m-%d, %H:%M:%S') + " (UTC). " + orPDT.strftime('%Y-%m-%d, %H:%M:%S') + " (PST)"
            issuer = "Correlator Issuer: " + sender
            
            if detectType == True:
                mesg = tag + "\n \n" + mag_epi + "\n \n" + or_time + "\n \n" + iss_time + "\n \n" + statDetect + "\n \n" + issuer
            elif detectType == False:
                mesg = FalseTag + "\n \n" + mag_epi + "\n \n" + or_time + "\n \n" + iss_time + "\n \n" + statDetect + "\n \n" + issuer
                tag = "[DETECTION - POTENTIAL FALSE]"            
    
            slack_client.files.upload(channels = "#earthquake_alerts",
                            file_ = location_png,
                            filename = 'Map ' + issueUTC.strftime('%Y-%m-%d T%H_%M_%S'),
                            initial_comment = mesg,
                            filetype = "png")
            
            slack_client_ONC.files.upload(channels = "#earthquake_warn_detections",
                            file_ = location_png,
                            filename = 'Map ' + issueUTC.strftime('%Y-%m-%d T%H_%M_%S'),
                            initial_comment = mesg,
                            filetype = "png")
            print("Slack sent 1/2")
            
            slack_client.files.upload(channels = "#earthquake_alerts",
                            file_ = location,
                            filename = location,
                            initial_comment = "Download and open the following HTML document for an interactive map",
                            filetype = "html")
            slack_client_ONC.files.upload(channels = "#earthquake_warn_detections",
                            file_ = location,
                            filename = location,
                            initial_comment = "Download and open the following HTML document for an interactive map",
                            filetype = "html")
            print("Slack sent 2/2. Done. Sending emails...")
            
            
                    #   Grab the saved image for the email    
            with open(location, "rb") as fp:
                map_attach = FileAttachment(name = location, content = fp.read())
            
            #   Constructs the response email body
            
            if detectType == True:
                tit = HTMLBody('<html><body><p>' + iss_time + '</p><p>' + or_time + '</p><p>' + mag_epi + '</p><p>' + issuer + '</p><p>' + statDetect + '</body></html>')
                tit2 = HTMLBody('<html><body><p>' + iss_time + '</p><p>' + or_time + '</p><p>' + mag_epi + '</body></html>')
            else:
                tit = HTMLBody('<html><body><p>' + FalseTag + '</p><p>' + iss_time + '</p><p>' + or_time + '</p><p>' + mag_epi + '</p><p>' + issuer + '</p><p>' + statDetect + '</body></html>')
                tit2 = HTMLBody('<html><body><p>' + FalseTag + '</p><p>' + iss_time + '</p><p>' + or_time + '</p><p>' + mag_epi + '</body></html>')
            #   Composes change email to return (can go to any email)
            m = Message(
                account=a,
                subject = tag + " M" + stMag + ". " + iss_time,
                body = tit,
                to_recipients = [Mailbox(email_address='Email#1'),
                                 Mailbox(email_address='Email#2'),
                                 Mailbox(email_address='Email#3'),
                                 ....]
]
                )
            m.attach(map_attach)
            
#            #   Send away!
            m.send()
            
            print("Emails sent. Awaiting next quake")
            
            
            #   clear old map and make new Base map
            del ma
            
            ma = folium.Map(tiles = "Stamen Terrain")
            ma.fit_bounds([(46,-131.75),(52.2,-123)])
            folium.Rectangle([(46,-131.75),(52.2,-123)], popup = folium.Popup("WARN Detection Boundary")).add_to(ma)
            

