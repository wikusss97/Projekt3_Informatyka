# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:02:10 2019

@author: lenovo
"""
from math import atan, sqrt, sin, tan, cos, radians
import gpxpy
import numpy as np

def Wczytaj(file):
    lat = []
    lon = []
    el = []
    dates = []
    with open(file, 'r' ) as gpx_file: # podac sciezke do pliku
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for seg in track.segments:
                for point in seg.points:					
                    lon.append(point.longitude)
                    lat.append(point.latitude)
                    
                    if point.elevation != None:
                        #jesli elewacja jest dostepna
                        el.append(point.elevation)
        			# jesli czas dostepny
        			# usuniecie informacji o strefie czasowej
                    if point.time != None:
                        point.time = point.time.replace(tzinfo=None)
                        dates.append(point.time)
                       
    return (lon, lat, el, dates)

                

def Vincenty(fa,la,fb,lb):
    fa = radians(fa)
    la = radians(la)
    fb = radians(fb)
    lb = radians(lb)
    e2=0.00669438002290
    a=6378137
    b=a*sqrt(1-e2)
    f=1-(b/a)
    Ua=atan((1-f)*tan(fa))
    Ub=atan((1-f)*tan(fb))
    l=lb-la
    L=l
    i=0
    
    while True:
        i = i+1
        sd = sqrt(((cos(Ub)*sin(L))**2)+(cos(Ua)*sin(Ub)-sin(Ua)*cos(Ub)*cos(L))**2)
        cd = sin(Ua)*sin(Ub)+cos(Ua)*cos(Ub)*cos(L)
        d = atan(sd/cd)
        sa = cos(Ua)*cos(Ub)*sin(L)/sd
        c2a = 1-(sa)**2
        c2d = cd-2*sin(Ua)*sin(Ub)/c2a
        C = (f/16)*c2a*(4+f*(4-3*c2a))
        Ls = L
        L = l+(1-C)*f*sa*(d+C*sd*(c2d+C*cd*(-1+2*c2d**2)))
        if abs(L-Ls) < (0.000001/206265):
            break
  
    
    u2 = ((a**2-b**2)/b**2)*c2a
    A = 1+(u2/16384)*(4096+u2*(-768+u2*(320-175*u2)))
    B = (u2/1024)*(256+u2*(-128+u2*(74-47*u2)))
    dd = B*sd*(c2d+(1/4)*B*(cd*(-1+2*(c2d**2))-(1/6)*B*c2d*(-3+4*(sd**2))*(-3+4*(c2d**2))))
    S = b*A*(d-dd)
    return S

def d_m_s(czas): 
    d=int(czas) #godziny
    m=int((czas-d)*60.0) #minuty
    s=int((czas-d-m/60.0)*3600.0) #sekundy
    return (d, m, s) 
    
def zmienne(lon, lat, el, dates):
    alt_dif = [0] 					# przewyższenie na punktach
    time_dif = [0]					# czas pomiędzy punktami
    dist = [0]                      # odległość między punktami
    v = [0]
    for index in range(len(lat)): # index - od zera do końca listy 
        if index == 0:	# pomijamy pierwszy element
            pass
        else:
            start = index-1
            stop = index
		
            dist_part = Vincenty(lat[start],lon[start],lat[stop],lon[stop])		#liczenie odległości funkcją Vincentego
			
            dist.append(dist_part)												#lista z odległościami
		
            if el != []:
                alt_part = el[stop]-el[start]								#przewyższenie z różnicy elewacji
                alt_dif.append(alt_part)
                if dates != []:
                    time_delta = (dates[stop] - dates[start])			#czas między punktami
                    time_dif.append(time_delta.seconds)
                    
                    if time_delta.seconds == 0:
                        v.append(0)
                    else:
                        v.append(dist_part/time_delta.seconds) 			#średnia prękość między dwoma pkt [m/s]
	
	#to wystąpi dla każdych danych 
    dystans=sum(dist)			#zwracamy długość trasy (pozioma)
	
	#jeśli będą elewacje
    if alt_dif != [0]:
        wejscia=0
        zejscia=0
        for h in alt_dif:
            if h >= 0:
                wejscia = wejscia + h
            else:
                zejscia = zejscia + h
                
                wejscia=round(wejscia,3) 				#suma wejść
                zejscia=abs(round(zejscia,3))		#suma zejść
                Hmax=max(el) 						#min wysokość
                Hmin=min(el) 						#max wysokość
                dH=Hmax - Hmin			#całkowite przewyższenie
                
    if time_dif != [0]:
        timeH=sum(time_dif)/3600
        h,m,s=d_m_s(timeH)
        Vsr = dystans/(timeH*3600)
        return dystans, Vsr, dH, wejscia, zejscia, Hmax, Hmin, h, m, s
