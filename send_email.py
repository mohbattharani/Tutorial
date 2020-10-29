import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate
from os.path import basename

COMMASPACE = ', '

class Email_Service ():
    def __init__ (self,sender_email, sender_email_pwd):
        self.port = 465 # 587 #465
        self.sender_email = sender_email
        self.sender_email_pwd = sender_email_pwd
        self.msg = MIMEMultipart()
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', self.port )
        self.server_status = False
        self.config()

    def config (self):       
        self.msg['From'] = self.sender_email
        self.server.ehlo()
        #self.server.starttls()
        try:
            self.server.login(self.sender_email, self.sender_email_pwd)
            self.server_status = True
        except:
            print ('Failed for configure sender email')
      
    def load_images (self, paths):
        paths = list (paths)
        for path in paths:
            img_data = open(path, 'rb').read()
            image = MIMEImage(img_data, name=os.path.basename(path.split('/')[-1]))
            self.msg.attach(image)

    def load_files (self, files):
        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            self.msg.attach(part)

    def send (self, to, subject, body, attachment = None):
        self.msg['To'] = send_to
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body))

        if (attachment is not None):
            self.load_files (attachment)

        if (self.server_status):
            try:
                self.server.sendmail(send_from, send_to, self.msg.as_string())
                self.server.close()
            except Exception as e:
                print ('Please ensure email is configured properly.')
                print ('Exception is:', e)
                self.server_status = False
                return False
        else:
            print ('Please configure email.')
            return False
        return True


send_from = 'abc@gmail.com'
password = 'pwd'
send_to = 'xyz@gmail.com'

subject = 'Test message'
body = 'Body of test message'
images = ['Yolo4/im1.png', 'Yolo4/coco.names']

email_server = Email_Service (send_from, password)
sent = email_server.send (send_to, subject, body, attachment = images)