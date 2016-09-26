#!/usr/bin/python

import smtplib
import time
from email.mime.text import MIMEText
from socket import socket

host = "SET_ME"
hostname = "SET_ME"
port = 25
encoding = "UTF-8"
timeout = 10
fallbackMail = "mail@fallback" #Edit this with your own mail
fallbackHost = "localhost" #And mail server
logFile = "/var/log/smtp_tester.log"

mailTemplate = "The mail server %s doesn't seems to be responding. The mail testing script reported this error : %s"

def send_mail(error):
    msg = MIMEText(mailTemplate %(host, error))
    msg['Subject'] = '[%s][Error Reported on SMTP server]' %hostname
    msg['From'] = "server@hostname"
    msg['To'] = fallbackMail
    s = smtplib.SMTP(fallbackHost)
    s.sendmail(msg['From'], fallbackMail, msg.as_string())
    s.quit()

def write_log(message):
    date = time.strftime("%H:%M:%S")
    data = "[%s] : %s\n" %(date, message)
    with open(logFile, "a+") as f:
        f.write(data)
    
def test(s):
    try:
        s.connect((host, port))
        string = "HELO %s\n" %hostname
        data = s.recv(1024)
        s.send(string.encode())
        data = s.recv(1024).decode(encoding)
        if not data.startswith("250"):
            return False, data
        else:
            return True, data
    except Exception as e:
        return False, str(e)

def main():
    s = socket()
    s.settimeout(timeout)
    status, message = test(s)
    if status is False:
        write_log(message)
        return send_mail(message)
    return 0

if __name__ == "__main__":
    main()
