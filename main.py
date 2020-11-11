import functions as funcs
import pandas as pd
import os
import re
import time
import json
import random
import smtplib

# student name, id, and email
student_info = pd.read_csv('student_info.csv')
student_info = student_info.assign(student=student_info.Student,
                                   id=student_info.ID.astype(int),
                                   email=student_info['E-mail Address'])[['student', 'id', 'email']]
#------------------------------------
# initialize parameters
## grade homework folder
hw_dir = 'homework/'
## SMTP server info
with open('secret.json') as f:
    secret = json.load(f)
sender_email = secret['sender_email']
sender_password = secret['sender_password']
host = "smtp.aol.com"
port = 465
## pause time betwee loops
time_pause = random.randrange(30, 90)
#------------------------------------
# loop through graded homework and send email
for hw_file in os.listdir(hw_dir):
    try:
        student_no = int(re.findall('[0-9]{7}', hw_file)[0])
        name = student_info.loc[student_info.id == student_no, 'student'].values[0]
        email = student_info.loc[student_info.id == student_no, 'email'].values[0]
        subject = 'Your graded homework'
        body = 'Hi, ' + name + \
               "\n\n You followed the insturction to correctly name your " \
               "homework, and my Python program succesfully matched your homework with your email address." \
               "Your graded homework is thus attached.\n\n" \
               "Please don't reply to this email. " \
               "It is not moniotored and only serves as an email server.\n\n" \
               + "Zhan Li"
        funcs.send_email(email, subject, body, hw_dir + hw_file, sender_email, sender_password, host, port)
        print(f'Email sucessfully sent to {name}!')
    except (IndexError, smtplib.SMTPSenderRefused) as e:
        print(e)
    time.sleep(time_pause)
