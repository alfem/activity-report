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

def seconds2hms(s):
  return str(datetime.timedelta(seconds=int(s)))


try:
  logfile = open(LOGFILE, "r")
except IOError:
  print "No es posible leer el registro de actividad "+LOGFILE

session_seconds=0
worked_seconds=0
last_date=""
last_time=0

days=[]


#Recorriendo el fichero de log
for line in logfile:
  (e_date,e_time,e_type,e_status,e_text)=line.split(",",4)
  struct_time=time.strptime(e_date+","+e_time,"%Y-%m-%d,%H:%M:%S")
  e_time=time.mktime(struct_time)
#  print line

  if (e_date != last_date):
    if worked_seconds > 0:
#      print "TOTAL:",last_date,worked_seconds
      days.append( [ last_date,seconds2hms(worked_seconds),seconds2hms(session_seconds) ] )
    session_start_time=0
    session_seconds=0
    worked_seconds=0
    last_date=e_date
    last_time=0

  if e_type == "START":
    last_time=e_time
    if session_start_time == 0:
      session_start_time=e_time
        
  if e_type == "IDLE" or e_type == "SCREENSAVER":
    if e_status == "1":
      if last_time > 0:
        worked_seconds=worked_seconds+e_time-last_time
#        print worked_seconds
        last_time=0
    if e_status == "0":
      last_time=e_time

  if e_type == "PRESENCE":
    if e_status == "0":
      last_time=e_time
    else:
      if last_time > 0:
        worked_seconds=worked_seconds+e_time-last_time
#        print worked_seconds
        last_time=0
    
  if e_type == "LOGOUT" and e_status == "1":
      if last_time > 0:
        worked_seconds=worked_seconds+e_time-last_time
#        print worked_seconds
      if session_start_time > 0:
        session_seconds=e_time - session_start_time

#Fin del log
if (last_time > 0 and last_date == str(datetime.date.today())):
  worked_seconds=worked_seconds+time.time()-last_time
  session_seconds=e_time - session_start_time
  
#  print worked_seconds
 

#print "TOTAL:",last_date,str(datetime.timedelta(seconds=int(worked_seconds)))
days.append( [ last_date,seconds2hms(worked_seconds),seconds2hms(session_seconds) ] )

logfile.close()

cmd='zenity --title "Activity" --text "Acumulado diario" --width 400 --height 200 --list --column "Fecha" --column "Tiempo activo" --column "Duración Sesión" '

days.reverse()
for d in days:
  cmd=cmd+d[0]+" "+d[1]+" "+d[2]+" " 

p = subprocess.Popen(cmd, shell=True)
