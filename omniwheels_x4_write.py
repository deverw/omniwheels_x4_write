# omniwheels_x4_write
# writes single letters selected on the touchscreen
# or text from voice control.
# Mechatronics: omniwheels_x4_paint / Malroboter as described in manual

# Author: Stefan Abendroth, 12/2025

import time
from fischertechnik.control.VoiceControl import VoiceControl
from fischertechnik.controller.Motor import Motor
from lib.controller import *
from lib.display import *

speed = 250		# default speed of motors
size = 2		# horizontal step size in mm (vertical step size is factor 1.5 longer)

# Characters start at lower left corner and finish at start of next character.
# Characters are maximum 6 steps wide (6mm * size) and 6 steps high (9mm * size).
# Each command has one unsigned integer parameter, separated by whitespace.
# Commands in character sequence are semicolon separated.
# pen up: P 0; pen down P 1
# move left (x steps): L x; right R x
# move upwards (y steps): U y; downwards D y
# move diagonal (z steps up/down and left/right combined): UL z; DL z; UR z; DR z
simplex = {
    'a_upper': 'P 1;U 3;UR 3;DR 3;D 3;P 0;UL 3;L 3;P 1;R 6;P 0;DR 2;D 1',
    'b_upper': 'P 1;R 5;UR 1;U 1;UL 1;L 3;P 0;R 3;P 1;UR 1;U 1;UL 1;L 5;D 6;P 0;R 8',
    'c_upper': 'UR 6;P 1;L 4;DL 2;D 2;DR 2;R 4;P 0;R 2',
    'd_upper': 'P 1;R 4;UR 2;U 2;UL 2;L 4;D 6;P 0;R 8',
    'e_upper': 'U 3;P 1;R 3;P 0;UR 3;P 1;L 6;D 6;R 6;P 0;R 2',
    'f_upper': 'U 3;P 1;R 3;P 0;UR 3;P 1;L 6;D 6;P 0;R 8',
    'g_upper': 'UR 3;P 1;R 3;D 3;L 4;UL 2;U 2;UR 2;R 4;P 0;DR 2;D 4',
    'h_upper': 'P 1;U 6;P 0;D 3;P 1;R 6;P 0;U 3;P 1;D 6;P 0;R 2',
    'i_upper': 'P 1;U 6;P 0;DR 2;D 4',
    'j_upper': 'U 6;P 1;R 6;D 4;DL 2;L 2;UL 2;P 0;DR 2;R 6',
    'k_upper': 'P 1;U 6;P 0;R 6;P 1;DL 3;L 3;P 0;R 3;P 1;DR 3;P 0;R 2',
    'l_upper': 'U 6;P 1;D 6;R 6;P 0;R 2',
    'm_upper': 'P 1;U 6;DR 3;UR 3;D 6;P 0;R 2',
    'n_upper': 'P 1;U 6;DR 6;U 6;P 0;DR 2;D 4',
    'o_upper': 'R 2;P 1;R 2;UR 2;U 2;UL 2;L 2;DL 2;D 2;DR 2;P 0;R 6',
    'p_upper': 'P 1;U 6;R 5;DR 1;D 1;DL 1;L 5;P 0;DR 3;R 5',
    'q_upper': 'R 2;P 1;R 2;UR 2;P 0;L 2;P 1;DR 2;P 0;U 2;P 1;U 2;UL 2;L 2;DL 2;D 2;DR 2;P 0;R 6',
    'r_upper': 'P 1;U 6;R 5;DR 1;D 1;DL 1;L 5;P 0;R 3;P 1;DR 3;P 0;R 2',
    's_upper': 'P 1;R 5;UR 1;U 1;UL 1;L 4;UL 1;U 1;UR 1;R 5;P 0;DR 2;D 4',
    't_upper': 'U 6;P 1;R 6;P 0;L 3;P 1;D 6;P 0;R 5',
    'u_upper': 'U 6;P 1;D 4;DR 2;R 2;UR 2;U 4;P 0;DR 2;D 4',
    'v_upper': 'U 6;P 1;D 3;DR 3;UR 3;U 3;P 0;DR 2;D 4',
    'w_upper': 'U 6;P 1;D 6;UR 3;DR 3;U 6;P 0;DR 2;D 4',
    'x_upper': 'P 1;UR 6;P 0;L 6;P 1;DR 6;P 0;R 2',
    'y_upper': 'U 6;P 1;DR 3;D 3;P 0;U 3;P 1;UR 3;P 0;DR 2;D 4',
    'z_upper': 'U 6;P 1;R 6;DL 6;R 6;P 0;R 2',
    'ä_upper': 'P 1;U 3;UR 3;P 0;L 1;P 1;U 1;P 0;R 2;P 1;D 1;P 0;L 1;P 1;DR 3;D 3;P 0;UL 3;L 3;P 1;R 6;P 0;DR 2;D 1',
    'ö_upper': 'R 2;P 1;R 2;UR 2;U 2;UL 2;P 0;R 1;P 1;U 1;P 0;L 4;P 1;D 1;P 0;R 3;P 1;L 2;DL 2;D 2;DR 2;P 0;R 6',
    'ü_upper': 'UR 4;U 2;P 1;U 1;P 0;L 2;P 1;D 1;P 0;L 2;P 1;D 4;DR 2;R 2;UR 2;U 4;P 0;DR 2;D 4',
    'a_lower': 'R 4;P 1;U 3;UL 1;L 2;DL 1;D 2;DR 1;R 2;UR 1;P 0;DR 1;R 1',
    'b_lower': 'U 6;P 1;D 6;R 3;UR 1;U 2;UL 1;L 3;P 0;DR 4;R 2',
    'c_lower': 'UR 3;R 1;P 1;UL 1;L 2;DL 1;D 2;DR 1;R 2;UR 1;P 0;DR 1;R 1',
    'd_lower': 'UR 4;U 2;P 1;D 6;L 3;UL 1;U 2;UR 1;R 3;P 0;DR 2;D 2',
    'e_lower': 'U 2;P 1;R 4;U 1;UL 1;L 2;DL 1;D 2;DR 1;R 2;UR 1;P 0;DR 1;R 1',
    'f_lower': 'P 1;U 5;UR 1;R 2;DR 1;P 0;D 3;P 1;L 4;P 0;DR 2;R 4',
    'g_lower': 'D 1;P 1;DR 1;R 2;UR 1;U 4;UL 1;L 2;DL 1;D 2;DR 1;R 3;P 0;R 2',
    'h_lower': 'P 1;U 6;P 0;D 3;P 1;UR 1;R 2;DR 1;D 3;P 0;R 2',
    'i_lower': 'P 1;U 4;P 0;U 1;P 1;U 1;P 0;DR 2;D 4',
    'j_lower': 'D 1;P 1;DR 1;R 2;UR 1;U 5;P 0;U 1;P 1;U 1;P 0;DR 2;D 4',
    'k_lower': 'P 1;U 6;P 0;DR 1;R 2;P 1;DL 2;L 2;P 0;R 1;P 1;DR 3;P 0;R 2',
    'l_lower': 'U 6;P 1;D 5;DR 1;R 2;UR 1;P 0;DR 1;R 1',
    'm_lower': 'U 4;P 1;D 4;P 0;U 3;P 1;UR 1;R 1;DR 1;D 3;P 0;U 3;P 1;UR 1;R 1;DR 1;D 3;P 0;R 2',
    'n_lower': 'U 4;P 1;D 4;P 0;U 3;P 1;UR 1;R 2;DR 1;D 3;P 0;R 2',
    'o_lower': 'R 1;P 1;R 2;UR 1;U 2;UL 1;L 2;DL 1;D 2;DR 1;P 0;R 5',
    'p_lower': 'D 2;P 1;U 6;R 3;DR 1;D 2;DL 1;L 3;P 0;R 6',
    'q_lower': 'DR 2;R 2;P 1;U 6;L 3;DL 1;D 2;DR 1;R 3;P 0;R 2',
    'r_lower': 'P 1;U 4;P 0;D 1;P 1;UR 1;R 2;DR 1;P 0;DR 2;D 1',
    's_lower': 'U 1;P 1;DR 1;R 2;UR 1;UL 1;L 2;UL 1;UR 1;R 2;DR 1;P 0;DR 2;D 1',
    't_lower': 'U 4;P 1;R 2;P 0;UL 1;U 1;P 1;D 5;DR 1;R 1;UR 1;P 0;R 2',
    'u_lower': 'U 4;P 1;D 3;DR 1;R 2;UR 1;P 0;D 1;P 1;U 4;P 0;DR 2;D 2',
    'v_lower': 'U 4;P 1;D 2;DR 2;UR 2;U 2;P 0;DR 2;D 2',
    'w_lower': 'U 4;P 1;D 3;DR 1;R 1;UR 1;U 2;P 0;D 2;P 1;DR 1;R 1;UR 1;U 3;P 0;DR 2;D 2',
    'x_lower': 'P 1;UR 4;P 0;L 4;P 1;DR 4;P 0;R 2',
    'y_lower': 'U 4;P 1;D 3;DR 1;R 3;P 0;DL 1;L 3;P 1;DR 1;R 2;UR 1;U 5;P 0;DR 2;D 2',
    'z_lower': 'U 4;P 1;R 4;DL 4;R 4;P 0;R 2',
    'ä_lower': 'R 4;P 1;U 3;UL 1;P 0;U 2;P 1;D 1;P 0;D 1;P 1;L 2;P 0;U 2;P 1;D 1;P 0;D 1;P 1;DL 1;D 2;DR 1;R 2;UR 1;P 0;DR 1;R 1',
    'ö_lower': 'R 1;P 1;R 2;UR 1;U 2;UL 1;P 0;U 2;P 1;D 1;P 0;D 1;P 1;L 2;P 0;U 2;P 1;D 1;P 0;D 1;P 1;DL 1;D 2;DR 1;P 0;R 5',
    'ü_lower': 'U 3;UR 3;P 1;D 1;P 0;L 2;P 1;U 1;P 0;DL 1;D 1;P 1;D 3;DR 1;R 2;UR 1;P 0;D 1;P 1;U 4;P 0;DR 2;D 2',
    'ß_lower': 'D 2;P 1;U 8;R 1;DR 1;D 1;DL 1;DR 1;D 2;L 1;P 0;R 3',
    'space': 'R 6'
}

