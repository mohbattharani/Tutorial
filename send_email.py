import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
COMMASPACE = ', '

def send_message (send_from, password, send_to, subject, body, images = None):
    #server = setup_server (send_from, password)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
    
    if (images is not None):
        for im_path in images:
            try:
                img_data = open(im_path, 'rb').read()
                image = MIMEImage(img_data, name=os.path.basename(im_path.split('/')[-1]))
                msg.attach(image)
            except:
                print ('failed')
                pass
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(send_from, password)
        server.sendmail(send_from, send_to, msg.as_string())
        server.close()
        return True
    except:  
        return False

send_from = 'abc@gmail.com'
password = 'abc'
send_to = 'xyz@gmail..com'

subject = 'Test message'
body = 'Body of test message'
path = '/Users/cvlab/Desktop/images/'
images = os.listdir (path)[1:-1]
images = [ os.path.join (path, im) for im in images]

import time
t0 = time.time()

status = send_message (send_from, password, send_to, subject, body, images)
print (status)
t1 = time.time()
print ('Total time:', (t1-t0)*1000)