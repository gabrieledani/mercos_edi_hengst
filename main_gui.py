import PySimpleGUI as sg
import processa_file_pdf

sg.theme("DarkBlue3")
sg.set_options(font=("Microsoft JhengHei", 12))

layout = [
            [
                sg.Text('Arquivo PDF do Pedido:'),
                sg.Input(key='-INPUT-'),
                sg.FileBrowse('Buscar',file_types=(("PDF Files", "*.pdf"), ("ALL Files", "*.*")))
            ],
            [
                sg.Text('Pasta Destino EDI:'),
                sg.Input(key='-PASTA-'),
                sg.FolderBrowse('Buscar')
            ],
            [sg.Button("Gerar Arquivos"),sg.Button("Sair")],
            [sg.Text('',key='atualiza')]
        ]
window = sg.Window('Geração de Arquivos para EDI Hengst Indústria de Filtros', layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED,'Sair'):
        break
    elif event == 'Gerar Arquivos':
        filename = values['-INPUT-']
        
        dir_edi = values['-PASTA-']
        print(filename,dir_edi)
        
        processa_file_pdf.processa_file(filename,dir_edi,'')
        
        window['atualiza'].Update('Arquivo gerado com sucesso!')

window.close()