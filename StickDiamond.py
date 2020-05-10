import configure
import tkinter as tk
from tkinter import messagebox
import random
import itertools
import requests
import sys, os
import string

import threading
import Speech_to_Text


subscription_key = "" # Enter azure key # Regenerate before leaving

with open('command.txt','w+') as f:
    f.close()

def get_rand_offset():
    offset = [100,-100]
    random.shuffle(offset)
    return offset[0]

control_lines = dict()
w = None
h = None
line_lst = list()
plot_dimension = {'width':0, 'height':0}



def create_grid_and_control_lines(event=None):
    global control_lines, w, h, line_lst, plot_dimension
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    #c.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, 100):
        c.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, 100):
        c.create_line([(0, i), (w, i)], tag='grid_line')

    plot_dimension['width'] = w//100
    plot_dimension['height'] = h//100

    print(plot_dimension)
    
    choices = list(itertools.product(range(0, w - 100, 100), range(0, h - 100, 100)))
    random.shuffle(choices)

    j = 0
    count = 0
    colour = ['red','green','blue','gold']
    random.shuffle(colour)
    
    while j < 4:
        origin_x, origin_y = choices[0]
        end_x, end_y = -1, -1
        random.shuffle(choices)

        while(end_x < 0 or end_y < 0):
            end_x, end_y = origin_x + get_rand_offset(), origin_y + get_rand_offset()

        if({(origin_x, origin_y), (end_x, end_y)} in line_lst):
            print("fail")
            continue

        ID = c.create_line([(origin_x, origin_y), (end_x, end_y)], tag = colour[j] + '_line', fill = colour[j], width = 10)
        line_lst.append({(origin_x, origin_y), (end_x, end_y)})
        
        control_lines[colour[j] + '_line'] = ID
        
        j += 1
    ##print(c.find_withtag("control_line_1"))


def rotate(ele):
    #print("hi")
    ID = control_lines[ele]

    x1,y1,x2,y2 = c.coords(ID)
    old_coords = {(x1,y1),(x2,y2)}

    if(y2 > y1):
        y2 -= 100
        y1 += 100
    else:
        y1 -= 100
        y2 += 100

    new_coords = {(x1,y1),(x2,y2)}

    if(new_coords in line_lst):
        return

    c.coords(control_lines[ele], x1, y1, x2, y2)

    line_lst.remove(old_coords)
    line_lst.append(new_coords)


def translate(ele, direction, val):    

    ID = control_lines[ele]
    
    x1, y1, x2, y2 = c.coords(ID)
    old_coords = {(x1,y1),(x2,y2)}

    disp = int(val) * 100

    if(direction == "up" and min(y1,y2) - disp >= 0 and {(x1, y1 - disp), (x2, y2 - disp)} not in line_lst):
        c.move(ID, 0, -disp)

    elif(direction == "down" and max(y1,y2) + disp <= h and {(x1, y1 + disp), (x2, y2 + disp)} not in line_lst):
        c.move(ID, 0, disp)

    elif(direction == "right" and max(x1,x2) + disp <= w and {(x1 + disp, y1), (x2 + disp, y2)} not in line_lst):
        c.move(ID, disp, 0)

    elif(direction == "left" and min(x1,x2) - disp >= 0 and {(x1 - disp, y1), (x2 - disp, y2)} not in line_lst):
        c.move(ID, -disp, 0)

    new_coords = {(c.coords(ID)[0],c.coords(ID)[1]), (c.coords(ID)[2],c.coords(ID)[3])}

    line_lst.remove(old_coords)
    line_lst.append(new_coords)

