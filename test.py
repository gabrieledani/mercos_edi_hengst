from imap_tools import MailBox, AND

# get unseen emails sent by good@some.xx from INBOX folder
with MailBox('mail.vedafil.com.br').login('pedidos@vedafil.com.br', 'Vdfil.2022', 'INBOX') as mailbox:
    # *mark emails as seen on fetch, see mark_seen arg
    for msg in mailbox.fetch(AND(from_='vedafil', seen=False),mark_seen=False):  
        
        subject = msg.subject
        print(subject)
        pedido = subject[subject.find('Nº')+3:subject.find('-')-1] 
        #Pedido Nº 1701 - Acessocar - Hengst
        print(pedido)
        html_file = open('body'+pedido+'.html','w')
        body = msg.html
        #print(body)
        html_file.write(body)



