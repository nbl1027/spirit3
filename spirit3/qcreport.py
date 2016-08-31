#This script is used for the automatic generation of a PlateQC PDF report

import mysql.connector
from reportlab.lib import colors, utils
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Frame, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, HexColor
import datetime

#***** Database Connection & Cursor *****
cnx = mysql.connector.connect(user='kirsty', password='ngskirsty_201605', host='10.229.233.250', database = 'spirit3')
cursor = cnx.cursor()

#******* Internal Functions *********

def removeduplicates(values):
	output = []
	seen = set()
	for value in values:
		if value not in seen:
			output.append(value)
			seen.add(value)
	return output


#***** Variables *****
infoplate = []
resulttype = {}
standardtype = {}
controltype = {}
passfail = {}
statements = {}
ablstd = []
bcrstd = []
ablcntrl = []
bcrcntrl = []
authresults = []
IDresults = []
sampleresultid = []
Numdict = {}
IDdict = {}
sampleid = []
aresults = []
ablqc = []
bcrstate = []
sampleauth = []

#***** SQL statements for use in script ******

#Selects Plate ID
plateidselect =("""
		SELECT plateid, dateofrun FROM plate WHERE plateid = (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1);
		""")

#Selects the authorisation info
authselect = ("""
	      SELECT * FROM plateqc WHERE plateid = (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1);
	      """)

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

#Selects sample IDs from plate info 
IDselect = (""" 
	   SELECT * FROM sampleseg WHERE plateid = (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1);
	   """)

#Selects the sample number which corresponds to the the sampleID
SampleIDselect = ("""
		  SELECT samplenumber FROM samples WHERE sampleid = (%s)
		  """)

#Selects the pass/fail
passfailselect = (""" 
		SELECT passfailid FROM plateqcresult WHERE plateid = (SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1);
		""")


