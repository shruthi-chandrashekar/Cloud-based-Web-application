from flask import Flask ,abort , make_response , request, jsonify , render_template , url_for 
import requests 

import json
import pickle
import base64
import re
app = Flask(__name__)




@app.route('/')
def hello_world():
   return 'Hello World'
   
   
@app.route('/utsav')
def catch_all():	
	data = ["utsav"] 
	requests.post('http://127.0.0.1:6000/write/acts', json=data) 
	print("*"*100)
	resp = requests.get('http://127.0.0.1:6000/read/acts')
	#print(resp.text,"hello")
	return resp.text,200
	return "",200


if __name__ == '__main__':
   app.run(debug=True,port=8001)