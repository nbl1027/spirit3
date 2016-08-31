from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4 
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from spirit3.models import Patientinfo
from reportlab.lib import colors


#c = canvas.Canvas("hello.pdf")
#c.drawString(100,750,"Welcome to Reportlab!")
#c.showpage()
#c.save()

def plateqcreport(plateid):
	c = canvas.Canvas("(plateid).pdf")
	c.showpage()
 	c.save()





#class MyPrint:
	#def __init__(self, buffer, pagesize):
		#self.buffer = buffer
		#if pagesize == 'A4':
			#self.pagesize = A4
		#elif pagesize == 'Letter':
			#self.pagesize = letter
		#self.width, self.height = self.pagesize 

	#def print_users(self):
		#buffer = self.buffer
		#doc = SimpleDocTemplate(buffer, 
					#rightMargin=72, 
					#leftMargin=72, 
					#topMargin=72, 
					#bottomMargin=72, 
					#pagesize=self.pagesize)
		#elements = []
		##Pre made style sheet
		#styles = getSampleStyleSheet()
		#styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
		#Draw things on PDF 
		#users = Patientinfo.objects.all()
		#elements.append(Paragraph('Patient List', styles['Heading1']))
		#for i, user in enumerate(users):
			#elements.append(Paragraph(user.initials, styles['Normal']))
		#doc.build(elements)
		#pdf = buffer.getvalue()
		#buffer.close()
		#return pdf 

	
