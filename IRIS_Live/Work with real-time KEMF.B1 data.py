#!/usr/bin/env python
# coding: utf-8

# In[48]:


import numpy as np
from obspy.clients.fdsn import Client
from obspy import UTCDateTime, Stream, read
import datetime
from datetime import time
client = Client("IRIS")
# get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# In[95]:

    
x = np.arange(0, 7, 0.01)




gettimeNow = datetime.datetime.now()
    
t_start = str((gettimeNow-datetime.timedelta(seconds=1)).date())+'T'+str((gettimeNow-datetime.timedelta(seconds=1)).time())
t = str(gettimeNow.date())+'T'+str(gettimeNow.time())



urlpars = "http://service.iris.edu/irisws/timeseries/1/query?net=NV&sta=KEMF&cha=MNZ&start=2020-08-26T00:00:00&end=2020-08-26T00:01:00&scale=AUTO&format=miniseed&loc=B1"
urlpar1 = "http://service.iris.edu/irisws/timeseries/1/query?net=NV&sta=KEMF&cha=MNZ&start=2020-08-26T00:00:00&end=2020-08-26T00:01:00&scale=AUTO&format=miniseed&loc=B1"
urlpar2 = "http://service.iris.edu/irisws/timeseries/1/query?net=NV&sta=KEMF&cha=MNZ&start=2020-08-26T00:00:00&end=2020-08-26T00:01:00&scale=AUTO&format=miniseed&loc=B1"


ts = urlpars[:urlpars.find('start=')]
te = urlpars[(urlpars.rfind('&end=') + 24):]



timestring = 'start=' + t_start + '&end=' + t


chans = [(urlpars[urlpars.find('cha=')+4:])[0:3],(urlpars[urlpars.find('cha=')+4:])[0:3],(urlpars[urlpars.find('cha=')+4:])[0:3]]

test = [[(urlpars[urlpars.find('cha=')+4:])[0:3],(urlpars[urlpars.find('cha=')+4:])[0:3]],[(urlpars[urlpars.find('cha=')+4:])[0:3],(urlpars[urlpars.find('cha=')+4:])[0:3]]]

# url = 'http://service.iris.edu/irisws/timeseries/1/query?net=NV&sta=KEMF&cha='+'MNZ'+'&start='+t_sgraph+'&end='+t+'&scale=AUTO&format=miniseed&loc=B1'
# stg.append(read(url)[0])
# print('MNZ')
# url = 'http://service.iris.edu/irisws/timeseries/1/query?net=NV&sta=KEMF&cha='+'MNN'+'&start='+t_sgraph+'&end='+t+'&scale=AUTO&format=miniseed&loc=B1'
# stg.append(read(url)[0])
# print('MNN')
# url = 'http://service.iris.edu/irisws/timeseries/1/query?net=NV&sta=KEMF&cha='+'MNE'+'&start='+t_sgraph+'&end='+t+'&scale=AUTO&format=miniseed&loc=B1'
# stg.append(read(url)[0])
# print('MNE')     

# t_start = t
# t = str(datetime.datetime.now().date())+'T'+str(datetime.datetime.now().time())

# t_del = datetime.timedelta(datetime.strptime(t,'%y-%m-%dT%HH:%MM:%SS.%f')-datetime.strptime(t_start,'%y-%m-%dT%HH:%MM:%SS.%f'))
# print(t_del)

# retrieving corrected data from IRIS for the last 10 minutes for KEMF.B1 MN channels

st = Stream()