def qcreport(csv):
	
	if csv: 
		#Selects plateid and date of run from the DB 
		cursor.execute(plateidselect)
		platei = str(cursor.fetchone())
		plateinfo = platei.split(',')

		#Creates dictionaries of the result types, standard types, control types, result designation and BCR statements.

		cursor.execute(""" SELECT * FROM resulttype; """)
		for row in cursor:
			resulttype[row[0]] = row[1]

		cursor.execute(""" SELECT * FROM standardtype; """)
		for row in cursor:
			standardtype[row[0]] = row[1]

		cursor.execute(""" SELECT * FROM controltype; """) 
		for row in cursor: 
			controltype[row[0]] = row[1]

		cursor.execute(""" SELECT * FROM passfail; """)
		for row in cursor: 
			passfail[row[0]] = row[1]

		cursor.execute(""" SELECT * FROM statements; """)
		for row in cursor:
			statements[row[0]] = row[1]


		#Creates the Pass/Fail and Plate info summary 

		cursor.execute(passfailselect)
		resulto = cursor.fetchone()
		boo = int(resulto[0][0])
		overall = passfail.get(boo)
		plateinfo.append(overall)

		plateinfo[0] = plateinfo[0][1:]
		plateinfo[1] = plateinfo[1][15:]
		plateinfo[2] = plateinfo[2][1:]
		plateinfo[3] = plateinfo[3][1:3]
		d = plateinfo[3]+'/'+plateinfo[2]+'/'+plateinfo[1]
		pid = plateinfo[0] 
		pdesig = plateinfo[4]

		infoplate.append(pid)
		infoplate.append(d)
		infoplate.append(pdesig)

		
		#Selects the samples IDs and result IDs from the DB
		cursor.execute(IDselect)
		ID = cursor.fetchall()
		for row in ID:
			IDresults.append(list(row))
		for row in IDresults:
			IDdict[row[2]] = row[1] #SampleIDs / ResultIDs
			sampleresultid.append(row[2])
			sampleid.append(row[1])
 
		sampleids = removeduplicates(sampleid) #SampleIDs

		#Creates a dictionary of sampleids and sample numbers
		for row in sampleids:
			cursor.execute("""
		  			SELECT samplenumber FROM samples WHERE sampleid = (%s)
		  		       """, ((row,)))
			snum = cursor.fetchone()
			Numdict[row] = snum #SampleIDs/ Sample Numbers


		#Selects authorisation information for standards/controls 

		cursor.execute(authselect)
		authresults1 = (cursor.fetchall())
		for row in authresults1:
			authresults.append(list(row))

		for row in authresults:
			del row[0:2]
			temp = []
			typ = resulttype.get(row[0])
			temp.append(typ)
			for num in row[1:]:
				desig = passfail.get(num)
				temp.append(desig)
			aresults.append(temp)

		#Selects authorisation information for samples

		#Selects ABL QC info
		for row in sampleids: 
			cursor.execute("""
		  		SELECT * FROM ablresutqc WHERE sampleid = (%s)
		  		""", ((row,)))
			aqc = cursor.fetchall()
			newest = list(aqc[-1])
			ablqc.append(newest)

		#Sorts and retrives BCR statement
		for row in ablqc: 
			del row[0]
			temp = []
			sampid = Numdict.get(row[0])
			id2 = str(sampid[0])
			temp.append(id2)
			temp.append(row[1])
			desig = str(passfail.get(row[4]))
			temp.append(desig)
			search = row[0]
			cursor.execute(""" SELECT statementsid FROM resultanalysis WHERE sampleid = (%s)
					""",((search,)))
			res = cursor.fetchall()
			bcrstat = res[-1]
			intbcrstat = bcrstat[0]
			state = str(statements.get(intbcrstat))
			temp.append(state)
			sampleauth.append(temp)

		#Selects relevant standards from the database and sorts 
		cursor.execute(standardselect)
		standardresults = cursor.fetchall()

		for result in standardresults:
			cursor.execute(standardresult, result)	
			pick = list(cursor.fetchone())
			del pick[0]
			if pick[1] == 1 or pick[1] == 3:
				rtype = resulttype.get(pick[1])
				stype = standardtype.get(pick[0])
				pick[1] = rtype
				pick[0] = stype
				ablstd.append(pick)
			else: 
				rtype = resulttype.get(pick[1])
				pick[1] = rtype
				stype = standardtype.get(pick[0])
				pick[0] = stype
				bcrstd.append(pick)

		
		#Selects relevant controls from the database and sorts 

		cursor.execute(controlselect)
		controlresult = cursor.fetchall()

		for result in controlresult:
			cursor.execute(controlresults, result)
			pick = list(cursor.fetchone())
			del pick[0]
			if pick[1] == 1 or pick[1] == 3:
				rtype = resulttype.get(pick[1])
				ctype = controltype.get(pick[0])
				pick[1] = rtype
				pick[0] = ctype
				ablcntrl.append(pick)
			else:
				rtype = resulttype.get(pick[1])
				ctype = controltype.get(pick[0])
				pick[1] = rtype
				pick[0] = ctype
				bcrcntrl.append(pick)



		#***** Table creation for PDF  ******

		#Colours 
		spirit = HexColor('#602060')

		#Table heads 
		platesum = ['Plate ID', 'Date of Run', 'Result']

		authhead = ['', 'H2O Check', 'Neg Check', 'Threshold Setting', 'Baseline Setting', 'POS Control (deltaCt<0.5)', 'STD Curve 20 or 50', 'STD Curve Points', 'Slope >= 3.2 <=3.6', 'Correlation >= 0.98']

		samplehead = ['Sample', 'ABL Quant', 'ABL QC', 'BCR-ABL']

		resulttitle = ['Type', 'Result Type', 'Well', 'Ct', 'Ct Mean', 'Quantity', 'Quantity Mean', 'Ct Threshold', 'Base Start', 'Base End']

		#Creates summary table 
		plateresult = []
		plateresult.append(platesum)
		plateresult.append(infoplate)
		plateresulttable= Table(plateresult, colWidths=(2*inch, 2*inch, 2*inch))
		plateresulttable.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.white), 
					('FONTNAME', (0,0), (2,0), 'Helvetica-Bold'),
					('FONTSIZE', (0,0), (2,1), 8),
	        		       ('TEXTCOLOR',(0,0),(1,-1),colors.black),
				        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
					('BOX', (0,0), (-1,-1), 0.25, colors.black),
					]))

	
		#Creates authorisation table
		authtable = []

		count = 0	
		for row in authhead:
			temp = []
 			temp.append(row)
			for ro in aresults:
				uu = ro[count]
				temp.append(uu)
			authtable.append(temp)
			count += 1

		authorisationtable = Table(authtable, colWidths=(1.25*inch, 0.60*inch, 0.60*inch), hAlign='LEFT')
		authorisationtable.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.white),
					('FONTSIZE', (0,0), (2,9), 6), 
					('FONTNAME', (0,0), (2,0), 'Helvetica-Bold'),
					('FONTNAME', (0,0), (0,9), 'Helvetica-Bold'),
	        		       ('TEXTCOLOR',(0,0),(1,-1),colors.black),
				        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
					('BOX', (0,0), (-1,-1), 0.25, colors.black),
					]))

		#Creates Sample QC Table
		sampleqctab = []
		sampleqctab.append(samplehead)
		for row in sampleauth:
			sampleqctab.append(row)


		sampleqctable = Table(sampleqctab, colWidths=(0.60*inch, 0.60*inch, 0.60*inch, 1.25*inch), hAlign='RIGHT')
		sampleqctable.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.white), 
	        		       ('TEXTCOLOR',(0,0),(1,-1),colors.black),
					('FONTSIZE', (0,0), (-1,-1), 6), 
					('FONTNAME', (0,0), (3,0), 'Helvetica-Bold'),
				        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
					('BOX', (0,0), (-1,-1), 0.25, colors.black),
					]))


		#Creates the QC Summary table
		qcsummary = [[authorisationtable, sampleqctable]]
		shell_table = Table(qcsummary)
		shell_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1,), 'TOP')]))

		#Creates ABL control and standard results tables
		ablstandardtable = []
		ablcontroltable = []

		ablstandardtable.append(resulttitle)
		ablcontroltable.append(resulttitle)
		for row in ablstd:
			ablstandardtable.append(row)
		for row in ablcntrl:
			ablcontroltable.append(row)

		abltablestandard = Table(ablstandardtable, colWidths=(0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.7*inch, 0.65*inch, 0.6*inch, 0.6*inch))
		abltablestandard.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.white), 
	        		       ('TEXTCOLOR',(0,0),(1,-1),colors.black),
					('FONTSIZE', (0,0), (-1,-1), 6), 
					('FONTNAME', (0,0), (9,0), 'Helvetica-Bold'),
				        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
					('BOX', (0,0), (-1,-1), 0.25, colors.black),
					]))

		abltablecontrol = Table(ablcontroltable, colWidths=(0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.7*inch, 0.65*inch, 0.6*inch, 0.6*inch))
		abltablecontrol.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.white), 
	        		       ('TEXTCOLOR',(0,0),(1,-1),colors.black),
					('FONTSIZE', (0,0), (-1,-1), 6), 
					('FONTNAME', (0,0), (9,0), 'Helvetica-Bold'),
				        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
					('BOX', (0,0), (-1,-1), 0.25, colors.black),
					]))


		#Creates BCR control and standard results tables
		bcrstandardtable = []
		bcrcontroltable = []

		bcrstandardtable.append(resulttitle)
		bcrcontroltable.append(resulttitle)
		for row in bcrstd:
			bcrstandardtable.append(row)
		for row in ablcntrl:
			bcrcontroltable.append(row)


		bcrtablestandard = Table(bcrstandardtable, colWidths=(0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.7*inch, 0.65*inch, 0.6*inch, 0.6*inch))
		bcrtablestandard.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.white), 
	               ('TEXTCOLOR',(0,0),(1,-1),colors.black),
			('FONTSIZE', (0,0), (-1,-1), 6), 
			('FONTNAME', (0,0), (9,0), 'Helvetica-Bold'),
		        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
			('BOX', (0,0), (-1,-1), 0.25, colors.black),
			]))

		bcrtablecontrol = Table(bcrcontroltable, colWidths=(0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.7*inch, 0.65*inch, 0.6*inch, 0.6*inch))
		bcrtablecontrol.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.white), 
	        		       ('TEXTCOLOR',(0,0),(1,-1),colors.black),
					('FONTSIZE', (0,0), (-1,-1), 6), 
					('FONTNAME', (0,0), (9,0), 'Helvetica-Bold'),
				        ('INNERGRID',(0,0),(-1,-1), 0.25, colors.black),
					('BOX', (0,0), (-1,-1), 0.25, colors.black),
					]))

		#***** Creates PDF Report ******

		#SetUp
		doc = SimpleDocTemplate("plateqcreport.pdf", pagesize=A4)
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
		styles.add(ParagraphStyle(name='spiritfont', fontSize = 12, alignment = TA_LEFT, textColor = '#602060'))
		header = []
		elements = []

		#Spacers 
		s = Spacer(width=0, height=0.5*inch)
		s2 = Spacer(width=0, height=0.25*inch)
		s3 = Spacer(width=0, height=0.15*inch)
		s4 = Spacer(width=0, height=0.35*inch)

		#Grabs the images needed from the report and creates header by adding them to a table
		Lab = Image('/home/kirsty/SPIRIT3/spirit3/static/images/lab.jpeg',1.5*inch, 0.5*inch)
		Spirit = Image('/home/kirsty/SPIRIT3/spirit3/static/images/logo.jpeg', 1.5*inch, 0.75*inch)
		Trust = Image('/home/kirsty/SPIRIT3/spirit3/static/images/trust.jpeg', 1.75*inch, 0.9*inch)
		CPA = Image('/home/kirsty/SPIRIT3/spirit3/static/images/cpa.jpeg', 0.75*inch, 0.5*inch)
		Add = Image('/home/kirsty/SPIRIT3/spirit3/static/images/add.jpeg', 2*inch, 1*inch)

		header1 = [[Lab, Spirit, Trust]]
		header2 = [[CPA, [], Add]]
		header = header1 + header2

		headtable = Table(header, colWidths = 2*inch)

		#*** Assembles the PDF *****#

		aut = Paragraph("Plate QC",styles['spiritfont'])
		aut2 = Paragraph("Sample QC",styles['spiritfont'])
		qcheader = [[aut, aut2]]
		headshell = Table(qcheader)
		headshell.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 6)]))

		elements.append(headtable)
		elements.append(s)
		elements.append(Paragraph("Quality Control Report",styles['title']))
		elements.append(s2)
		elements.append(plateresulttable)
		elements.append(s)
		elements.append(Paragraph("Authorisation Checklist",styles['title']))
		elements.append(s4)
		elements.append(headshell)
		elements.append(s3)
		elements.append(shell_table)
		elements.append(s2)
		elements.append(Paragraph("ABL/GUS QC Results",styles['Heading2']))
		elements.append(s2)
		elements.append(Paragraph("Standard Results",styles['spiritfont']))
		elements.append(s2)
		elements.append(abltablestandard)
		elements.append(s2)
		elements.append(Paragraph("Control Results",styles['spiritfont']))
		elements.append(s2)
		elements.append(abltablecontrol)
		elements.append(s)
		elements.append(s)
		elements.append(s)
		elements.append(Paragraph("BCR-ABL QC Results",styles['Heading2']))
		elements.append(s2)
		elements.append(Paragraph("Standard Results",styles['spiritfont']))
		elements.append(s2)
		elements.append(bcrtablestandard)
		elements.append(s2)
		elements.append(Paragraph("Control Results",styles['spiritfont']))
		elements.append(s2)
		elements.append(bcrtablecontrol)

		#Builds the PDF
		doc.build(elements)

		#Adds the PDF to the database 
		report = open('plateqcreport.pdf').read()
		qcinsert = (""" INSERT INTO qcreport(plateid, qcreport) 
	    		VALUES ((SELECT plateid FROM plate ORDER BY plateid DESC LIMIT 1), %s);
	    		""")
		cursor.execute(qcinsert, (report,))

		#Commits results to database
		cnx.commit() 

		


