from flask import Flask
import requests 

app = Flask(__name__)

import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
REFRESH_INTERVAL = 5 #seconds
 
scheduler = BackgroundScheduler()
scheduler.start()
DOCKER_START=""
def main():
    # Call our function the first time
    health_check()

        # then every 60 seconds after that.
    scheduler.add_job(health_check, 'interval', seconds = REFRESH_INTERVAL)
 
    # main loop
    while True:
    	time.sleep(1)


crash=0
tester=[8000]
i=0
def health_check():
	global i
	global tester
	print(str(tester[i]))
	resp = requests.get('http://0.0.0.0:'+str(tester[i])+'/'+'api/v1/_health')
	if resp.status_code==200:
		print(str(tester[i]),"is working")
		i=i+1
		if i==len(tester):
			i=0
	else:
		print("here")
		DOCKER_KILL="docker kill "+str(tester[i])
		os.system(DOCKER_KILL)
		DOCKER_START="docker run --rm --name "+str(tester[i])+" -d -p "+str(tester[i])+":5000 -ti -v a6:/file acts"
		os.system(DOCKER_START)
		i=i+1
		if i==len(tester):
			i=0

if __name__ == "__main__":
    main()
