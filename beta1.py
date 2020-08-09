import PySimpleGUI as sg
from datetime import date, datetime
import os
import csv

#magic constant to control how many inputs exist
numTasks = 6 #true number of tasks bc +1 in range()

#get date info
today = date.today()
dayInWeek = today.strftime('%A')
monthDay = today.strftime('%m/%d')
monDayYr = today.strftime('%m/%d/%Y')

def main():
    '''Returns nothing, generates the layouts, window, and runs the event loop (blocking)'''
    sg.change_look_and_feel('Topanga')  #change color theme
    btnStyle = {'border_width':0}
    chBoxStyle = {'tooltip':'mark box once adjacent task is completed'}
    inTxtStyle = {'tooltip':'input task name and details here', 'border_width':0}

    #layout
    layout =  [[sg.Text(f'{dayInWeek} Tasks:', font='Helvetica 15')]]  #title with day in week
    #checks and tasks with a comprehension and two string interpolations to generate the keys
    layout += [[sg.Text(f'{i}. '), sg.Checkbox('', key=f'task_completion_{i}',**chBoxStyle), sg.InputText(key='task_{}_name'.format(i),**inTxtStyle)] for i in range(1,numTasks+1)]
    layout += [[sg.Button('Save Changes',**btnStyle), sg.Button('Reload Save',**btnStyle), sg.Button('Clear Checks',**btnStyle), sg.Button('Close',**btnStyle)]]  #control buttons

    #check for saved file
    window = sg.Window(f'Simple Scheduler ({monthDay})', layout, alpha_channel=.96, finalize=True)  #removed grab_anywhere due to buggy behavior
    #.out naming convention is the day in the week+.out
    if os.path.exists(f'./{dayInWeek}.out'):
        load(window)

    #event loop
    while True:
        event, values = window.read()
        if event in (None, 'Close'):
            break
        elif event == 'Save Changes': #two mechanisms .out and .csv
            #save in the .out file
            save(window)
            #save to the .csv file
            write_csv(values)
        elif event == 'Reload Save':
            load(window)
        elif event == 'Clear Checks':
            clearChecks(window)
    window.close()

def save(window):
    '''Returns nothing, uses builtin save_to_disk() fcnt
    :param window: window object to save to .out file
    :type window: sg.Window() object'''
    window.save_to_disk(f'{dayInWeek}.out')

def clearChecks(window):
    '''Returns nothing, loops through and updates check values to false
    :param window: window object to clear checkboxes from
    :type window: sg.Window() object'''
    for i in range(1,numTasks+1):
        window.FindElement(f'task_completion_{i}').update(value=False)

def load(window):
    '''Returns nothing, loads with built-in fnct then determines whether checks should be cleared
    :param window: window object to load saved .out
    :type window: sg.Window() object'''
    #built-in load function from .out file
    window.load_from_disk(f'{dayInWeek}.out')
    #try to read the .csv file to see whether checks should be cleared
    try:
        with open('task_log.csv', 'r') as fin:
            cin = csv.reader(fin)
            logDate = [row for row in cin][-1][2]  #read the date from the last task
        todayFormatted = [int(i) for i in monDayYr.split('/')] #turn into list of ints for comparison
        logDateFormat = [int(i) for i in logDate.split('/')]

        #compare datetime objects in y/m/d format if today is greater then clear the checks
        if datetime(todayFormatted[2],todayFormatted[0],todayFormatted[1])>datetime(logDateFormat[2],logDateFormat[0],logDateFormat[1]):
            clearChecks(window)
    #catch errors when .csv does not exist
    except:
        sg.popup('Error reading csv file')

def write_csv(taskDict):
    '''Returns nothing but may return to end fnct, appends task status to the csv given data non-redundant
    :param taskDict: dictionary {str:bool,str:str,str:str} {'checked':bool,'task name':str,'converted date':str}
    :type taskDict: dictionary with {str:bool,str:str,str:str} setup'''
    #turn task values into list of dicts
    task_log = [{'task_completion':str(list(taskDict.values())[i]), 'task_name':list(taskDict.values())[i+1], 'date':monDayYr} for i in range(0,numTasks*2,2)]
    #check if the task_log has already been written in the .csv
    try:
        with open('task_log.csv', 'r') as fin:
            cin = csv.DictReader(fin, fieldnames=['task_completion','task_name','date'])
            lastSave = [row for row in cin][-numTasks:]  #get the last saved task_log
        #if equivalent then inform user and return to exit fnct
        if task_log==lastSave:
            sg.popup('Already saved')
            return
    #catch errors by passing
    except:
        pass
    #save the task_log
    with open('task_log.csv', 'a+', newline='') as fout:
        #fieldnames are the headers and may write in redundantly
        cout = csv.DictWriter(fout, ['task_completion','task_name', 'date'])
        cout.writeheader()
        cout.writerows(task_log)
    sg.popup('Changes saved')

#only runs main() when launched as a standalone program
if __name__=='__main__':
    main()
