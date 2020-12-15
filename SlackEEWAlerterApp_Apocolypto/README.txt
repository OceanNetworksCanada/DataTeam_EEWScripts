Created by: Jacob Kukovica, Data Team, ONC

To run the EEW Alert Parser for Slack/Email:

1.	Ensure that Java is installed on the system to run the WARNNotificationApiClient.jar application

2.	Run this through the command line from the parent folder with the call:
		java -jar WarnNotificationApiClient.jar > RunLog.txt
	This will send the output to the RunLog text file which is monitored from the Python Script

3.	Set up the WARNNotificationApiClient.properties fields to have the notifications come from the server
		-This will need an ONC Token and the server port set up

4.	Run the Apocolypto.bat file to start the python monitor script (WARN_Detections_Apocolypto.py)
		-If it crashes, try restarting it and it should run the second time. It helps if the Python script is running first, then starting the Java script. The "crash" can happen if there is no RunLog.txt file present when the Python script is started or running.
		-This commandline window and the one running java notification client need to be running 24/7 in order for the notifications to be live.
		-This bat file will require Anaconda python to be installed with an Obspy environment

5.	In the parent directory, install chromedriver.exe
		-Future iterations of the code could see this being removed in the Python file
		-This is a work around method for there to be a preview image of the map displayed in Slack. Slack can't preview HTML files so the chromedriver is used to open the created HTML file in Chrome, take a screenshot of the opened window, then sends the jpeg image into the Slack thread.
		-If Chrome on the computer updates, the chromedriver.exe file needs to be updated as well. This can be done by going to https://chromedriver.chromium.org/, downloading the version of chromedriver that matches the build model of Chrome on the running computer, and extracting the exe file from the compressed folder to the parent directory.
		-Mismatched versions of the chromedriver and the version of Chrome on the host computer will cause the code to crash.

6.	Consult ONC Internal Confluence page for more information


		