for i in range(2):
    
    
    gettimeNow = datetime.datetime.now()
    
    t_start = str((gettimeNow-datetime.timedelta(seconds=1)).date())+'T'+str((gettimeNow-datetime.timedelta(seconds=1)).time())
    t = str(gettimeNow.date())+'T'+str(gettimeNow.time())
    
    timestring = 'start=' + t_start + '&end=' + t
    
    
    print(datetime.datetime.now())
    print(t_start)
    print(t)

    

    url = 'http://service.iris.edu/irisws/timeseries/1/query?net=NV&sta=KEMF&cha='+'MNZ'+'&start='+t_start+'&end='+t+'&scale=AUTO&format=miniseed&loc=B1'
    st.append(read(url)[0])
    print('MNZ')
    url = 'http://service.iris.edu/irisws/timeseries/1/query?net=NV&sta=KEMF&cha='+'MNN'+'&start='+t_start+'&end='+t+'&scale=AUTO&format=miniseed&loc=B1'
    st.append(read(url)[0])
    print('MNN')
    url = 'http://service.iris.edu/irisws/timeseries/1/query?net=NV&sta=KEMF&cha='+'MNE'+'&start='+t_start+'&end='+t+'&scale=AUTO&format=miniseed&loc=B1'
    st.append(read(url)[0])
    print('MNE')     


    
    
    Zchan = np.mean(st.select(channel=chans[0])[0].data)
    Nchan =  np.mean(st.select(channel=chans[1])[0].data)
    Echan =  np.mean(st.select(channel=chans[2])[0].data)
    
    
    g = np.sqrt(Zchan**2+Nchan**2+Echan**2)
    
    
    
    
    
    # current angles for channels
    alpha_N = np.arcsin(Nchan/g)*180/np.pi
    alpha_E = np.arcsin(Echan/g)*180/np.pi
    alpha_Z = np.arccos(Zchan/g)*180/np.pi
    print(alpha_Z,alpha_E,alpha_N)
    
    degS = u"\u00b0"
    
    fig, (ax1, ax2, ax3) = plt.subplots(3,1,subplot_kw=dict(polar=True))
    
    ax1.plot(0,1)
    ax1.arrow(float(alpha_Z)/180*np.pi,0,0,0.82,
                          width = 0.05, edgecolor = 'black', facecolor = 'blue', lw = 2, zorder = 2)
    ax1.set_theta_direction(-1)
    ax1.set_theta_zero_location("E")
    ax1.set_thetamin(-90)
    ax1.set_thetamax(90)
    ax1.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
    ax1.set_yticklabels([])
    ax1.set_title("Dip", pad = 20, size = 18)
    ax1.set_xticklabels(['-90'+degS + '\n(Up)','-75'+degS,'-60'+degS,'-45'+degS,'-30'+degS,'-15'+degS,'0'+degS + "\n(Seafloor)",'15'+degS,'30'+degS,'45'+degS,'60'+degS,'75'+degS,'90'+degS +'\n(Down)'], size = 10)
    
    ax2.plot(0,1)
    ax2.arrow(float(alpha_N)/180*np.pi,0,0,0.82,
                          width = 0.05, edgecolor = 'black', facecolor = 'blue', lw = 2, zorder = 2)
    ax2.set_theta_direction(-1)
    ax2.set_theta_zero_location("E")
    ax2.set_thetamin(-90)
    ax2.set_thetamax(90)
    ax2.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
    ax2.set_yticklabels([])
    ax2.set_title("Dip", pad = 20, size = 18)
    ax2.set_xticklabels(['-90'+degS + '\n(Up)','-75'+degS,'-60'+degS,'-45'+degS,'-30'+degS,'-15'+degS,'0'+degS + "\n(Seafloor)",'15'+degS,'30'+degS,'45'+degS,'60'+degS,'75'+degS,'90'+degS +'\n(Down)'], size = 10)
    
    ax3.plot(0,1)
    ax3.arrow(float(alpha_E)/180*np.pi,0,0,0.82,
                         width = 0.05, edgecolor = 'black', facecolor = 'blue', lw = 2, zorder = 2)
    ax3.set_theta_direction(-1)
    ax3.set_theta_zero_location("E")
    ax3.set_thetamin(-90)
    ax3.set_thetamax(90)
    ax3.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
    ax3.set_yticklabels([])
    ax3.set_title("Dip", pad = 20, size = 18)
    ax3.set_xticklabels(['-90'+degS + '\n(Up)','-75'+degS,'-60'+degS,'-45'+degS,'-30'+degS,'-15'+degS,'0'+degS + "\n(Seafloor)",'15'+degS,'30'+degS,'45'+degS,'60'+degS,'75'+degS,'90'+degS +'\n(Down)'], size = 10)
    
    st.plot()
    
    r = st.plot()
    
    m = Figure()

    rs = plt.figure()

    t_start = t
    t = str(datetime.datetime.now().date())+'T'+str(datetime.datetime.now().time())
    
    
    
    
    
    
    
    # plt.clf()
    # ax1 = fig.add_subplot(121, projection = 'polar')
    # ax1.plot(0,1)
    # ax1.arrow(float(r['values'][18])/180*np.pi,0,0,0.82, 
    #           width = 0.05, edgecolor = 'black', facecolor = 'blue', lw = 2, zorder = 2)
    # ax1.set_theta_zero_location("N")
    # ax1.set_theta_direction(-1)
    # ax1.set_yticklabels([])
    # ax1.set_title("Azimuth", pad = 20, size = 18)
    
    # ax2 = fig.add_subplot(122, projection = 'polar')
    # ax2.plot(0,1)
    # ax2.arrow(float(r['values'][19])/180*np.pi,0,0,0.82,
    #           width = 0.05, edgecolor = 'black', facecolor = 'blue', lw = 2, zorder = 2)
    # ax2.set_theta_direction(-1)
    # ax2.set_theta_zero_location("E")
    # ax2.set_thetamin(-90)
    # ax2.set_thetamax(90)
    # ax2.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
    # ax2.set_yticklabels([])
    # ax2.set_title("Dip", pad = 20, size = 18)
    # ax2.set_xticklabels(['-90'+self.degS + '\n(Up)','-75'+self.degS,'-60'+self.degS,'-45'+self.degS,'-30'+self.degS,'-15'+self.degS,'0'+self.degS + "\n(Seafloor)",'15'+self.degS,'30'+self.degS,'45'+self.degS,'60'+self.degS,'75'+self.degS,'90'+self.degS +'\n(Down)'], size = 10)
    # fig.canvas.draw()
    

    # fig = plt.figure(figsize = (int(w*0.4/96),int(h*0.6/96)))
    # ax1 = fig.add_subplot(121, projection = 'polar')
    # ax1.plot(0,1)
    # ax1.set_theta_zero_location("N")
    # ax1.set_theta_direction(-1)
    # ax1.set_yticklabels([])
    # ax1.set_title("Azimuth", pad = 20, size = 18)
    
    # ax2 = fig.add_subplot(122, projection = 'polar')
    # ax2.plot(0,1)
    # ax2.set_theta_direction(-1)
    # ax2.set_theta_zero_location("E")
    # ax2.set_thetamin(-90)
    # ax2.set_thetamax(90)
    # ax2.set_xticks(np.linspace((-1*(np.pi))/2,(np.pi)/2, 13))
    # ax2.set_yticklabels([])
    # ax2.set_title("Dip", pad = 20, size = 18)
    # ax2.set_xticklabels(['-90'+self.degS + '\n(Up)','-75'+self.degS,'-60'+self.degS,'-45'+self.degS,'-30'+self.degS,'-15'+self.degS,'0'+self.degS + "\n(Seafloor)",'15'+self.degS,'30'+self.degS,'45'+self.degS,'60'+self.degS,'75'+self.degS,'90'+self.degS +'\n(Down)'], size = 10)
    
