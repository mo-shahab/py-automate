import requests

from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

now = datetime.datetime.now()

#email content placeholder
content = ""


def extract_news(url):
    print("Extracting Hacker News stories......")
    cnt = ''
    cnt += ('<b>HN Top Stories: <b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'yalign': ''})):
        cnt += ((str(i+1)+' :: ' + tag.text + '\n' + '<br>') if tag.txt != "More" else '')
    return cnt

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-----------<br>')
content += ('<br><br>End of the Message')

# this shit is sending the email and all
print("Composing Email")

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = "your email id" # put your email id and all
TO = "the address to which you are sending to " # could be a list and all
PASS = "*****" # i would have pushed my stuff to git without even knowing that passwords are a thing and all


msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initialising Server....')

server = smtplib.SMTP(SERVER, PORT) #this shit didnt work for the first time i debugged, like not exactly and all so yeah
server.connect(SERVER,587) 
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.ehlo()

server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()

