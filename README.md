# DataTeam_EEWScripts
Collection of scripts used by the data team to monitor the EEW system or seismic data. Additional scripts for ONC internal employees can be found on Confluence.

# DMASMonitorCheck_V2
Sick of seeing all of the DMAS alerts and don't want to sift through the red table of death just to see what has changed? This application will look at each email that comes out daily and check what the update from the previous day was. Additionally, this can look at the EEW alert emails that come from the Event Maintenance page if a user follows it.

# IRIS_Live
Application that looks at near real time data streams (~5-10s delay depending on the internet connection) and calculates what the dip of an instrument is. This works using accelerometer channels from the instrument. A log of the changing dips is then printed to text file in the parent directory.

# ProTransMMI_Converter
This looks at taking the JMA heartbeat in near-real time for the Titan sensor located at the ProTrans station and converts the value to MMI based on a log linear conversion factor. This can be adapted to any JMA sensor name.

# SlackEEWAlerterApp_Apocolypto
Meet Apocolypto_bot (Yes I know the spelling is wrong). Him and his brother, Detecto_bot monitor, the WARNApiClient for when there is a CAP message issued from the correlator. When that message is recieved, these bots will send a Slack message to the ONC_Data and ONC_Main Slack environments, respectively. This will include a breakdown of useful information from the CAP message and an interactive HTML map showing where the event happened. These messages are processed quickly and are released generally 2 minutes before an email and will include any updates as more data is fed into the correlator.
