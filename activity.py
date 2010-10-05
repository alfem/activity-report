#!/usr/bin/python
# -*- coding: utf8 -*-

# Logger for GNOME sesion activity
# Author: Alfonso E.M.
# 1 October 2010


import dbus
import dbus.glib 
import gobject
import datetime, time
import signal
import os
import gnome.ui


def on_signal(signum, frame):
  log_event("SIGNAL",signum,"Señal detectada")

def on_screensaver_changed(state):
  """Metodo llamado automaticamente cuando el salvapantallas se activa/desactiva """
  if state == 1:
    log_event("SCREENSAVER",state,"Comienza periodo de inactividad") 
  else:
    log_event("SCREENSAVER",state,"Fin del periodo de inactividad")      

def on_session_changed(state):
  """Metodo llamado automaticamente cuando el salvapantallas se activa/desactiva """
  if state == 3:
    log_event("PRESENCE",state,"Comienza periodo de inactividad") 
  else:
    log_event("PRESENCE",state,"Fin del periodo de inactividad") 
  
def on_logout(*args):
  log_event("LOGOUT",1,"Fin de la sesion")      

def on_logout_cancel(*args):
  log_event("LOGOUT",0,"Cancelando fin de la sesion")      



def log_event(type,state,message):
  """Guarda la fecha, hora y estado del evento"""
  try:
    logfile = open(LOGFILE, "a")
    try:
      human_datetime=time.strftime("%Y-%m-%d,%H:%M:%S",time.localtime())
      logfile.write("%s,%s,%i,%s\n" % (human_datetime,type,state,message))
    finally:
      logfile.close()
  except IOError:
    print "No es posible grabar el registro de actividad "+LOGFILE



#Configuración

#Archivo de log en el home del usuario
homedir = os.path.expanduser('~')
LOGFILE=homedir+"/activity.log"


#Comienza el programa
log_event("START",1,"Inicio del medidor de actividad")      

#Capturamos señales de terminacion
signal.signal(signal.SIGTERM, on_signal)
      
#Obtenemos el bus de sesión (mediante dbus)
session_bus = dbus.SessionBus()

#Añadimos una llamada a nuestro método cuando dbus avise de un cambio en el salvapantallas o en la presencia
session_bus.add_signal_receiver(on_screensaver_changed,'ActiveChanged','org.gnome.ScreenSaver')
session_bus.add_signal_receiver(on_session_changed,'StatusChanged','org.gnome.SessionManager.Presence')

gnome.program_init('Activity',"1") 
client = gnome.ui.master_client() 
client.connect('save-yourself', on_logout) # Fin de la sesion Gnome, hora de guardar datos
client.connect('shutdown-cancelled', on_logout_cancel) # Fin de sesion cancelado
#client.connect('die', on_logout) # Programa finalizado por fin de sesion


#Esperamos eventos
loop = gobject.MainLoop()
loop.run()

 