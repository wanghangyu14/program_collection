import pickle
import os
import re

class People(object):
	"""utilize a class of People to store peoples' information"""
	def __init__(self, name, adress, email, phonenumber):
		self.name=name
		self.adress=adress
		self.email=email
		self.phonenumber=phonenumber

#load function load a pickle instance once a time,so we need a recurrance to get all the pickle instance in the file.
def getAllRecord(filename):
	dic={}
	with open(filename,'rb+') as f:#Note that only rb+ mode can load file.
		try:
			while True:
				temp=pickle.load(f)#load a pickle instance(a dict instance indeed)
				for v in temp.values():
					dic[v.name]=v#copy value from temp to dic
		except EOFError as e:
			pass
	return dic

# check whether file exists
def checkFile(filename):
	if not os.path.exists(filename):
		return False
	return True

#save changes to file
def saveFile(filename,dic):
	with open(filename,'wb+') as f:
		pickle.dump(dic, f)

#get a person's information and return a People instance
def getInformation():
	name=input('Please enter a name:')
	adress=input('Please enter an adress:')
	while True:
		email=input('Please enter an e-mail:')
		if re.match(r'\w+\.?\w+@\w+\.com|org', email):
			break
		else:
			print('The format of e-mail is wrong!')
	while True:
		phonenumber=input('Please enter a phonenumber:')
		if re.match(r'\d{11}',phonenumber):
			break
		else:
			print('The format of phonenumber is wrong!')
	p=People(name, adress, email, phonenumber)
	return p

if __name__ == '__main__':
	'''written by why  
	   version = 0.1'''
	while True:
		option=input('Please enter a number：0.create 1.browse 2.add 3.edit 4.delete 5.find 6.exit')

		#create
		if option=='0':
			if checkFile('record.pk'):
				print('The file already exists!')
			else:
				dic={}
				p=getInformation()
				dic[p.name]=p
				saveFile('record.pk',dic)
				print('Finished creating!')
		
		#browse
		if option=='1':
			if not checkFile('record.pk'):
				print('The file does not exist!')
			else:
				record=getAllRecord('record.pk')
				for v in record.values():#print all the record in the 'record' dict
					print('name:{}\nadress:{}\ne-mail:{}\nphonenumber:{}\n'.format(v.name,v.adress,v.email,v.phonenumber), sep=' ', end='\n')

		#add
		if option=='2':
			if not checkFile('record.pk'):
				print('The file does not exist!')
			else:
				p=getInformation()
				record=getAllRecord('record.pk')
				record[p.name]=p#add p instance to 'record' dict
				saveFile('record.pk',record)
				print('Finished adding!')

		#edit
		if option=='3':
			if not checkFile('record.pk'):
				print('The file does not exist!')
			name=input('Please enter a person\'s name you want to edit:')
			part=input('Which part do you want to edit?')
			change=input('Please enter your change:')
			record=getAllRecord('record.pk')
			setattr(record[name],part,change)#get the specified People instance from 'record' dict and change the 'part'(such as email) with 'change'
			saveFile('record.pk',record)
			print('Finished editing!')

		#delete
		if option=='4':
			if not checkFile('record.pk'):
				print('The file does not exist!')
			else:
				record=getAllRecord('record.pk')
				name=input('Please enter the person you want to delete:')
				del record[name]
				saveFile('record.pk',record)
				print('Finished deleting!')

		#find
		if option=='5':
			if not checkFile('record.pk'):
				print('The file does not exist!')
			else:
				name=input('Please enter a person\'s name:' )#get key
				record=getAllRecord('record.pk')
				if name in record:#judge whether the key exists
					v=record[name]
					print('name:{}\nadress:{}\ne-mail:{}\nphonenumber:{}\n'.format(v.name,v.adress,v.email,v.phonenumber), sep=' ', end='\n')
				else:
					print('Can not find such person!')

		#exit
		if option=='6':
			exit(0)