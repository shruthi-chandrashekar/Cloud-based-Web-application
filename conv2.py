import pickle

categories  = []

acts= []

users=[]

with open("categories.json", 'w') as fp:
	#for item in categories:
	pickle.dump(categories,fp)
	
fp.close()
with open("acts.json", 'w') as fp:
	#for item in categories:
	pickle.dump(acts,fp)
	
fp.close()
with open("users.json", 'w') as fp:
	#for item in categories:
	pickle.dump(users,fp)
	
fp.close()
