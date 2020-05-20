from flask import Flask ,abort , make_response , request, jsonify , render_template , url_for 
import requests 

import json
import pickle
import base64
import re
import unicodedata

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

chttp=0
cacts=0
categories={}
users=[]
acts=[]

with open('/file/categories.json', 'r+') as fp:
	categories=pickle.load(fp)
fp.close()
with open('/file/acts.json', 'r+') as fp:
	acts=pickle.load(fp)
fp.close()

print(categories,"categories")
print(acts,"acts")

crash=0

@app.route('/api/v1/_crash',methods=['POST'])
def crash_check():
	global crash
	crash=1
	return "",200

@app.route('/api/v1/_health',methods=['GET'])
def health_check():
	global crash
	if (crash==1):
		return "",500

	return "",200
@app.route('/api/v1/acts/counts')
def count_acts():
	if (crash==1):
		return "",500
	if request.method== 'POST' or request.method== 'DELETE' or request.method=='PUT' :
			return "",405
	return jsonify([len(acts)]),200
	

@app.route('/api/v1/_count',methods=['GET','POST','PUT'])
def count_http():
	if (crash==1):
		return "",500

	if request.method== 'POST' or request.method== 'DELETE' or request.method=='PUT' :
		return "",405
	
	global chttp
	return jsonify([chttp]),200


@app.route('/api/v1/_count' , methods=['DELETE','POST','PUT'])
def reset_http():
	if (crash==1):
		return "",500
	if request.method== 'POST' or request.method== 'GET' or request.method=='PUT' :
		return "Wrong Method",405
	global chttp
	chttp=0	
	return "",200

@app.route('/api/v1/categories', methods=['POST'])
def create_cats():
	if (crash==1):
		return "",500
	if request.method== 'GET' or request.method== 'DELETE' or request.method=='PUT' :
		return "",405
	global chttp
	global categories
	chttp+=1
	with open('/file/categories.json', 'r+') as fp:
		categories=pickle.load(fp)
	fp.close()
	with open('/file/acts.json', 'r+') as fp:
		acts=pickle.load(fp)
	fp.close()
	#categories=categories1[0]
	#print(categories,"create")
	cat={}
	c =request.json
	print(c)
	a=""
	for ele in c:
		a=str(ele)
	print(a,"qwerty")
	for key in categories:
		if str(key)==a :
			return "This category already exists",400
	categories[a]=0
	with open("/file/categories.json", 'w') as fp:
		pickle.dump(categories,fp)
	fp.close()
	return "",201


@app.route('/api/v1/categories', methods=['GET'])
def get_cats_list():
	if (crash==1):
		return "",500
	global chttp
	global categories
	chttp+=1

	if request.method== 'POST' or request.method== 'DELETE' or request.method=='PUT' :
		return "",405
	with open('/file/categories.json', 'r+') as fp:
		categories=pickle.load(fp)
	fp.close()
	with open('/file/acts.json', 'r+') as fp:
		acts=pickle.load(fp)
	fp.close()

	if(len(categories)!=0):
		return jsonify(categories),200
	else:
		return "No category to show ",204
@app.route('/api/v1/categories/<cat_id>', methods=['DELETE']) 
def delete_cat(cat_id):
	if (crash==1):
		return "",500
	if request.method== 'GET' or request.method== 'POST' or request.method=='PUT' :
		return "",405
	with open('/file/categories.json', 'r+') as fp:
		categories=pickle.load(fp)
	fp.close()
	with open('/file/acts.json', 'r+') as fp:
		acts=pickle.load(fp)
	fp.close()
	global chttp
	chttp+=1
	flag=0
	catid=0
	for key in list(categories.keys()):
		if key==cat_id:
			del categories[key]
			flag=1

	for act in acts:
		if(act['categoryName']==cat_id and flag==1):
			acts.remove(act)
	for act in acts:
		if(act['categoryName']==cat_id and flag==1):
			acts.remove(act)

	with open("/file/acts.json", 'w') as fp:
		pickle.dump(acts,fp)
		fp.close()

	with open("/file/categories.json", 'w') as fp:
		pickle.dump(categories,fp)
		fp.close()

	if(flag == 1):
		return "",200
		#return jsonify({'cats':categories}), 200   
	else:
		return "Cannot delete non existing category",400
