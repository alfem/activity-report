#!/usr/bin/python
# -*- coding: utf8 -*-

# Reporter for GNOME sesion activity
# Author: Alfonso E.M.
# 1 October 2010

import os
import subprocess
import datetime, time



homedir = os.path.expanduser('~')
LOGFILE=homedir+"/activity.log"


try:
  logfile = open(LOGFILE, "r")
except IOError:
  print "No es posible leer el registro de actividad "+LOGFILE

seconds=0
last_date=""
last_time=0

days=[]


for line in logfile:
#  print line
  (e_date,e_time,e_type,e_status,e_text)=line.split(",",4)
  e_time=float(e_time)
#  print e_date,e_time

  if (e_date != last_date):
    if seconds > 0:
      print "TOTAL:",last_date,seconds
      days.append( [last_date,str(datetime.timedelta(seconds=int(seconds)))] )
    seconds=0
    last_date=e_date
    last_time=0

  if e_type == "START":
    last_time=e_time
    
  if e_type == "IDLE" or e_type == "SCREENSAVER":
    if e_status == "1":
      if last_time > 0:
        seconds=seconds+e_time-last_time
        last_time=0
    if e_status == "0":
      last_time=e_time

  if e_type == "PRESENCE":
    if e_status == "0":
      last_time=e_time
    else:
      if last_time > 0:
        seconds=seconds+e_time-last_time
        last_time=0
    
  if e_type == "LOGOUT" and e_status == "1":
      if last_time > 0:
        seconds=seconds+e_time-last_time


if (last_time > 0 and last_date == str(datetime.date.today())):
  seconds=seconds+time.time()-last_time


print "TOTAL:",last_date,str(datetime.timedelta(seconds=int(seconds)))
days.append( [last_date,str(datetime.timedelta(seconds=int(seconds)))] )

logfile.close()

cmd='zenity --title "Activity" --text "Acumulado diario" --list --column "Fecha" --column "Horas" '

days.reverse()
for d in days:
  cmd=cmd+d[0]+" "+d[1]+" " 

#print cmd
p = subprocess.Popen(cmd, shell=True)
