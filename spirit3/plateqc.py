#This script is used for the automatic calculation of plate qc for the SPIRIT3 database

#***** Imports libraries *****
import mysql.connector
from scipy import stats
import numpy as np

#***** Database Connection & Cursor *****
cnx = mysql.connector.connect(user='kirsty', password='ngskirsty_201605', host='10.229.233.250', database = 'spirit3')
cursor = cnx.cursor()

# ***** Variables ******

std = []
cntrl = []
bcrplateqc = []
ablgusplateqc =[]
replicatectresult = []
ablgusstdcurve = []
bcrstdcurve = []
totalplateqc = []

#**** Functions for use in script ******

def controlqc(controls):
	ablgush2oarray = []
	ablgusnegarray = []
	bcrh2oarray = []
	bcrnegarray = []
	ablgusthresharray = []
	bcrthresharray = []
	for result in controls:
		if result[2] == 1 or result[2] == 3:
			if result[1] == 3:
				ablgush2oarray.append(result[4])
				ablgusthresharray.append(result[8])
			elif result[1] == 2:
				ablgusnegarray.append(result[4])
	
		if result[2] == 2:
			if result[1] == 3:
				bcrh2oarray.append(result[4])
				bcrthresharray.append(result[8])
			elif result[1] == 2:
				bcrnegarray.append(result[4])
	if ablgush2oarray[0] == 0 and ablgush2oarray[1] == 0:
		ablgusplateqc.append(1)
	else:
		ablgusplateqc.append(2)
	if bcrh2oarray[0] == 0 and bcrh2oarray[1] == 0:
		bcrplateqc.append(1)
	else:
		bcrplateqc.append(2)
	if ablgusnegarray[0] == 0 and ablgusnegarray[1] == 0 and ablgusnegarray[2] ==0:
		ablgusplateqc.append(1)
	else: 
		ablgusplateqc.append(2)
	if bcrnegarray[0] == 0 and bcrnegarray[1] == 0 and bcrnegarray[2] ==0:
		bcrplateqc.append(1)
	else: 
		bcrplateqc.append(2)
	if ablgusthresharray[1] == 0.1:
		ablgusplateqc.append(1)
	else:
		ablgusplateqc.append(2)
	if bcrthresharray[1] == 0.1:
		bcrplateqc.append(1)
	else: 
		bcrplateqc.append(2)

#Function calculates the replicate ct values and carries out replicatect and 20/50 and standard curve point checks. 
def calculatereplicatect(standards):
	ablgus = []
	bcr = []
	ablguspoint = []
	bcrpoint = []
	count1 = 0
	count2 = 0
	index = 0
	for row in standards:
		if row[2] == 1 or row[2] == 3:
			ablgus.append(row[4])
		else:
			bcr.append(row[4])
	for number in ablgus:
		index += 1
		if index >=1 and index %2 != 0:
			count1 += 1
			index2 = index - 1
			repct = ablgus[index] - ablgus[index2]
			ablgusresult = [repct, 4, count1]
			replicatectresult.append(ablgusresult)
			if ablgusresult[2] == 7:
				if ablgusresult[0] <=1.5:
					ablgusplateqc.append(1)
				else: 
					ablgusplateqc.append(2)
			if ablgusresult[2] <= 6:
				ablguspoint.append(ablgusresult[0])
	index = 0
	for number in bcr:
		index += 1
		if index >=1 and index %2 != 0:
			count2 += 1
			bcrresult = []
			index2 = index - 1
			repct = bcr[index] - bcr[index2]
			bcrresult = [repct, 2, count2]
			replicatectresult.append(bcrresult)
			if bcrresult[2] == 7:
				if bcrresult[0] <=1.5:
					bcrplateqc.append(1)
				else:
					bcrplateqc.append(2)
			if bcrresult[2] <= 6:
				bcrpoint.append(bcrresult[0])
	if ablguspoint[0] <=1 and ablguspoint[1] <=1 and ablguspoint[2] <=1 and ablguspoint[3] <=1 and ablguspoint[4] <=1 and ablguspoint[5] <=1:
		ablgusplateqc.append(1)
	else:
		ablgusplateqc.append(2)
	if bcrpoint[0] <=1 and bcrpoint[1] <=1 and bcrpoint[2] <=1 and bcrpoint[3] <=1 and bcrpoint[4] <=1 and bcrpoint[5] <=1:
		bcrplateqc.append(1)
	else:
		bcrplateqc.append(2)
 	


#***** SQL statements for use in script ******

#Selects standardids from plate
standardselect = (""" 
		SELECT standardresultid FROM plate2standard WHERE plateid = (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1);
 		""")

#Selects the standard results
standardresult= (""" 
		SELECT * FROM standardresults WHERE standardresultid = %s
	       """)

#Selects control ids from plate 
controlselect = (""" 
		SELECT controlresultid FROM plate2control WHERE plateid = (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1);
		""")

#Selects the control results 
controlresults = ("""
		  SELECT * FROM controlresults WHERE controlresultid = %s
		 """)

#Selects the standard curve which is needed for analysis
standardcurveselect = ("""
			SELECT * FROM standardcurve WHERE standardcurveid = %s;
		       """) 

#Inserts calculated insertreplicatect into database
insertreplicatect = ("""
		     INSERT INTO replicatect(replicatect, resulttypeid, standardtypeid, plateid)
		     VALUES (%s, %s, %s, (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1));
		    """) 

#Inserts QC check results
insertplateqcresults = (""" 
			INSERT INTO plateqc(watercheck, negcheck, thresholdcheck, baselinecheck, poscheck, stdcurve2050, 				stdcurvepoints, slopecheck, correlationcheck, resulttypeid, plateid) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1));
			""")

