#!/usr/bin/python

# Needed packages: sudo apt-get install python python-tk python-serial
# This tutorial is a simple program that allows one to adjust the hue, saturation, and value ranges of the ObjectTracker
# module using sliders

serdev = 'COM9' # USB port connected to JeVois

from Tkinter import *
import serial
import time


# default values for Hue, Saturation, and Value ranges:
lowerHue = 0
upperHue = 255
lowerSat = 0
upperSat = 255
lowerVal = 0
upperVal = 255
errode = 0
dilate = 0
approx = 6
area = 500
solidity = 100

####################################################################################################
# Send a command to JeVois and show response
def send_command(cmd):
    print "HOST>> " + cmd
    ser.write(cmd + '\n')
    out = ''
    time.sleep(0.1)
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != '':
        print "JEVOIS>> " + out, # the final comma suppresses extra newline, since JeVois already sends one
        
####################################################################################################
def update_lowerHue(val):
     global lowerHue
     lowerHue = val
     send_command('lowerHue={0}'.format(lowerHue))
     
####################################################################################################
def update_upperHue(val):
    global upperHue
    upperHue = val
    send_command('upperHue={0}'.format(upperHue))
    
####################################################################################################
def update_lowerSat(val):
    global lowerSat
    lowerSat = val
    send_command('lowerSat={0}'.format(lowerSat))
    
####################################################################################################
def update_upperSat(val):
    global upperSat
    upperSat = val
    send_command('upperSat={0}'.format(upperSat))

####################################################################################################
def update_lowerVal(val):
    global lowerVal
    lowerVal = val
    send_command('lowerVal={0}'.format(lowerVal))
    
####################################################################################################
def update_upperVal(val):
    global upperVal
    upperVal = val
    send_command('upperVal={0}'.format(upperVal))
    
####################################################################################################
def update_errode(val):
    global errode
    errode = val
    send_command('errode={0}'.format(errode))
    
####################################################################################################
def update_dilate(val):
    global dilate
    dilate = val
    send_command('dilate={0}'.format(dilate))
    
####################################################################################################
def update_approx(val):
    global approx
    approx = val
    send_command('approx={0}'.format(approx))
    
####################################################################################################
def update_area(val):
    global area
    area = val
    send_command('area={0}'.format(area))
    
####################################################################################################
def update_solidity(val):
    global solidity
    solidity = val
    send_command('solidity={0}'.format(solidity))
    
####################################################################################################
# Main code
ser = serial.Serial(serdev, 115200, timeout=1)
send_command('ping')                   # should return ALIVE

master = Tk()
master.geometry('1220x500')
master.config(bg="navy")
master.title("Eagle Vision JeVois Tuner")

w1 = Label(master, text = "Hue min", fg="white", bg="red3")
w2 = Scale(master, from_=0, to=180, tickinterval=30, length=600, width=16, orient=HORIZONTAL, command=update_lowerHue)
w2.config(fg="black", bg="SlateBlue4", troughcolor="black", activebackground="red3")
w2.set(lowerHue)

w3 = Label(master, text = "Hue max", fg="white", bg="red3")
w4 = Scale(master, from_=0, to=180, tickinterval=30, length=600, width=16, orient=HORIZONTAL, command=update_upperHue)
w4.config(fg="black", bg="SlateBlue4", troughcolor="black", activebackground="red3")
w4.set(upperHue)

w5 = Label(master, text = "Saturation min", fg="white", bg="red3")
w6 = Scale(master, from_=0, to=255, tickinterval=25, length=600, width=16, orient=HORIZONTAL, command=update_lowerSat)
w6.config(fg="black", bg="SlateBlue3", troughcolor="black", activebackground="red3")
w6.set(lowerSat)
 
w7 = Label(master, text = "Saturation max", fg="white", bg="red3")
w8 = Scale(master, from_=0, to=255, tickinterval=25, length=600, width=16, orient=HORIZONTAL, command=update_upperSat)
w8.config(fg="black", bg="SlateBlue3", troughcolor="black", activebackground="red3")
w8.set(upperSat)

w9 = Label(master, text = "Value min", fg="white", bg="red3")
w10 = Scale(master, from_=0, to=255, tickinterval=25, length=600, width=16, orient=HORIZONTAL, command=update_lowerVal)
w10.config(fg="black", bg="SlateBlue2", troughcolor="black", activebackground="red3")
w10.set(lowerVal)

w11 = Label(master, text = "Value max", fg="white", bg="red3")
w12 = Scale(master, from_=0, to=255, tickinterval=25, length=600, width=16, orient=HORIZONTAL, command=update_upperVal)
w12.config(fg="black", bg="SlateBlue2", troughcolor="black", activebackground="red3")
w12.set(upperVal)

w13 = Label(master, text = "Errode", fg="white", bg="red3")
w14 = Scale(master, from_=0, to=20, tickinterval=4, length=600, width=16, orient=HORIZONTAL, command=update_errode)
w14.config(fg="black", bg="SlateBlue1", troughcolor="black", activebackground="red3")
w14.set(errode)

w15 = Label(master, text = "Dilate", fg="white", bg="red3")
w16 = Scale(master, from_=0, to=20, tickinterval=4, length=600, width=16, orient=HORIZONTAL, command=update_dilate)
w16.config(fg="black", bg="SlateBlue1", troughcolor="black", activebackground="red3")
w16.set(dilate)

w17 = Label(master, text = "Approx", fg="white", bg="red3")
w18 = Scale(master, from_=0, to=25, tickinterval=5, length=600, width=16, orient=HORIZONTAL, command=update_approx)
w18.config(fg="black", bg="SlateBlue1", troughcolor="black", activebackground="red3")
w18.set(approx)

w19 = Label(master, text = "Area", fg="white", bg="red3")
w20 = Scale(master, from_=0, to=10000, tickinterval=1000, length=600, width=16, orient=HORIZONTAL, command=update_area)
w20.config(fg="black", bg="SlateBlue1", troughcolor="black", activebackground="red3")
w20.set(area)

w21 = Label(master, text = "Solidity", fg="white", bg="red3")
w22 = Scale(master, from_=0, to=100, tickinterval=20, length=600, width=16, orient=HORIZONTAL, command=update_solidity)
w22.config(fg="black", bg="grey", troughcolor="black", activebackground="red3")
w22.set(solidity)

w1.grid(row=0, column=0) #Hue Min
w2.grid(row=1, column=0)
w3.grid(row=0, column=1) #Hue Max
w4.grid(row=1, column=1)

w5.grid(row=2, column=0) #Sat Max
w6.grid(row=3, column=0)
w7.grid(row=2, column=1) #Sat Max
w8.grid(row=3, column=1)

w9.grid(row=4, column=0)  #Val Max
w10.grid(row=5, column=0)
w11.grid(row=4, column=1) #Val Max
w12.grid(row=5, column=1)

w13.grid(row=6, column=0) #Errode
w14.grid(row=7, column=0)
w15.grid(row=6, column=1) #Dilate
w16.grid(row=7, column=1)

w17.grid(row=8, column=0) #Approx
w18.grid(row=9, column=0)
w19.grid(row=8, column=1) #Area
w20.grid(row=9, column=1)

w21.grid(row=10, columnspan=2) #Solidity
w22.grid(row=11, columnspan=2)

mainloop()
