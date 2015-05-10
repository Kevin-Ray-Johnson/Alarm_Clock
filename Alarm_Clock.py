#!/usr/bin/env python

# Description:
# An alarm clock application to help my sleeping problem and to learn the 
# Tkiner/Python interface.  The keybinding m changes the clock display 
# type and a right-click will show the date.
#
# Author:
# Kevin Johnson
#
# Date:
# 03/10/06 
#
# Version: 1.0
#
# To-Do:
# > Safety check the input
# > Think of more To-Do's
# > Find some bugs
# > Kill those darn bugs

from Tkinter import *
from mx.DateTime import now, TimeDelta, DateTime
import os, sys
import clock

##################################################################################

class Alarm_Control(Frame):
   def __init__(self, parent, bd=4, relief=RAISED):
      Frame.__init__(self, parent)      
      ##################################################################################
      # Some variables for our use in the program
      snooze_min = 15
      armed = False
      go_time = now() + TimeDelta(8,0,0)
      dt = TimeDelta(8,0,0)
      Update_per_sec = 2
      
      ##################################################################################
      # Define some functions that may be handy to make the functions of an alarm clock

      def run_alarm():
         update_fields()
         if self.armed:
            if self.go_time < now():
               sound_alarm()
            self.after(1000 / Update_per_sec, run_alarm)   # run N times per second  
   
      # Runs the command in the "Halt Command" field when we snooze or halt the alarm
      def halt_alarm():
         self.armed = False 
         dt = TimeDelta(0,0,0)
         update_fields()
         os.system(halt_field.get() + '&')
   
      def snooze_alarm():
         self.go_time = now() + TimeDelta(0,snooze_min,1)
         self.dt = TimeDelta(0,snooze_min)
         halt_alarm()
         self.armed = True
         run_alarm()
   
      # Runs the command in the "Alarm Command" field when the alarm is to go off
      def sound_alarm():
         self.armed = False
         dt = TimeDelta(0,0,0)
         update_fields()
         os.system(run_field.get() + '&')
   
      # Refreshes the display fields to we can see the time count down
      def update_fields():
         # find the new dt
         self.dt = self.go_time - now()
         # Clear the fields and then...
         time_field_hour.delete(0,END)
         time_field_min.delete(0,END)
         time_field_sec.delete(0,END)
         dt_field_hour.delete(0,END)
         dt_field_min.delete(0,END)
         dt_field_sec.delete(0,END)
         # fill them in again
         time_field_hour.insert(0,self.go_time.hour)
         time_field_min.insert(0,self.go_time.minute)
         time_field_sec.insert(0,int(self.go_time.second))
         dt_field_hour.insert(0,self.dt.hour)
         dt_field_min.insert(0,self.dt.minute)
         dt_field_sec.insert(0,int(self.dt.second))

      # Sets the time the alarm will go off   
      def set_time():
         h = int(time_field_hour.get())
         m = int(time_field_min.get())
         s = int(time_field_sec.get())
         self.go_time = DateTime(now().year,now().month,now().day,h,m,s)
         if self.go_time < now():
            self.go_time = DateTime(now().year, now().month, now().day + 1, h, m, s)
         self.dt = self.go_time - now()
         self.armed = True
         run_alarm()

      # Sets the alarm to go off after so long
      def set_dt():
         self.dt = TimeDelta(int(dt_field_hour.get()),int(dt_field_min.get()),int(dt_field_sec.get()))
         self.go_time = now() + self.dt
         self.armed = True
         run_alarm()

      ##################################################################################
      # Here we build the GUI and make the button point to functions that do stuff for us.

      # This field takes the time we want the alarm to go off
      tmp_time = now() + TimeDelta(8,0,0)        #Find sugested 8 hours from now
      time_field_hour = Entry(self, width=2)    #Make the entry field
      time_field_hour.insert(0, tmp_time.hour)  #Put the reccomended hour in
      time_field_min = Entry(self, width=2)
      time_field_min.insert(0, tmp_time.minute)
      time_field_sec = Entry(self, width=2)
      time_field_sec.insert(0, tmp_time.minute)
      time_field_label = Label(self, text="Alarm Time:")
      set_time_button = Button(self, text="Set Time", command=set_time)
     
      # This takes the amount of time we want to elapse before the alarm goes off
      dt_field_hour = Entry(self, width=2)
      dt_field_hour.insert(0, 8)
      dt_field_min = Entry(self, width=2)
      dt_field_min.insert(0, 0)
      dt_field_sec = Entry(self, width=2)
      dt_field_sec.insert(0, 0)
      dt_field_label = Label(self, text="Countdown:")
      set_dt_button = Button(self, text="Set Countdown", command=set_dt)
     
      # This field runs a command inserted into this field
      run_field = Entry(self)
      run_field.insert(0,'totem --play')
      run_field_label = Label(self, text="Alarm Command:")
   
      halt_field = Entry(self)
      halt_field.insert(0,'totem --pause')
      halt_field_label = Label(self, text="Stop Command:")
            
      # The quit button.  Closes the window and exits the program
      quit_button = Button(self, text="Quit", command=root.quit)
      
      # The stop alarm button.  Stops the alarm clock
      stop_button = Button(self, text="Stop Alarm", fg="red", command=halt_alarm)
      
      # This button starts the snooze sequence
      snooze_button = Button(self, text="Snooze " + str(snooze_min) + " min.", fg="red", command=snooze_alarm)
          
      #Set everything's location
      time_field_label.grid(row=0, column=0, sticky=W)
      time_field_hour.grid(row=0, column=1, sticky=W)
      Label(self, text=":").grid(row=0, column=2, sticky=W)
      time_field_min.grid(row=0, column=3, sticky=W)
      Label(self, text=":").grid(row=0, column=4, sticky=W)
      time_field_sec.grid(row=0, column=5, sticky=W)
      set_time_button.grid(row=0, column=6, sticky=EW)

      dt_field_label.grid(row=1, column=0, sticky=W)
      dt_field_hour.grid(row=1, column=1, sticky=W)
      Label(self, text=":").grid(row=1, column=2, sticky=W)
      dt_field_min.grid(row=1, column=3, sticky=W)
      Label(self, text=":").grid(row=1, column=4, sticky=W)
      dt_field_sec.grid(row=1, column=5, sticky=W)
      set_dt_button.grid(row=1, column=6, sticky=EW)

      rows = 7
      columns = 7

      run_field_label.grid(row=2, column=0, sticky=W)
      run_field.grid(row=2, column=1, columnspan=columns-1, sticky=EW)
      halt_field_label.grid(row=3, column=0, sticky=W)
      halt_field.grid(row=3, column=1, columnspan=columns-1, sticky=EW)
      snooze_button.grid(row=4, columnspan=columns, sticky=NSEW)
      stop_button.grid(row=5, columnspan=columns, sticky=NSEW)
      quit_button.grid(row=6, columnspan=columns, sticky=NSEW)
      
