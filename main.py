import functions as funcs
import pandas as pd
import os
import re
import time
import json

# student name, id, and email
student_info = pd.read_csv('student_info.csv')
student_info = student_info.assign(student=student_info.Student,
                                   id=student_info.ID,
                                   email=student_info['E-mail Address'])[['student', 'id', 'email']]
# grade homework
hw_files = os.listdir('homework')
# SMTP server info
with open('secret.json') as f:
    secret = json.load(f)
sender_email = secret['sender_email']
sender_password = secret['sender_password']
host = "smtp.aol.com"
port = 465
# loop through graded homework and send email
for hw_file in hw_files:
    try:
        student_no = int(re.findall('[0-9]{7}', hw_file)[0])
        name = student_info.loc[student_info.id == student_no, 'student'].values[0]
        email = student_info.loc[student_info.id == student_no, 'email'].values[0]
        subject = 'Your graded homework/exam'
        body = 'Hi, ' + name + \
               "\n\n A graded item (homework or exam) is attached.\n\n" \
               "Please don't reply to this email. " \
               "It is not moniotored and only serves as an email server.\n\n" \
               + "Zhan Li"
        funcs.send_email(email, subject, body, 'homework/' + hw_file, sender_email, sender_password, host, port)
    except IndexError as e:
        print(e)
    time.sleep(60)
