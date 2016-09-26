#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText
from socket import socket

host = "2.lp1.eu"
hostname = "lp1.eu"
port = 25
encoding = "UTF-8"
timeout = 10
fallbackMail = "bad633k@gmail.com"
fallbackHost = "localhost"

mailTemplate = "The mail server %s doesn't seems to be responding. The mail testing script reported this error : %s"

def send_mail(error):
    msg = MIMEText(mailTemplate %(host, error))
    msg['Subject'] = '[%s][Error Reported on SMTP server]' %hostname
    msg['From'] = "server@hostname"
    msg['To'] = fallbackMail
    s = smtplib.SMTP(fallbackHost)
    s.sendmail(me, [you], msg.as_string())
    s.quit()

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
        return send_mail(message)
    else:
        print("status is true "+message)
    return 0

if __name__ == "__main__":
    main()
