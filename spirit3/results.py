#This script is used for the automatic entry of RT-PCR BCR/ABL data into the SPIRIT 3 database

#***** Imports libraries *****
import csv
from Tkinter import * 
from tkFileDialog import * 
import mysql.connector
from datetime import datetime
import numpy as np

#***** Database Connection & Cursor *****
cnx = mysql.connector.connect(user='kirsty', password='ngskirsty_201605', host='10.229.233.250', database = 'spirit3')
cursor = cnx.cursor()

# ***** Variables ******
controls = []
standards = []
samples = []
standardresults = []
bcrablsample = []
ablsample = []

#**** Functions for use in script ******

#Function sorts the results in the csv file into POS/NEG/H2O/Standard/Sample and ABL/BCRABL
def resultsort(csv):
	for row in csv:
		if any("POS" in s for s in row):
			if any ("BCR-ABL" in s for s in row):
				del row[2:4]
				row[1] = 2
				row.append(1)
				controls.append(row)
			elif any ("GUS" in s for s in row):
				del row[2:4]
				row[1] = 3
				row.append(1)
				controls.append(row)
			else:
				del row[2:4]
				row[1] = 1
				row.append(1)
				controls.append(row)
		elif any("NEG" in s for s in row): 
			if any ("BCR-ABL" in s for s in row):
				del row[2:4]
				row[1] = 2
				row.append(2)
				controls.append(row)
			elif any ("GUS" in s for s in row):
				del row[2:4]
				row[1] = 3
				row.append(2)
				controls.append(row)
			else: 
				del row[2:4]
				row[1] = 1
				row.append(2)
				controls.append(row)
		elif any("H2O" in s for s in row):
			if any ("BCR-ABL" in s for s in row):
				del row[2:4]
				row[1] = 2
				row.append(3)
				controls.append(row)
			elif any ("GUS" in s for s in row):
				del row[2:4]
				row[1] = 3
				row.append(3)
				controls.append(row)
			else: 
				del row[2:4]
				row[1] = 1
				row.append(3)
				controls.append(row)
		elif any("Standard" in s for s in row):
			if any ("BCR-ABL" in s for s in row):
				del row[2:4]
				row[1] = 2
				standards.append(row)
			elif any ("GUS" in s for s in row):
				del row[2:4]
				row[1] = 3
				standards.append(row)
			else:
				del row[2:4]
				row[1] = 1
				standards.append(row)
		elif any("B" in s for s in row[1]) and not any("Experiment" in s for s in row):
			if any ("BCR-ABL" in s for s in row):
				del row[2:4]
				row.append(2)
				row[1] = row[1][0:8]
				samples.append(row)
			elif any ("GUS" in s for s in row):
				del row[2:4]
				row.append(3)
				row[1] = row[1][0:8]
				samples.append(row)
			else:
				del row[2:4]
				row.append(1)
				row[1] = row[1][0:8]
				samples.append(row)
	
#Function adds standard labels for ABL tests
def bcrabllabel(standard):
	for result in standard[0:2]:
		result.append(1)
	for result in standard[2:4]:
		result.append(2)
	for result in standard[4:6]:
		result.append(3)
	for result in standard[6:8]:
		result.append(4)
	for result in standard[8:10]:
		result.append(5)
	for result in standard[10:12]:
		result.append(6)
	for result in standard[12:14]:
		result.append(7)

#Function adds standard labels for GUSB tests
def guslabel(standard):
	for result in standard[0:2]:
		result.append(8)
	for result in standard[2:4]:
		result.append(9)
	for result in standard[4:6]:
		result.append(10)
	for result in standard[6:8]:
		result.append(11)
	for result in standard[8:10]:
		result.append(12)
	for result in standard[10:12]:
		result.append(13)
	for result in standard[12:14]:
		result.append(14)

#Function sorts the standard results 
def standardsort(standard):
	abl = [] 
	bcr = []
	gus = []
	for row in standard:
		if row[1] == 2:
			bcr.append(row)
		if row[1] == 1:
			abl.append(row)
		if row[1] == 3:
			gus.append(row)
	if len(gus) == 0:
		bcrabllabel(bcr)
		bcrabllabel(abl)
		for row in bcr:
			standardresults.append(row)
		for row in abl:
			standardresults.append(row)
	else:
		guslabel(bcr)
		guslabel(gus)
		for row in bcr:
			standardresults.append(row)
		for row in gus:
			standardresults.append(row)
	for row in standardresults:
		if len(row) == 11:
			del row[2]
		




#***** SQL statements for use in script ******
			
#Inserts Control Results into database. 
controlinsert = (""" 
		INSERT INTO controlresults(wellnumber, resulttypeid, controlct, controlctmean, controlquant, controlquantmean,     			controlctthresh, controlbasestart, controlbaseend, controltypeid)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
		INSERT INTO plate2control(controlresultid, plateid) 
		VALUES (LAST_INSERT_ID(), (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1));
 		""")

#Inserts Standard Results into database
standardinsert = ("""  
		 INSERT INTO standardresults(wellnumber, resulttypeid, standardct, standardctmean, standardquant, standardquantmean, 			 standardctthresh, standardbasestart, standardbaseend, standardtypeid)
		 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
		 INSERT INTO plate2standard(standardresultid, plateid)
		 VALUES (LAST_INSERT_ID(), (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1));
		 """)

#Inserts Sample Results into database
sampleinsert = ("""
		INSERT INTO sampleresult(wellnumber, samplect, samplectmean, samplequant, samplequantmean, 			     			samplectthresh, samplebasestart, samplebaseend, resulttypeid)
        	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); 
		INSERT INTO sampleseg(sampleresultid, sampleid, plateid)
		VALUES (LAST_INSERT_ID(), (SELECT sampleid FROM samples WHERE samplenumber=%s), (SELECT plateid FROM plate ORDER BY 			plateid DESC LIMIT 1));
		"""
		)

##**** Execution script ******
#Allows user to select a results file and reads the CSV
Tk().withdraw()
filename = askopenfilename()
f = open(filename)
csv_f = csv.reader(f)
csv = [row for row in csv_f]
	

#Finds the date of the plate run and adds to database
try:
	dateofrun = csv[3][1]
	dateofrun = dateofrun[0:10]
	dateofrun = datetime.strptime(dateofrun, '%Y-%m-%d')
	dateofrun = datetime.date(dateofrun)
	cursor.execute("""INSERT INTO plate(dateofrun)
	      	 VALUES (%s)""", ((dateofrun,)))
except:
	raise Exception ('The plate has no date. Please add a date')

#Sorts the results from the input file
resultsort(csv)
standardsort(standards)

for row in controls:
	if len(row) == 11:
		del row[2]

for row in samples:
	if len(row) == 11:
		del row[2]

#Adds results to database

for result in controls:
	cursor.execute(controlinsert, result)

for result in standardresults:
		cursor.execute(standardinsert, result)

for result in samples:
	sampleid = result[1]
	del result[1]
	result.append(sampleid)
	cursor.execute(sampleinsert, result)

#Commits results to the database 
cnx.commit() 
	