def penUp():
    TXT_M_S1_servomotor.set_position(int(300))
    time.sleep(0.1)

def penDown():
    TXT_M_S1_servomotor.set_position(int(256))
    time.sleep(0.1)

def moveD(units):
    TXT_M_M1_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M2_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M3_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M4_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M1_encodermotor.set_distance(units*size, TXT_M_M2_encodermotor, TXT_M_M3_encodermotor, TXT_M_M4_encodermotor)
    while True:
        if (not TXT_M_M1_encodermotor.is_running()):
            break
        time.sleep(0.010)

def moveU(units):
    TXT_M_M1_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M2_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M3_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M4_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M1_encodermotor.set_distance(units*size, TXT_M_M2_encodermotor, TXT_M_M3_encodermotor, TXT_M_M4_encodermotor)
    while True:
        if (not TXT_M_M1_encodermotor.is_running()):
            break
        time.sleep(0.010)

def moveR(units):
    TXT_M_M1_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M2_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M3_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M4_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M1_encodermotor.set_distance(units*size, TXT_M_M2_encodermotor, TXT_M_M3_encodermotor, TXT_M_M4_encodermotor)
    while True:
        if (not TXT_M_M1_encodermotor.is_running()):
            break
        time.sleep(0.010)

def moveL(units):
    TXT_M_M1_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M2_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M3_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M4_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M1_encodermotor.set_distance(units*size, TXT_M_M2_encodermotor, TXT_M_M3_encodermotor, TXT_M_M4_encodermotor)
    while True:
        if (not TXT_M_M1_encodermotor.is_running()):
            break
        time.sleep(0.010)

