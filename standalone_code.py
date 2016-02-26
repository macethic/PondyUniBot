import csv
import requests
from bs4 import BeautifulSoup, Comment
from fileinput import input, FileInput

headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

def newcsv(path):
	with open(path, "w") as csv_file:
		pass

def csv_writer(data, path):
    		with open(path, "a") as csv_file:
	        	writer = csv.writer(csv_file, delimiter=',')
        		for line in data:
            			print line
				writer.writerow(line)	


#Sending request to get the sub names
for lines in FileInput():
        RegNo = lines[0:8]
        break

payload = {
                   'txtregno': RegNo,
                   'cmbdegree': 'BTHCS~\BTHCS\\result.mdb',
                   'cmbexamno': 'G',
                   'dpath': '\BTHCS\\result.mdb',
                   'dname': 'BTHCS',
                   'txtexamno': 'G'
                  }

r = requests.post("http://result.pondiuni.edu.in/ResultDisp.asp", headers=headers, data=payload)


if r.status_code == 200:
	soup = BeautifulSoup(r.text)
	print soup
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


path = "output.csv"
#path = open ('output.csv', 'w')
newcsv(path)
csv_writer(data, path)

for lines in input():
	RegNo = lines[0:8]
	
	payload = {
                   'txtregno': RegNo,
                   'cmbdegree': 'BTHCS~\BTHCS\\result.mdb',
                   'cmbexamno': 'G',
                   'dpath': '\BTHCS\\result.mdb',
                   'dname': 'BTHCS',
                   'txtexamno': 'G'
                  }


	r = requests.post("http://result.pondiuni.edu.in/ResultDisp.asp", headers=headers, data=payload)

	if r.status_code == 200:
	       	soup = BeautifulSoup(r.text)
		Name = soup.findAll("b")[3].contents[1].text.encode('utf-8')
		Grade = []
		for grades in range(9,37,3):
		    Grade.append(soup.findAll("td", {"width" : "5%"})[grades].text.encode('utf-8'))

		#cgpa_find = soup.find_all('tr')[len(soup.find_all('tr')) - 6].contents[1]
		#CGPA = cgpa_find.find_all('b')[2].text.encode('utf-8')
		#CGPA = 0
		comments = soup.findAll(text=lambda text:isinstance(text, Comment))
		CGPA = [comment.extract() for comment in comments][0][26:30]
		data = []
		temp_data = []
		temp_data.append(RegNo)
		temp_data.append(Name)
		for totalsub in range(len(soup.findAll("td", {"width" : "66%"}))):    
			temp_data.append(Grade[totalsub])
		temp_data.append(CGPA)
		data.append(temp_data)

    		

		path = "output.csv"
    		csv_writer(data, path)
	else:
		print "Connection error!! "