def operate_game_by_command(x):
    global subscription_key
    try:
        command = str(x).replace('&','and').replace(' a ',' 1 ')
        r = requests.get(f'https://centralindia.api.cognitive.microsoft.com/luis/v2.0/apps/67ec9d8b-fed1-4ded-a47d-c76f07d5ef93?verbose=true&timezoneOffset=0&subscription-key=' + subscription_key + '&q=' + command)
        result = r.json()
        print(result)
    except Exception as e:
        print(f'{e}')
    #result = {'query': 'move red line rightwards by 1 block and then rotate the blue line.', 'topScoringIntent': {'intent': 'move', 'score': 0.982636154}, 'intents': [{'intent': 'move', 'score': 0.982636154}, {'intent': 'rotate', 'score': 0.151299834}, {'intent': 'None', 'score': 0.00239448785}], 'entities': [{'entity': 'red', 'type': 'colour', 'startIndex': 5, 'endIndex': 7, 'score': 0.9873937}, {'entity': 'blue', 'type': 'colour', 'startIndex': 56, 'endIndex': 59, 'score': 0.998382449}, {'entity': 'rightwards', 'type': 'direction', 'startIndex': 14, 'endIndex': 23, 'score': 0.9956634, 'role': 'right'}, {'entity': '1', 'type': 'builtin.number', 'startIndex': 28, 'endIndex': 28, 'resolution': {'subtype': 'integer', 'value': '1'}}]}

    intent = list()

    '''temp = (requests.get(f'https://centralindia.api.cognitive.microsoft.com/luis/v2.0/apps/9add54d5-3a9a-4315-b153-daa4c53395ad?verbose=true&timezoneOffset=0&subscription-key=' + subscription_key + '&q=' + command)).json() #update
    print(temp)
    flag = None
    
    if(temp['topScoringIntent']['intent'] == 'MoveAndRotate'):
        flag = True'''
    
    '''for ele in result['intents']:
        if(flag and (ele['intent'] == "move" or ele['intent'] == "rotate")):
            intent.append(ele['intent'])
        elif(ele['intent'] == "move" or ele['intent'] == "rotate"):
            intent.append(ele['intent'])
            break
        else:
            break'''

    intent.append(result['topScoringIntent']['intent'])

    colour = list()
    direction = list()
    magnitude = list()

    for ele in result['entities']:
        if(ele['type'] == 'colour'):
            colour.append(ele['role'])
        elif(ele['type'] == 'direction'):
            direction.append(ele['role'])
        elif(ele['type'] == 'builtin.number'):
            magnitude.append(ele['resolution']['value'])

    #print(intent,colour,direction,magnitude)

    processed_x = x.translate(str.maketrans('', '', string.punctuation)).split()
    
    if(colour == [] and ('all' in processed_x or 'every' in processed_x)):
        colour = ['red','green','blue','gold']

    if(direction == [] and magnitude == []):
        if('top' in x.lower()):
            direction = ['up']
        if('bottom' in x.lower()):
            direction = ['down']
        if('rightmost' in x.lower()):
            direction = ['right']
        if('leftmost' in x.lower()):
            direction = ['left']
        for ele in colour:
            x1,y1,x2,y2 = c.coords(control_lines[ele + '_line'])
            if(direction == ['up']):
                magnitude.append(max(y1,y2)/100 - 1)
            elif(direction == ['down']):
                magnitude.append(plot_dimension['height'] - max(y1,y2)/100)
            elif(direction == ['right']):
                magnitude.append(plot_dimension['width'] - max(x1,x2)/100)
            elif(direction == ['left']):
                magnitude.append(max(x1,x2)/100 - 1)

    elif('extreme' in x.lower()):
        for ele in colour:
            x1,y1,x2,y2 = c.coords(control_lines[ele + '_line'])
            if(direction == ['up']):
                magnitude.append(max(y1,y2)/100 - 1)
            elif(direction == ['down']):
                magnitude.append(plot_dimension['height'] - max(y1,y2)/100)
            elif(direction == ['right']):
                magnitude.append(plot_dimension['width'] - max(x1,x2)/100)
            elif(direction == ['left']):
                magnitude.append(max(x1,x2)/100 - 1)
        
    elif(magnitude == []):
        magnitude = [1]

    print('magnitude-',magnitude)

    if(len(intent) == 0 or len(colour) == 0 or ('move' in intent and (len(direction)== 0 or len(magnitude) == 0))):
        num_of_ops = 0
    else:
        if(intent == ['move']):
            num_of_ops = max(len(magnitude),len(colour),len(direction))
        elif(intent == ['rotate']):
            num_of_ops = len(colour)
        else:
            num_of_ops = 0
        '''if('rotate' in intent):
            num_of_ops += 1'''
        
    print(intent,colour,direction,magnitude)
    
    data = [intent, colour, direction, magnitude]

    command_colours_num = len(colour)

    for i in range(num_of_ops):

        if(data[0][0] == 'move'):
            translate(data[1][0] + '_line', data[2][0], data[3][0])
            for j in range(1,4):
                if(j == 1 and (((i + 1) % round(num_of_ops/command_colours_num)) != 0)):
                    continue
                if(len(data[j]) > 1):
                    del data[j][0]
            '''if(data[3] == []):
                del data[0][0]'''

        else:
            rotate(data[1][0] + '_line')
            if(len(data[1]) > 1):
                del data[1][0]
                     
root = tk.Tk()

#win1 = tk.Toplevel(root)
c = tk.Canvas(root, bg='white')
root.wm_attributes('-fullscreen','true')
c.pack(fill=tk.BOTH, expand=True)

win2 = tk.Toplevel(root)
win2.resizable(0,0)
win2.transient(root)
win2.title('Game Controller')
win2.attributes("-topmost",True)

win2.geometry(str(root.winfo_screenwidth()) + "x" + str(round(root.winfo_screenheight()*0.028)) + "+" + str(0) + "+" + str(round(root.winfo_screenheight()*0.938)))

e = tk.Entry(win2, font = "Helvetica 20 bold")
e.place(relwidth=0.9, relheight=1)


win_img = tk.PhotoImage(file = 'win.ppm')

