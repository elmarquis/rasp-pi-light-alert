#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import datetime
import smtplib
from email.message import EmailMessage

#CONFIG
from_email_addr = "gmail email address"
from_email_password = "application password (from gmail)"
to_email_addr = "to address"
email_subject = "Solar inverter error"
email_body = "Reset the solar inverter"


GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

inverterError = False

def send_email():
        #create a message object
        msg = EmailMessage()
        #set the email body
        msg.set_content(email_body)
        #set sender and recipient
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr
        #set your email subject
        msg['Subject'] = email_subject
        #connect to server and send email
        #edit this line with your provider's SMTP server details
        server = smtplib.SMTP('smtp.gmail.com', 587)
        #comment out this line if your provider doesn't use TLS
        server.starttls()
        server.login(from_email_addr, from_email_password)
        server.send_message(msg)
        server.quit()

def logMessage(message):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(timestamp+" "+message)
        # write to log file
        with open("/home/pi/light_alert.log", "a") as log:
                log.write(timestamp+" "+message+"\n")


while True:
        errorLightOn = True if GPIO.input(4) == 0 else False

        if errorLightOn == True and inverterError == False:
                logMessage("Inverter error")
                send_email()
                inverterError = True
        if errorLightOn == False and inverterError == True:
                logMessage("Inverter reset")
                inverterError = False
        time.sleep(5)
