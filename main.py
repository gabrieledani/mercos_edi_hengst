import processa_file_pdf
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

dir_pdf = config['CAMINHO_PDF']['dir_pdf']
dir_edi = config['CAMINHO_EDI']['dir_edi']

for file in os.listdir(dir_pdf):
    if file.endswith(".pdf"):
        print(file)
        processa_file_pdf.processa_file(file,dir_edi,dir_pdf)
        os.rename(os.path.join(dir_pdf,file) , os.path.join(dir_pdf,file+'_ok'))

for file in os.listdir(dir_edi):
    if file.endswith(".dir"):
        print(file)