@app.route('/api/v1/categories/<cat_id>/acts', methods=['GET'])
def get_acts_list(cat_id):
	if (crash==1):
		return "",500
	with open('/file/categories.json', 'r+') as fp:
		categories=pickle.load(fp)
	fp.close()
	with open('/file/acts.json', 'r+') as fp:
		acts=pickle.load(fp)
	fp.close()
	print("here")
	if request.method== 'POST' or request.method== 'DELETE' or request.method=='PUT' :
		return "",405
	global chttp
	chttp+=1
	length=0
	id1=0
	flag=0
	k1=0
	k=[]
	for key,values in categories.iteritems():
			if key==cat_id:
				k1=categories[key]
	if(k1>100):
		return "",413
	else:
		for act in acts:
			if(act['categoryName']==cat_id):
				flag=1
				k.append(act)	

	if(flag == 1):
		return jsonify(k) ,200   

	else:
		print("here")
		return "No acts to show",204


@app.route('/api/v1/categories/<cat_id>/acts/size', methods=['GET'])
def number_of_acts(cat_id):
	if (crash==1):
		return "",500
	with open('/file/categories.json', 'r+') as fp:
		categories=pickle.load(fp)
	fp.close()
	with open('/file/acts.json', 'r+') as fp:
		acts=pickle.load(fp)
	fp.close()
	#print(categories,type(categories))
	length=0
	flag=0
	if request.method== 'POST' or request.method== 'DELETE' or request.method=='PUT' :
		return "",405
	global chttp
	chttp+=1
	for key,value in categories.iteritems():
		if(key==cat_id):
			length=categories[key]
			flag=1

	if(flag == 1):
		return jsonify([length]) ,200
	else:
		return "No acts exist",204

@app.route('/api/v1/acts/upvote', methods=['GET','POST','DELETE'])
def upvote():
	if (crash==1):
		return "",500
	with open('/file/categories.json', 'r+') as fp:
		categories=pickle.load(fp)
	fp.close()
	with open('/file/acts.json', 'r+') as fp:
		acts=pickle.load(fp)
	fp.close()
	flag=0
	if request.method== 'GET' or request.method== 'DELETE' or request.method=='PUT' :
		return "Wrong method",405
	global chttp
	chttp+=1
	check=request.json

	if(len(check)>1):
		return "",400

	ele=check[0]

	for act in acts:
		if(act['actId']==ele):
			act['upvote']=act['upvote']+1
			flag=1
			#print(act['upvote'])

	#requests.post('http://127.0.0.1:6000/write/acts', json=acts)

	with open("/file/acts.json", 'w') as fp:
		pickle.dump(acts,fp)
	fp.close()
	with open("/file/categories.json", 'w') as fp:
			pickle.dump(categories,fp)
	fp.close()
	if(flag==1):    
		return "",200
	else:
		return "Act not found",400
@app.route('/api/v1/categories/<cat_id>/acts1', methods=['GET'])
def range_of_acts(cat_id):
	if (crash==1):
		return "",500
	with open('/file/categories.json', 'r+') as fp:
		categories=pickle.load(fp)
	fp.close()
	with open('/file/acts.json', 'r+') as fp:
		acts=pickle.load(fp)
	fp.close()
	if request.method== 'POST' or request.method== 'DELETE' or request.method=='PUT' :
		return "",405

	global chttp
	chttp+=1
	ac=[]
	ac1=[]
	flag=0
	val=0
	start=int(request.args['start'])
	end=int(request.args['end'])

	if ((end-start)+1>100):
		return "",413
	else:
		for act in acts:
			if act['categoryName']==cat_id:
				ac.append(act)
				flag=1
		if (flag==0):
			return "",204

		for keys,values in categories.iteritems():
			if keys==cat_id :
				val=categories[keys]
		if (val<end):
			end=val+1

		for i in range (start,end-1):
			ac1.append(ac[i])

		if (flag==1):
			return jsonify(ac1),200