#Inserts overall Pass/Fail result
insertqcresult = (""" INSERT INTO plateqcresult(plateid, passfailid)
		  VALUES ((SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1), %s);
		  """)

##**** Execution script ******

#Selects relevant standards from the database
cursor.execute(standardselect)
standardresults = cursor.fetchall()

for result in standardresults:
	cursor.execute(standardresult, result)	
	pick = list(cursor.fetchone())
	std.append(pick)

#Selects relevant controls from the database
cursor.execute(controlselect)
controlresult = cursor.fetchall()

for result in controlresult:
	cursor.execute(controlresults, result)
	pick = list(cursor.fetchone())
	cntrl.append(pick)


#Carrys out water, negative and threshold plate checks. 
controlqc(cntrl)

#Carrys out Baseline calculations and checks. 

for row in std:
	temparray = []
	if row[1] == 1 or row[1] == 8:
		if row[2] == 1 or row[2] == 3:
			temparray.append(row[4])
			ablgusct = temparray[0]
		if row[2] == 2:
			temparray.append(row[4])
			bcrct = temparray[0]

for row in cntrl:
	temparray = []
	if row[1] == 3 and row[2] == 1 or row[2] == 3:
		temparray.append(row[10])
		ablgusbaseline = temparray[0]
	if row[1] == 3 and row[2] == 2:
		temparray.append(row[10])
		bcrbaseline = temparray[0]

bcrbaseline3 = bcrct - bcrbaseline 
ablgusbaseline3 = ablgusct - ablgusbaseline

if bcrbaseline3 >=3 and bcrbaseline3 <=4:
	bcrplateqc.append(1)
else:
	bcrplateqc.append(2)

if ablgusbaseline3 >=3 and ablgusbaseline3 <=4:
	ablgusplateqc.append(1)
else:
	ablgusplateqc.append(2)

#Carrys out Pos Delta CT calculations and checks. 

temparray1 = []
temparray2 = []
for row in cntrl:
	if row[1] == 1:
		if row[2] == 1 or row[2] == 3:
			temparray1.append(row[4])
		if row[2] == 2:
			temparray2.append(row[4])
ablguspos = temparray1[2] - temparray1[0]
bcrpos = temparray2[2] - temparray2[0]

if ablguspos <= 0.5 and ablguspos >=0.001:
	ablgusplateqc.append(1)
else:
	ablgusplateqc.append(2)

if bcrpos <= 0.5 and bcrpos >=0.001:
	bcrplateqc.append(1)
else:
	bcrplateqc.append(2)

#Calculates replicate ct results and checks 20/50 and standard curve points
calculatereplicatect(std)


#Selects curve for analysis and calculates the slope, intercept and correlation of the curve and checks.
curveselect = []
for row in std:
		if row[2] == 1 or row[2] == 3:
			curveselect.append(row)
			ablgusstdcurve.append(row[5])
		else:
			bcrstdcurve.append(row[5])

for row in curveselect:
	a = []
	b = []
	if row[1] == 14:
		if row[6] == 20:
			curve = 7
		else:
			curve = 8
	if row[1] == 7:
		if row[6] == 50:
			curve = 8
		elif row[6] == 20:
			curve = 7
		else:
			curve = 9

cursor.execute(standardcurveselect, (curve,))
stdcurve = list(cursor.fetchone())
del stdcurve[0:2]

bcrslope, bcrintercept, bcrr_value, p_value, std_err = stats.linregress(stdcurve, bcrstdcurve)
ablgusslope, ablgusintercept, ablgusr_value, p_value, std_err = stats.linregress(stdcurve, ablgusstdcurve)


if ablgusslope <=3.6 and ablgusslope >=3.2:
	ablgusplateqc.append(1)
else:
	ablgusplateqc.append(2)

if bcrslope <=3.6 and bcrslope >=3.2:
	bcrplateqc.append(1)
else:
	bcrplateqc.append(2)

if ablgusr_value > 0.98:
	ablgusplateqc.append(1)
else:
	ablgusplateqc.append(2)

if bcrr_value > 0.98:
	bcrplateqc.append(1)
else:
	bcrplateqc.append(2)


#Pass/Fail Plate Result check 

plateqc = bcrplateqc + ablgusplateqc 
bcrplateqc.append(2)
ablgusplateqc.append(4)
totalplateqc.append(bcrplateqc)
totalplateqc.append(ablgusplateqc)

if 2 in plateqc:
	plateresult = 2
else:
	plateresult = 1

#Adds all results to the database 
for result in replicatectresult:
 	cursor.execute(insertreplicatect, result)

cursor.execute("""
	       INSERT INTO standardcurvecriteria(resulttypeid, slope, correlation, intercept, baseline3, posdeltact, plateid)
	       VALUES (%s, %s, %s, %s, %s, %s, (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1));
	       """ % (2, bcrslope, bcrr_value, bcrintercept, bcrbaseline3, bcrpos,))

cursor.execute("""
	       INSERT INTO standardcurvecriteria(resulttypeid, slope, correlation, intercept, baseline3, posdeltact, plateid)
	       VALUES (%s, %s, %s, %s, %s, %s, (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1));
	       """ % (4, ablgusslope, ablgusr_value, ablgusintercept, ablgusbaseline3, ablguspos,))

for row in totalplateqc:
	cursor.execute(insertplateqcresults, row)

cursor.execute(insertqcresult, (plateresult,))

#Commits results to database
cnx.commit() 


