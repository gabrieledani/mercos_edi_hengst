import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import configparser

def send_test_mail(filename):
    config = configparser.ConfigParser()
    config.read('config.ini')

    dir_edi = config['CAMINHO_EDI']['dir_edi']

    body = 'Arquivo de Pedido!'
    sender_email = config['E_MAIL']['sender_email']
    receiver_email = config['E_MAIL']['receiver_email']
    smtp = config['E_MAIL']['smtp']
    porta = config['E_MAIL']['porta']
    login = config['E_MAIL']['login']
    senha = config['E_MAIL']['senha']

    msg = MIMEMultipart()
    msg['Subject'] = '[Pedido Vedafil]'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msg.attach(msgText)

    fil = open(os.path.join(dir_edi,filename), "rb")
    part = MIMEApplication(fil.read(),Name=os.path.basename(filename))    
    part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(filename)
    msg.attach(part)

    try:
        with smtplib.SMTP(smtp, porta) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(login, senha)
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
            return 'success'
    except Exception as e:
        print(e)
        return e
        

#filename = 'EXPORTA_PEDIDO_HENGST_SIGA BEM_1667.dir'
#send_test_mail(filename)
