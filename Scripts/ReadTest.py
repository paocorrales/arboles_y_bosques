#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 18:20:33 2023

@author: jruiz
"""
import SynopDataModule as SDM
import numpy as np
import matplotlib.pyplot as plt


data = SDM.read_raw_data("../Datos/EXP_133453_HORA.txt")

plt.figure()
#Temperatura en centigrados
plt.plot( data['temperature'][data['temperature'] != data['undef'] ] )
plt.figure()
#Punto de rocio en centigrados
plt.plot( data['dewpoint'][data['dewpoint'] != data['undef'] ] )
plt.figure()
#Velocidad del viento en km/h
plt.plot( data['windspeed'][data['windspeed'] != data['undef'] ] )
plt.figure()
#En winddir el valor 99.0 identifica la calma, los demas valores son los grados / 10 (eg 10 son 100 grados y asi).
plt.plot( data['winddir'][data['winddir'] != data['undef'] ] )
plt.figure()
#Humedad relativa (entre 0 y 1)
plt.plot( data['rh'][data['rh'] != data['undef'] ] )
plt.figure()
#Visibilidad en km (ojo que hay datos que llegan hasta 70 km ... yo pondria un limite en 10 km). 
plt.plot( data['vis'][data['vis'] != data['undef'] ] )
plt.figure()
#Presion en hPa
plt.plot( data['pressure'][data['pressure'] != data['undef'] ] )
