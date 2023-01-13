# Import libraries
import configparser
import os

import processa_file_pdf

import requests
from bs4 import BeautifulSoup
from imap_tools import MailBox, AND

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

config = configparser.ConfigParser()
config.read('config.ini')

dir_pdf = config['CAMINHO_PDF']['dir_pdf']
dir_edi = config['CAMINHO_EDI']['dir_edi']

sender_email = config['E_MAIL']['sender_email']
receiver_email = config['E_MAIL']['receiver_email']

smtp_server = config['E_MAIL']['smtp_server']
smtp_port = config['E_MAIL']['smtp_port']
imap_server = config['E_MAIL']['smtp_server']

login = config['E_MAIL']['login']
password = config['E_MAIL']['password']

def send_mail(filename,subject,body):

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msg.attach(msgText)

    fil = open(os.path.join(dir_edi,filename), "rb")
    
    part = MIMEApplication(fil.read(),Name=os.path.basename(filename))    
    part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(filename)
    msg.attach(part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(login, password)
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
            return 'success'
    except Exception as e:
        print(e)
        return e


def read_mail():
    # get unseen emails sent by vedafil from INBOX folder
    mailbox = MailBox(imap_server).login(login, password, 'INBOX')

    # *mark emails as seen on fetch, see mark_seen arg
    for msg in mailbox.fetch(AND(from_='vedafil', seen=False)):#,mark_seen=False):  
        subject = msg.subject
        #print(subject)
        
        pedido = subject[subject.find('Nº')+3:subject.find('-')-1] 
        #print(pedido)
        
        body = msg.html
        #print(body)

        soup = BeautifulSoup(body, 'html.parser')

        link = soup.find_all('a')
        # URL from which pdfs to be downloaded
        pdf_file_url = link[1].get('href', [])
        #print(link[1].get('href', []))
        
        text = soup.find_all('div')
        content = text[2].text
        #print(text[2].text)

        # Requests URL and get response object
        response = requests.get(pdf_file_url)

        # Parse text obtained
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all hyperlinks present on webpage
        links = soup.find_all('a')
        i = 0

        # From all links check for pdf link and if present download file
        #for link in links:
        link = links[0]
        if ('.pdf' in link.get('href', [])):
            i += 1
            print("Downloading file: ", i)

            # Get response object for link
            response = requests.get(link.get('href'))

            # Write content in pdf file
            file = pedido+".pdf"
            pdf = open(os.path.join(dir_pdf,file), 'wb')
            pdf.write(response.content)
            pdf.close()
            print("File ", os.path.join(dir_pdf,pedido+".pdf"), " downloaded")

            #Generate EDI from PDF
            edi_filename = processa_file_pdf.processa_file(file,dir_edi,dir_pdf)
            os.rename(os.path.join(dir_pdf,file) , os.path.join(dir_pdf,file+'_ok'))
        
        print(edi_filename,subject,content)
        error = send_mail(edi_filename,subject,content)
        if error == 'success':
            os.rename(os.path.join(dir_edi,edi_filename) , os.path.join(dir_edi,edi_filename+'_ok'))


#Read new e-mails
print('Start')
read_mail()
print('End!')