import csv
import requests
from bs4 import BeautifulSoup
from fileinput import input, FileInput
from mailsend import *
headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

path = 'result/output.csv'
#regpath = 'uploads/regno.txt'
def newcsv(path):
	with open(path, "w") as csv_file:
		pass

def csv_writer(data, path):
    		with open(path, "a") as csv_file:
	        	writer = csv.writer(csv_file, delimiter=',')
        		for line in data:
            			print line
				writer.writerow(line)	


def PondyUniBot(regpath, emailtext):
	#Sending request to get the sub names
	f = open(regpath, "r")
	for lines in f.readlines():
		RegNo = lines[0:8]
        	break

	payload = {
                   'txtregno': RegNo,
                   'cmbdegree': 'BTHIT~\BTHIT\\result.mdb',
                   'cmbexamno': 'H',
                   'dpath': '\BTHIT\\result.mdb',
                   'dname': 'BTHIT',
                   'txtexamno': 'H'
                  }

	r = requests.post("http://result.pondiuni.edu.in/ResultDisp.asp", headers=headers, data=payload)

	if r.status_code == 200:
		soup = BeautifulSoup(r.text)
		SName = []
		for sub in range(len(soup.findAll("td", {"width" : "66%"}))):
	    		SName.append(soup.findAll("td", {"width" : "66%"})[sub].text.encode('utf-8'))

	# --- End ---

	data = []
	temp_data = []
	temp_data.append('RegNo')
	temp_data.append('Name')
	for totalsub in range(len(soup.findAll("td", {"width" : "66%"}))):    
		temp_data.append(SName[totalsub])
	temp_data.append('CGPA')
	data.append(temp_data)


	#path = open ('output.csv', 'w')
	newcsv(path)
	csv_writer(data, path)

	f = open(regpath, "r")
	for lines in f.readlines():

		RegNo = lines[0:8]
	
		payload = {
                   'txtregno': RegNo,
                   'cmbdegree': 'BTHIT~\BTHIT\\result.mdb',
                   'cmbexamno': 'H',
                   'dpath': '\BTHIT\\result.mdb',
                   'dname': 'BTHIT',
                   'txtexamno': 'H'
                  }


		r = requests.post("http://result.pondiuni.edu.in/ResultDisp.asp", headers=headers, data=payload)

		if r.status_code == 200:
	       		soup = BeautifulSoup(r.text)
			Name = soup.findAll("b")[3].contents[1].text.encode('utf-8')
			Grade = []
			for grades in range(9,31,3):
		    		Grade.append(soup.findAll("td", {"width" : "5%"})[grades].text.encode('utf-8'))

				#cgpa_find = soup.find_all('tr')[len(soup.find_all('tr')) - 6].contents[1]
				#CGPA = cgpa_find.find_all('b')[2].text.encode('utf-8')
				CGPA = 0

			data = []
			temp_data = []
			temp_data.append(RegNo)
			temp_data.append(Name)
			for totalsub in range(len(soup.findAll("td", {"width" : "66%"}))):    
				temp_data.append(Grade[totalsub])
			temp_data.append(CGPA)
			data.append(temp_data)

    		

    			csv_writer(data, path)
			
		else:
			print "Connection error!! "
	mail(emailtext,
   "Pondicherry University marks",
   "Please check out the attachment!, Thanks for using my service!",
   "result/output.csv")
	print "Mail sent to %s" % (emailtext)


