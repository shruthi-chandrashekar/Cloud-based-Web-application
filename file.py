from flask import Flask ,abort , make_response , request, jsonify , render_template , url_for 
import requests 

import json
import pickle
import base64
import re

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

categories=[]
acts=[]

@app.route('/write/acts',methods=['POST'])
def a1write():
	wdata=request.json 
	acts.append(wdata)
	print(wdata)
	with open("acts.json", 'a') as fp:
		pickle.dump(acts,fp)
	fp.close()
	return "",200
	
@app.route('/write/categories',methods=['POST'])
def a2write():
	wdata=request.json 
	with open("categories.json", 'a') as fp:
		pickle.dump(wdata,fp)
		fp.close()
	return "",200


@app.route('/read/acts')
def a3read():
	with open('acts.json', 'r') as fp:
		acts=pickle.load(fp)
	fp.close()
	print(acts)
	return jsonify(acts),200
	
@app.route('/read/categories')
def a4read():
	with open('categories.json', 'r') as fp:
		categories=pickle.load(fp)
	fp.close()
	return jsonify(categories),200


if __name__ == '__main__':
   app.run(debug=True,port=6000)

