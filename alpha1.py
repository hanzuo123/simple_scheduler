import PySimpleGUI as sg

sg.ChangeLookAndFeel('DarkBlue')

layout = [ [sg.Text('Today\'s Tasks', size=(32,1), font=('Helvetica', 20))],
           [sg.Text('1', size=(10,1)), sg.Checkbox(''), sg.InputText(key='1')],
           [sg.Text('2', size=(10,1)), sg.Checkbox(''), sg.InputText(key='2')],
           [sg.Submit(), sg.Cancel()]
           ]

window = sg.Window('alpha1', layout)        #.Layout(layout)
while True:
    button, values = window.Read()
    print(button, values)
    if button in (None, 'Cancel'):
        break
    elif button in ('Submit'):
        sg.Popup('You entered:', values)

window.close()