def moveDR(units):
    TXT_M_M2_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M3_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M2_encodermotor.set_distance(2 * units * size, TXT_M_M3_encodermotor)
    while True:
        if (not TXT_M_M2_encodermotor.is_running()):
            break
        time.sleep(0.010)

def moveDL(units):
    TXT_M_M1_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M4_encodermotor.set_speed(speed, Motor.CCW)
    TXT_M_M1_encodermotor.set_distance(2 * units * size, TXT_M_M4_encodermotor)
    while True:
        if (not TXT_M_M1_encodermotor.is_running()):
            break
        time.sleep(0.010)

def moveUR(units):
    TXT_M_M1_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M4_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M1_encodermotor.set_distance(2 * units * size, TXT_M_M4_encodermotor)
    while True:
        if (not TXT_M_M1_encodermotor.is_running()):
            break
        time.sleep(0.010)

def moveUL(units):
    TXT_M_M2_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M3_encodermotor.set_speed(speed, Motor.CW)
    TXT_M_M2_encodermotor.set_distance(2 * units * size, TXT_M_M3_encodermotor)
    while True:
        if (not TXT_M_M2_encodermotor.is_running()):
            break
        time.sleep(0.010)

def write(event):
    # write single character
    letter = event['id']
    sequence = simplex[letter].split(';')
    for step in sequence:
        step = step.split()
        op = step[0]
        param = int(step[1])
        if op=='P':
            if param<1:
                penUp()
            else:
                penDown()
        elif op=='D':
            moveD(param)
        elif op=='U':
            moveU(param)
        elif op=='L':
            moveL(param)
        elif op=='R':
            moveR(param)
        elif op=='DR':
            moveDR(param)
        elif op=='DL':
            moveDL(param)
        elif op=='UR':
            moveUR(param)
        elif op=='UL':
            moveUL(param)

def shift(event):
    # swap display buttons between lower and upper characters
    upper = event['id']=='shift_upper'
    for c in range(97,123):
        display.set_attr(chr(c)+"_upper.enabled",upper)
        display.set_attr(chr(c)+"_lower.enabled",not upper)
    display.set_attr("shift_upper.enabled",not upper)
    display.set_attr("shift_lower.enabled",upper)
        
def command_callback(event):
    # write entire string received from voice control
    for letter in event:
        if letter.isalpha():
            if letter.isupper():
                write({'id' : letter.lower()+'_upper'})
            else:
                write({'id' : letter+'_lower'})
        elif letter==' ':
            write({'id' : 'space'})

def init():
    for c in range(97,123):
        display.button_clicked(chr(c)+"_upper",write)
        display.button_clicked(chr(c)+"_lower",write)
    display.button_clicked("space", write)
    display.button_clicked("shift_lower", shift)
    display.button_clicked("shift_upper", shift)
    voice_control = VoiceControl()
    voice_control.add_command_listener(command_callback)
    penUp()

init()
while True:
    pass