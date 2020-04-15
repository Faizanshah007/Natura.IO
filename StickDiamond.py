import tkinter as tk
from tkinter import messagebox
import random
import itertools
import requests
import sys

def get_rand_offset():
    offset = [100,-100]
    random.shuffle(offset)
    return offset[0]

control_lines = dict()
w = None
h = None
line_lst = list()

def create_grid_and_control_lines(event=None):
    global control_lines, w, h, line_lst
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    #c.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, 100):
        c.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, 100):
        c.create_line([(0, i), (w, i)], tag='grid_line')

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
    print("hi")
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
    try:
        command = x
        r = requests.get(f'https://centralindia.api.cognitive.microsoft.com/luis/v2.0/apps/67ec9d8b-fed1-4ded-a47d-c76f07d5ef93?staging=true&verbose=true&timezoneOffset=330&subscription-key=b95bd42248b548f5b94f34dad2bde47a&q=' + command)
        result = r.json()
        print(result)
    except Exception as e:
        print(f'{e}')
    #result = {'query': 'move red line rightwards by 1 block and then rotate the blue line.', 'topScoringIntent': {'intent': 'move', 'score': 0.982636154}, 'intents': [{'intent': 'move', 'score': 0.982636154}, {'intent': 'rotate', 'score': 0.151299834}, {'intent': 'None', 'score': 0.00239448785}], 'entities': [{'entity': 'red', 'type': 'colour', 'startIndex': 5, 'endIndex': 7, 'score': 0.9873937}, {'entity': 'blue', 'type': 'colour', 'startIndex': 56, 'endIndex': 59, 'score': 0.998382449}, {'entity': 'rightwards', 'type': 'direction', 'startIndex': 14, 'endIndex': 23, 'score': 0.9956634, 'role': 'right'}, {'entity': '1', 'type': 'builtin.number', 'startIndex': 28, 'endIndex': 28, 'resolution': {'subtype': 'integer', 'value': '1'}}]}

    intent = list()

    temp = (requests.get(f'https://centralindia.api.cognitive.microsoft.com/luis/v2.0/apps/9add54d5-3a9a-4315-b153-daa4c53395ad?staging=true&verbose=true&timezoneOffset=330&subscription-key=b95bd42248b548f5b94f34dad2bde47a&q=' + command)).json()
    flag = None
    
    if(temp['topScoringIntent']['intent'] == 'MoveAndRotate'):
        flag = True
    
    for ele in result['intents']:
        if(flag and (ele['intent'] == "move" or ele['intent'] == "rotate")):
            intent.append(ele['intent'])
        elif(ele['intent'] == "move" or ele['intent'] == "rotate"):
            intent.append(ele['intent'])
            break
        else:
            break

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

    print(intent,colour,direction,magnitude)

    if(magnitude == []):
        magnitude = [1]

    if(len(intent) == 0 or len(colour) == 0 or ('translate' in intent and (len(direction)== 0 or len(magnitude) == 0))):
        num_of_ops = 0
    else:
        num_of_ops = max(len(intent), len(colour), len(direction), len(magnitude))

    data = [intent, colour, direction, magnitude]

    for i in range(num_of_ops):

        if(data[0][0] == 'move'):
            translate(data[1][0] + '_line', data[2][0], data[3][0])
            for spec in data:
                if(len(spec) > 1):
                    del spec[0]

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
win2.attributes("-topmost",True)

win2.geometry(str(root.winfo_screenwidth()) + "x" + str(round(root.winfo_screenheight()*0.028)) + "+" + str(0) + "+" + str(round(root.winfo_screenheight()*0.938)))
e = tk.Entry(win2)
e.pack(fill=tk.BOTH, expand=True)

win_img = tk.PhotoImage(file = 'win.ppm')

previous_command = ''

def callback(event):
    global root,win_img, previous_command
    if(e.get() != ''):
        if any(wrd in (e.get().lower()).split(' ') for wrd in ['exit', 'quit', 'close']):
            root.destroy()
            sys.exit()
        if("repeat" in e.get()):
            if(messagebox.askyesno("Repeat", "Do you want to repeat the current instruction?")):
                operate_game_by_command(e.get())
                operate_game_by_command(e.get())
            elif(messagebox.askyesno("Repeat", "Do you want to repeat the previous instruction?")):
                operate_game_by_command(previous_command)
        else:
            operate_game_by_command(e.get())
        previous_command = e.get()

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



c.bind('<Configure>', create_grid_and_control_lines)

##root.after(100,thread_loop)

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
root.mainloop()
