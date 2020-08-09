import PySimpleGUI as sg
from datetime import date
import os

sg.change_look_and_feel('DarkAmber')  #change color theme

#magic constant to control how many inputs exist
numTasks = 6 #true number of tasks bc +1 in range()

#get date info
today = date.today()
dayInWeek = today.strftime('%A')

#layout
layout =  [[sg.Text(f'{dayInWeek} Tasks:', font='Helvetica 15')]]  #title with formatted dates
layout += [[sg.Text(f'{i}',size=(4,1)), sg.Checkbox('', key=f'box{i}'), sg.InputText(key=i)] for i in range(1,numTasks+1)] #checks and tasks
layout += [[sg.Button('Save Changes'), sg.Button('Reload'), sg.Button('Clear Checks'), sg.Button('Close')]]  #control buttons

#check for saved file
window = sg.Window(f'Laptop Scheduler', layout, finalize=True)
if os.path.exists(f'./{dayInWeek}.out'):
    window.load_from_disk(f'{dayInWeek}.out')

#event loop
while True:
    event, values = window.read()
    if event in (None, 'Close'):
        break
    elif event == 'Save Changes':
        window.save_to_disk(f'{dayInWeek}.out')
        sg.popup('Changes Saved')
    elif event == 'Reload':
        window.load_from_disk(f'{dayInWeek}.out')
    elif event == 'Clear Checks':
        for i in range(1,numTasks+1):
            window.FindElement(f'box{i}').update(value=False)
window.close()