@app.route('/api/v1/acts/<int:act_id>', methods=['DELETE'])
def delete_act(act_id):
	if (crash==1):
		return "",500
	if request.method== 'GET' or request.method== 'POST' or request.method=='PUT' :
		return "wrong method",405
	with open('/file/categories.json', 'r+') as fp:
		categories=pickle.load(fp)
	fp.close()
	with open('/file/acts.json', 'r+') as fp:
		acts=pickle.load(fp)
	fp.close()
	global chttp
	chttp+=1	
	flag=0

	catid=""

	for act in acts:
		if(act['actId']==act_id):
			flag=1
			acts.remove(act)
			catid=act['categoryName']

	for key,value in categories.iteritems():
		if(key==catid):
			categories[key]-=1

	with open("/file/categories.json", 'w') as fp:
		pickle.dump(categories,fp)
		fp.close()

	with open("/file/acts.json", 'w') as fp:
		pickle.dump(acts,fp)
		fp.close()

	if(flag == 1):
		return    "",200 
	else:
		return "Could not delete act",400
@app.route('/api/v1/acts', methods=['GET','POST','DELETE'])
def create_acts():
	if (crash==1):
		return "",500
	with open('/file/categories.json', 'r+') as fp:
		categories=pickle.load(fp)
	fp.close()
	with open('/file/acts.json', 'r+') as fp:
		acts=pickle.load(fp)
	fp.close()
	id1=0
	flag=0
	uflag=0
	if request.method== 'GET' or request.method== 'DELETE' or request.method=='PUT' :
		return "",405
	global chttp
	chttp+=1
	username=request.json.get('username').encode("ascii")
	resp = requests.get('http://127.0.0.1:9000/api/v1/users')
	if(resp.status_code == 201):
		all_user=resp.json()
		for i in range(0,len(all_user)):
			if(all_user[i].encode("ascii")==username):
				#print("user")
				uflag=1
				break
		if(not uflag):
			return "No user",400
	else :
		return "No user name ",400

	act1= {
		'actId': request.json.get('actId',""),
		'username':request.json.get('username',""),
		'timestamp': request.json.get('timestamp',""),
		'categoryName': request.json.get('categoryName',""),
		'imgB64': request.json.get('imgB64',""),
		'caption': request.json.get('caption',""),
		'upvote':request.json.get('upvote',"")
	  }
	s=act1["imgB64"]
	try:
		if(base64.b64encode(base64.b64decode(s)) == s):
			pass
	except Exception:
		return "image not in base64",400
	for act in acts:
		if(act['actId']==act1['actId']):
			return "duplicate act id",400
	if re.match("([0-2][0-9]|(3)[0-1])-((0)[0-9]|(1)[0-2])-[1-9][0-9][0-9][0-9]:[0-5][0-9]-[0-5][0-9]-((0)[0-9]|(1)[0-9]|(2)[0-3])",act1['timestamp']):
		pass
	else:
		return "Enter the timestamp properly",400
	if(act1['upvote']):
		return "upvote to be 0",400
	for key,values in categories.iteritems():
		if (key==act1['categoryName']):
			categories[key]+=1
			flag=1
			with open("/file/categories.json", 'w') as fp:
				pickle.dump(categories,fp)
			fp.close()
	#separate dictionary so no one could tamper with the upvotes
	#above dictionary is user fed inputs below dictionary is what we feed to the list.
	act = {
	'caption':act1['caption'],
	'actId': act1['actId'],
	'timestamp':act1['timestamp'],
	'imgB64':act1['imgB64'],
	'upvote':0,
	'username':act1['username'],
	'categoryName':act1['categoryName']
	}
	acts.append(act)
	if(flag==1):
		with open("/file/acts.json", 'w') as fp:
			pickle.dump(acts,fp)
		fp.close()
		return "",200
	else:
		return "Category does not exist",400


if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0",port=5000)

