#***** SQL statements for use in script ******

#SQL statements for inserting results into DB			
#Inserts Control Results into database. 
controlinsert1 = (""" 
		INSERT INTO controlresults(wellnumber, resulttypeid, controlct, controlctmean, controlquant, controlquantmean,     			controlctthresh, controlbasestart, controlbaseend, controltypeid)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""")
		
controlinsert2 = ("""
		  INSERT INTO plate2control(controlresultid, plateid) 
		  VALUES (LAST_INSERT_ID(), (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1));
 		  """)

#Inserts Standard Results into database
standardinsert1 = ("""  
		 INSERT INTO standardresults(wellnumber, resulttypeid, standardct, standardctmean, standardquant, standardquantmean, 			 standardctthresh, standardbasestart, standardbaseend, standardtypeid)
		 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""")

standardinsert2= ("""
		 INSERT INTO plate2standard(standardresultid, plateid)
		 VALUES (LAST_INSERT_ID(), (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1));
		 """)

#Inserts sample results into the database
sampleinsert1 = ("""
		INSERT INTO sampleresult(wellnumber, samplect, samplectmean, samplequant, samplequantmean, 			     			samplectthresh, samplebasestart, samplebaseend, resulttypeid)
        	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""")

sampleinsert2 = ("""
		INSERT INTO sampleseg(sampleresultid, sampleid, plateid)
		VALUES (LAST_INSERT_ID(), (SELECT sampleid FROM samples WHERE samplenumber= %s), (SELECT plateid FROM plate ORDER BY 			plateid DESC LIMIT 1));
		""") 

#SQL statements for Plate QC
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

