#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header


def sendMail(argv):
    print(argv[0], argv[1])
    user = "mafengwo_dev@sina.com"
    pwd = "c21bb77fb5ef1bf5"
    to = ['guoyanchen@mafengwo.com']
    msg = MIMEMultipart()

    msg['Subject'] = Header('task failed', 'utf-8')
    msg['From'] = Header(user)

    s = 'IP: ' + str(argv[0]) + '\n' +'ErrorInfo: ' + str(argv[1])
    content1 = MIMEText(s, 'plain', 'utf-8')
    msg.attach(content1)

    s = smtplib.SMTP('smtp.sina.com')
    s.starttls()
    s.login(user, pwd)
    s.sendmail(user, to, msg.as_string())
    to = ['chenya@mafengwo.com']
    time.sleep(5)
    s.sendmail(user, to, msg.as_string())
    s.close()
