import PySimpleGUI as sg
from datetime import date
import os

sg.change_look_and_feel('DarkGrey')   #change color theme

#get date info
today = date.today()
dayInWeek = today.strftime('%A')

#layout
layout =  [[sg.Text('Today\'s Tasks:', font='Helvetica 15')]]  #title with formatted dates
layout += [[sg.Text(f'{i}',size=(7,1)), sg.CBox(''), sg.Input()] for i in range(1, 6)]  #checks and Tasks
layout += [[sg.Button('Save Changes'), sg.Button('Reload'), sg.Button('Close')]]  #control buttons

#check for saved file
window = sg.Window('Laptop Scheduler', layout, finalize=True)
if os.path.exists(f'./{dayInWeek}.out'):
    window.load_from_disk(f'{dayInWeek}.out')

#event loop
while True:
    event, values = window.read()
    if event in (None, 'Close'):
        break
    elif event == 'Save Changes':
        window.save_to_disk(f'{dayInWeek}.out')
    elif event == 'Reload':
        window.load_from_disk(f'{dayInWeek}.out')
window.close()
