#This script is used for the automatic calculation of sample results for the SPIRIT3 database

#***** Imports libraries *****
import mysql.connector
import numpy as np

#***** Database Connection & Cursor *****
cnx = mysql.connector.connect(user='kirsty', password='ngskirsty_201605', host='10.229.233.250', database = 'spirit3')
cursor = cnx.cursor()

# ***** Variables ******
IDresults = []
IDdict = {}
sampleresultid = []
sampleid = []
sampleresults = []
ablgussample = []
bcrsample = []
ablgusqcresult = []
bcrablresult = []

#**** Functions for use in script ******

def removeduplicates(values):
	output = []
	seen = set()
	for value in values:
		if value not in seen:
			output.append(value)
			seen.add(value)
	return output

#Function carries out sample result ABLQC
def ablgusqc(result, ids):
	for ids in ids:
		temp = []
		temp2 = []
		for row in result:
			if row[10] == ids:
				temp.append(row[5])
		yes = sum(temp)
		temp2.append(ids)
		temp2.append(yes)
		if temp[0] >= 10000 and temp[1] >= 10000 and temp[2] >= 10000:
			temp2.append(1)
		else:
			temp2.append(2)
		if yes >= 32000:
			temp2.append(1)
		else:
			temp2.append(2)
		if temp2[2] == 1:
			if temp2[3] == 1:
				temp2.append(1)
			elif temp2[3] == 2:
				temp2.append(3)
		else:
			temp2.append(2)
		ablgusqcresult.append(temp2)

#Carries our BCR ABL analysis
def bcrablanalysis(bcrsample, sampleids):
	for ids in sampleids:
		temp = []
		temp2 = []
		temp3 = []
		for row in bcrsample:
			if row[10] == ids:
				temp.append(row[5])
				temp3.append(row[3])
		yes = sum(temp)
		temp2.append(ids)
		temp2.append(yes)
		for row in ablgusqcresult:
			if row[0] == ids:
				ratio = (yes / row[1]) * 1.4
				temp2.append(ratio)
				percentage = ratio * 100
				temp2.append(percentage)
				if ablgussample[0][1] == 3:
					if percentage <=10 and percentage >=1 and row[1] >=27000:
						temp2.append(1)
					elif percentage <=1 and percentage >0.1 and row[1] >=27000:
						temp2.append(2)
					elif percentage <=0.1 and percentage >0.01 and row[1] >=27000:
						temp2.append(3)
					elif percentage <=0.01 and percentage >0.0032 and row[1] >=27000 and row[1] <=86399:
						temp2.append(4)
					elif percentage <= 0.032 and percentage >0.001 and row[1] >=86400 and row[1] <=269999:
						temp2.append(4.5)
					elif percentage <= 0.001 and percentage >0.0001 and row[1] <=270000:
						temp2.append(5)
					else:
						temp2.append(0)
				else:
					if percentage <=10 and percentage >=1 and row[1] >=10000:
						temp2.append(1)
					elif percentage <=1 and percentage >0.1 and row[1] >=10000:
						temp2.append(2)
					elif percentage <=0.1 and percentage >0.01 and row[1] >=10000:
						temp2.append(3)
					elif percentage <= 0.01 and percentage >0.0032 and row[1] >=10000 and row[1] <=31999:
						temp2.append(4)
					elif percentage <= 0.032 and percentage >0.001 and row[1] >=32000 and row[1] <=99999:
						temp2.append(4.5)
					elif percentage <=0.001 and percentage >0.0001 and row[1] >=100000:
						temp2.append(5)
					else:
						temp2.append(0)
				sensitivity = 1 / row[1]
				temp2.append(sensitivity)
				if temp3[0] <=30 and temp3[0] >0:
					if temp3[1] <=30 and temp3[1] >0:
						if temp3[2] <=30 and temp3[2] >0:
							if (temp3[2] - temp3[0]) <0.5:
								temp2.append(12)
				if temp3[0] >= 30.1 and temp3[0] <=33:
					if temp3[1] >= 30.1 and temp3[1] <=33:
						if temp3[2] >= 30.1 and temp3[2] <=33: 
							if (temp3[2] - temp3[0]) <= 1:
								temp2.append(13)
				if temp3[0] >=33.1 and temp3[0] <=37:
					if temp3[1] >=33.1 and temp3[1] <=37:
						if temp3[2] >=33.1 and temp3[2] <=37:
							if (temp3[2] - temp3[0]) <= 1.5:
								temp2.append(14)
				if temp3[0] >=37.1 and temp3[1] >=37.1 and temp3[2] >=37.1:
					if (temp[2] - temp[0]) <=1.5:
						temp2.append(17)
				if np.count_nonzero(temp3) == 1:
					temp2.append(15)
				if np.count_nonzero(temp3) == 2:
					temp2.append(16)
				if sum(temp3) == 0:
					temp2.append(11)
				if len(temp2) == 6:
					temp2.append(19)
		bcrablresult.append(temp2)
				

#***** SQL statements for use in script ******

IDselect = (""" 
	   SELECT * FROM sampleseg WHERE plateid = (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1);
	   """)

sampleresult = (""" 
		SELECT * FROM sampleresult WHERE sampleresultid = %s;
		""")

insertablgusqc = (""" 
	       INSERT INTO ablresutqc(sampleid, ablanalysis, totalcheck, individualcheck, qcresult)
	       VALUES (%s, %s, %s, %s, %s);
	       """)


insertbcrresult = (""" 
	       INSERT INTO resultanalysis(sampleid, BCRcopies, BCRABLratio, percentageratio, mr, sensitivity, statementsid)
	       VALUES (%s, %s, %s, %s, %s, %s, %s);
	       """)


##**** Execution script ******

#Selects the samples IDs and result IDs from the DB
cursor.execute(IDselect)
ID = cursor.fetchall()
for row in ID:
	IDresults.append(list(row))
for row in IDresults:
	IDdict[row[2]] = row[1]
	sampleresultid.append(row[2])
	sampleid.append(row[1])

#Selects sample results from the DB and seperates
for row in sampleresultid:
	cursor.execute(sampleresult, (row,))
	pick = list(cursor.fetchone())
	sampleresults.append(pick)

sampleids = removeduplicates(sampleid)

for result in sampleresults:
	sid = IDdict.get(result[0])
	result.append(sid)
	if result[1] == 1 or result[1] == 3:
		ablgussample.append(result)
	else:
		bcrsample.append(result)

#Carries out Sample ABLQC
ablgusqc(ablgussample, sampleids)

#Carries out BCR-ABL analysis
bcrablanalysis(bcrsample, sampleids)


#Inputs Results into Database 
		
for result in ablgusqcresult:
	cursor.execute(insertablgusqc, result)

for result in bcrablresult:
	cursor.execute(insertbcrresult, result)
	
#Commits results to database
cnx.commit() 