previous_commands = list()

def exit_game():
    global root
    Speech_to_Text.record_mic_voice.flag = 'stop'
    root.destroy()
    sys.exit()

def callback(event):
    global e,root,win_img, previous_command, listNodes
    if(e.get() != ''):
        if any(wrd in (e.get().lower().strip()).split(' ') for wrd in ['exit', 'quit', 'close']):
            exit_game()
        try:
            if("repeat" in (e.get()).lower()):
                messagebox.showinfo("Repeat", "Your command history will pop-up, please select the command that you want to repeat.")
                toggle_visibility()
            else:
                operate_game_by_command(e.get())
            if(e.get() in previous_commands):
                previous_commands.remove(e.get())
            previous_commands.append(e.get())
            listNodes.delete(0, tk.END)
            listNodes.insert(tk.END, *previous_commands)
        except Exception as msg:
            print("err ", e.get(), msg)

        # Check Win
        x = set()
        for ele in line_lst:
            x = x.union(ele)
        if(len(x) == 4):
            print("Won")
            c.delete("all")
            c.create_image(round(root.winfo_screenwidth()/2.3), round(root.winfo_screenheight()/2.5), anchor = tk.NW, image = win_img)
    e.delete(0, 'end')
    
c.bind_all('<Return>', callback)
c.bind_all('<FocusIn>', lambda temp : e.focus())

win2.protocol("WM_DELETE_WINDOW", exit_game)

c.bind('<Configure>', create_grid_and_control_lines)

log = tk.Toplevel(win2)
log.geometry(str(round(root.winfo_screenwidth() * 0.25)) + "x" + str(round(root.winfo_screenheight()*(1/3))) + "+" + str(root.winfo_screenwidth() - round(root.winfo_screenwidth() * 0.25)) + "+" + str(round(root.winfo_screenheight()*0.938) - round(root.winfo_screenheight()*(1/3))))
log.overrideredirect(1)
hidden = True

def toggle_visibility():
    global hidden, log, btn_text
    if hidden:
        log.deiconify()
        btn_text.set('Hide Command History')
        log.attributes("-topmost", True)
    else:
        log.withdraw()
        btn_text.set('Show Command History')
        log.attributes("-topmost", False)
    hidden = not hidden


btn_text = tk.StringVar()
btn_text.set('Show Command History')
tk.Button(win2, textvariable = btn_text, command = toggle_visibility).place(relx=0.9, relheight = 1, relwidth = 0.1)

def onselect(evt):
    global e
    w = evt.widget
    tup = w.curselection()
    if(len(tup) > 0):
        cmd = w.get(tup[0])
    e.delete(0, "end")
    e.insert(0, cmd)

listNodes = tk.Listbox(log, font=("Helvetica", 12))
listNodes.bind('<<ListboxSelect>>', onselect)
listNodes.insert(tk.END, "test")
listNodes.place(relheight = 0.95, relwidth = 0.96)

scrollbary = tk.Scrollbar(log, orient="vertical")
scrollbary.config(command=listNodes.yview)
scrollbary.place(relx = 0.96, relheight = 1)

scrollbarx = tk.Scrollbar(log, orient="horizontal")
scrollbarx.config(command=listNodes.xview)
scrollbarx.place(rely = 0.95, relwidth = 1)

listNodes.config(yscrollcommand=scrollbary.set)
listNodes.config(xscrollcommand=scrollbarx.set)


'''c.bind('<Button-1>', lambda event, ele = "red_line":
       rotate(ele))
c.bind_all('<w>', lambda event, ele = "red_line", direction = "up", val = 1:
       translate(ele, direction, val))
c.bind_all('<a>', lambda event, ele = "red_line", direction = "left", val = 1:
       translate(ele, direction, val))
c.bind_all('<s>', lambda event, ele = "red_line", direction = "down", val = 1:
       translate(ele, direction, val))
c.bind_all('<d>', lambda event, ele = "red_line", direction = "right", val = 1:
       translate(ele, direction, val))'''
e.focus_set()

def voice_command_thread():
    global win2, c
    Speech_to_Text.run()
    
    while(Speech_to_Text.record_mic_voice.flag != 'stop'):
        if(Speech_to_Text.record_mic_voice.flag):
            win2.title('Speak Now')
            c.configure(bg="grey")
        else:
            win2.title('Game Controller')
            c.configure(bg="white")
        with open('command.txt', 'r') as f:
            data = f.readlines()
            f.close()

        while(True):
            try:
                with open('command.txt', 'w') as f:
                    f.writelines(data[1:])
                    f.close()
                    break
            except:
                print("cant open command.txt")
        
        if(data != []):
            print(data[0])
            e.delete(0, "end")
            e.insert(0, str(data[0]))
            e.event_generate('<Return>')
            
            

thread = threading.Thread(target = voice_command_thread)
thread.start()

root.mainloop()
