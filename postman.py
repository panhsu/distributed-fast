import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication 
from os.path import basename
from email.utils import COMMASPACE, formatdate
import os


class postman():
    
    def __init__(self):
        self.server = smtplib.SMTP('company.smtp.server')
        self.usename = ""
        self.password = ""
    
   
            
    def mail_attachment(self,subject,receivers,filepath,html_content):
       
        # Construct email
        msg = MIMEMultipart()
        msg['From'] = "Team Name"
        msg['To'] = receivers
        msg['Subject'] = subject
        for file in filepath:
            if file is not None:
                with open(file, "rb") as attachment:
                    body = attachment.read()
                    msg.attach(MIMEApplication(body,Content_Disposition='attachment; filename="%s"' % basename(file),Name=basename(file)))
                attachment.close()	
        msg.attach(MIMEText("<html>"+str(html_content)+"</html>", 'html'))
        text = msg.as_string()
        self.server.sendmail("AEGIS", receivers.split(";"), text)
        #if filepath is not None:
        #   attachment.close()

if __name__ =="__main__":
    filepath = "xxx.html"
    filename = basename(filepath)
    title = os.path.splitext(filename)[0]
    result = "(0)"
    build = "7.0"
    subject = "["+build+"] "+"FAST Report:"+title+result
    sender = postman()
    sender.mail_attachment(subject,'xxx@email.com',filepath,filepath)
