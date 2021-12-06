#!/usr/bin/python3

import json
import sys
import getopt
import linecache
import time

from sense_emu import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED

sense = SenseHat()

x = 0
y = 0
z = 0


class EnvData :
       def __init__ (self , roll , pitch, yaw, temp, press, humi, x, y, z):
               self.roll = roll
               self.pitch = pitch
               self.yaw = yaw
               self.x = x
               self.y = y
               self.z = z
               self.temp = temp
               self.press = press
               self.humi = humi
               
               
class EnvData_rpy:
       def __init__ (self , roll , pitch, yaw):
               self.roll = roll
               self.pitch = pitch
               self.yaw = yaw
               
class EnvData_tph:
       def __init__ (self , temp , press, humi):
               self.temp = temp
               self.press = press
               self.humi = humi
               
class EnvData_joy:
       def __init__ (self , x , y, z):
               self.x = x
               self.y = y
               self.z = z

def pushed_up(event):
    global y
    if event.action != ACTION_RELEASED:
        y = y + 1

def pushed_down(event):
    global y
    if event.action != ACTION_RELEASED:
        y = y - 1

def pushed_left(event):
    global x
    if event.action != ACTION_RELEASED:
        x = x - 1

def pushed_right(event):
    global x
    if event.action != ACTION_RELEASED:
        x = x + 1
        
def pushed_middle(event):
    global z
    if event.action != ACTION_RELEASED:
        z = z + 1

def save_joy():

    with open('joy.json', 'w+') as outfile:
        obj_data = EnvData_joy(x, y, z)
        result = json.dumps(obj_data.__dict__)
        outfile.write(result)

def save_tph():

    with open('tph.json', 'w+') as outfile:
        obj_data = EnvData_tph(temp, press, humi)
        result = json.dumps(obj_data.__dict__)
        outfile.write(result)

def save_rpy():

    with open('rpy.json', 'w+') as outfile:
        obj_data = EnvData_rpy(roll, pitch, yaw)
        result = json.dumps(obj_data.__dict__)
        outfile.write(result)
        
def save_arrayCS():

    with open('data_arrayCS.json', 'w+') as outfile:

        result = json.dumps([{"name":'temperature',"value":temp,"unit":'C'},{"name":'pressure',"value":press,"unit":'mbar'},{"name": 'Humidity',"value":humi,"unit": '%'},
        {"name": 'Roll',"value":roll,"unit": 'deg'},{"name": 'Pitch',"value":pitch,"unit": 'deg'},{"name": 'Yaw',"value":yaw,"unit": 'deg'},{"name": 'x',"value":x,"unit": '-'},{"name": 'y',"value":y,"unit": '-'},{"name": 'z',"value":z,"unit": '-'}])
        outfile.write(result)
        
def save_arrayAndroid():

    with open('data_arrayAN.json', 'w+') as outfile:

        result = json.dumps([{"name":'temperature'},{"value":temp},{"unit":'C'},{"name":'pressure'},{"value":press},{"unit":'mbar'},{"name": 'Humidity'},{"value":humi},{"unit": '%'},
        {"name": 'Roll'},{"value":roll},{"unit": 'deg'},{"name": 'Pitch'},{"value":pitch},{"unit": 'deg'},{"name": 'Yaw'},{"value":yaw},{"unit": 'deg'},{"name": 'x'},{"value":x},{"unit": '-'},{"name": 'y'},{"value":y},{"unit": '-'},{"name": 'z'},{"value":z},{"unit": '-'}])
        outfile.write(result)
        

def save_data():

    with open('dataCS.json', 'w+') as outfile:
        obj_data = EnvData(roll , pitch, yaw, temp, press, humi, x, y, z)
        result = json.dumps(obj_data.__dict__)
        outfile.write(result)


while True:

    sense.stick.direction_up = pushed_up
    sense.stick.direction_down = pushed_down
    sense.stick.direction_left = pushed_left
    sense.stick.direction_right = pushed_right
    sense.stick.direction_middle = pushed_middle
    sense.stick.direction_any = save_data

    
    temp = sense.get_temperature()
    press = sense.get_pressure()
    humi = sense.get_humidity()

    
    orientation_degrees = sense.get_orientation_degrees()
    
    roll=orientation_degrees["roll"]
    pitch=orientation_degrees["pitch"]
    yaw=orientation_degrees["yaw"]

    save_arrayCS()
    save_arrayAndroid()
    save_joy()
    save_tph()
    save_rpy()
    save_data()
    
    time.sleep(0.1)
