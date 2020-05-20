from flask import Flask,request,jsonify
import requests
import re
import math
import os
from threading import Event
event = Event()


app = Flask(__name__)

import time
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()
DOCKER_START=""
crash=0
containers=[8000]
def health_check():
	event.wait()
	print(len(containers))
	for i in range(0,len(containers)):
		resp = requests.get('http://0.0.0.0:'+str(containers[i])+'/'+'api/v1/_health')
		print(resp.status_code)
		if resp.status_code==200:
			print(str(containers[i]),"is working")
		else:
			print("here")
			DOCKER_KILL="docker kill "+str(containers[i])
			os.system(DOCKER_KILL)
			DOCKER_START="docker run --rm --name "+str(containers[i])+" -d -p "+str(containers[i])+":5000 -ti -v a6:/file acts"
			os.system(DOCKER_START)
    #global tester

"""
    if (len(containers)==0):
    	pass
    else:
    	if(i==len(containers)):
    		i=0
    		print("akdsjfall")
    	print(containers)
    	print(i)
    	resp = requests.get('http://0.0.0.0:'+str(containers[i])+'/'+'api/v1/_health')
    	if resp.status_code==200:
    		print(str(containers[i]),"is working")
    		i=i+1
    	else:
    		print("here")
    		DOCKER_KILL="docker kill "+str(containers[i])
    		os.system(DOCKER_KILL)
    		DOCKER_START="docker run --rm --name "+str(containers[i])+" -d -p "+str(containers[i])+":5000 -ti -v a6:/file acts"
    		os.system(DOCKER_START)
    		i=i+1"""
 
i=0
count=0
num_of_containers=0
one_flag=1


DOCKER_START="docker  run --rm --name 8000  -p 8000:5000 -ti -v a6:/file acts"


@app.route('/')
def hello_world():
   return 'Hello World'


def del_con():
	global num_of_containers,count,containers,one_flag
	#containers=containers[:num_of_containers]
	event.clear()
	DOCKER_KILL="docker kill "
	#print("delete",(len(containers),num_of_containers))
	for i in range(len(containers),num_of_containers,-1):
		if(containers[i-1]==8000):
			continue
		os.system(DOCKER_KILL+str(containers[i-1]))
		print("deleting",containers[i-1])
		del containers[i-1]
		#print("deleting",containers[i])
	event.set()
	print("delete")
	num_of_containers=0
	count=0
	#print(num_of_containers)

def add_con(add_con):
	global count,num_of_containers,one_flag
	print("creating")
	for i in range(add_con):
		print("starting containers")
		new_port=containers[-1] + 1
		DOCKER_START="docker  run --rm --name "+str(new_port)+" -d -p "+str(new_port)+":5000 -ti -v a6:/file acts"
		os.system(DOCKER_START)
		containers.append(new_port)
	num_of_containers=0
	count=0
	#print(num_of_containers)
		
  
def new_container():
	global num_of_containers
	con=num_of_containers-len(containers)
	print("len con",len(containers),num_of_containers)
	if(con > 0 ):
		add_con(con)
	elif(con < 0):
		del_con()
	else:
		print("no auto scalling ")
		
def health_check2():
	print(containers)
   
@app.route('/<path:path>',methods=['POST','GET','DELETE'])
def catch_all(path):
    
	global i,count,one_flag,num_of_containers
	test=[[8000],[8001] ]
	print(path)
    #resp = requests.get('http://127.0.0.1:'+str(test[i][0])+'/'+path)
	crash = re.search("_crash", path)
	health=re.search("_health",path)
	if(health or crash):
		print("Not counting ")
	else:
		acts_api=re.search("api/v1/*",path)
		if(acts_api):
			count+=1
	num_of_containers=math.ceil(count/2)
	if(count ==1 and one_flag):
		event.set()
		print(count)
		scheduler.add_job(health_check, 'interval', seconds = 1)
		scheduler.add_job(new_container, 'interval', seconds = 60)
		scheduler.add_job(health_check2, 'interval', seconds = 5)
		one_flag=0
	if(len(containers)>0):
		if(request.method=='GET'):
			resp = requests.get('http://0.0.0.0:'+str(containers[i])+'/'+path)
			print(type(resp.json()))
			print("GET",containers[i])
			rd,rs=jsonify(resp.json()),resp.status_code
		elif(request.method=='POST'):
			data=request.json
			resp =requests.post('http://0.0.0.0:'+str(containers[i])+'/'+path,json=data)
			print("POST",containers[i])
			print(resp.status_code)
			rd,rs="",resp.status_code
		else:
			resp =requests.delete('http://0.0.0.0:'+str(containers[i])+'/'+path)
			print("DELETE",containers[i])
			print(resp.status_code)
			rd,rs="",resp.status_code
			#print(data)
		i+=1
		if(i==len(containers)):
			i=0	
	else :
		pass
	
	
	return rd,rs



if __name__ == '__main__':
    app.run(debug=True)

