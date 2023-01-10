import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def send_test_mail(filename):
    body = "Arquivo de Pedido!"
    sender_email = "gabriele.dani@modelovencedor.com.br"
    receiver_email = "gabrieledani@gmail.com"

    msg = MIMEMultipart()
    msg['Subject'] = '[Pedido Vedafil]'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msg.attach(msgText)

    dir_edi = os.getcwd()
    dir_edi = os.path.join(dir_edi,'edi')

    fil = open(os.path.join(dir_edi,filename), "rb")
    part = MIMEApplication(fil.read(),Name=os.path.basename(filename))    
    part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(filename)
    msg.attach(part)

    try:
        with smtplib.SMTP('mail.modelovencedor.com.br', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("gabriele.dani@modelovencedor.com.br", "Science@1984")
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
            return 'success'
    except Exception as e:
        print(e)
        return e
        

#filename = 'EXPORTA_PEDIDO_HENGST_SIGA BEM_1667.dir'
#send_test_mail(filename)