#################################################################################

###################
# Run the program #
###################

# Start up our GUI
if __name__ == '__main__':

   # set the command line arguments to the clock's look
   def getOptions(config, argv):
        for attr in dir(clock.ClockConfig):              # fill default config obj,
            try:                                   # from "-attr val" cmd args
                ix = argv.index('-' + attr)
            except:
                continue
            else:
                if ix in range(1, len(argv)-1):
                    if type(getattr(clock.ClockConfig, attr)) == type(0):
                        setattr(config, attr, int(argv[ix+1]))
                    else:
                        setattr(config, attr, argv[ix+1])
                
   # Set up the clock's settings        
   config = clock.ClockConfig() 
   #config = PhotoClockConfig()
   if len(sys.argv) >= 2:
      getOptions(config, sys.argv)         # clock.py -size n -bg 'blue'...

   # Make the window the GUI is in
   root = Tk()
   root.title("Alarm Clock")

   # Make our alarm system in one frame
   alarm_ctrl = Alarm_Control(root)
   
   # Make an analog (or digital!) clock face in the other frame
   clock_face = clock.Clock(config, root)

   # Put all these frames together in the window
   # Side-by-side form
   alarm_ctrl.grid(row=0, column=0, sticky=W, padx=4, pady=4)
   clock_face.grid(row=0, column=1)
#   # Over-under form
#   clock_face.grid(row=0, column=0)
#   alarm_ctrl.grid(row=1, column=0, sticky=N, padx=4, pady=4)   
   
   root.mainloop()

