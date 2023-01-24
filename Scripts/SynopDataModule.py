import numpy as np
from datetime import datetime as dt


def read_raw_data( file_in , undef = -9999.99 ) :
    
   data = dict()  #We will put the data in this dictionary.

   with open( file_in ) as f:
      lines = f.readlines()
      
   #Remove the header
   lines = lines[27:]
   #Get the length
   ndates = len( lines )   
   
   #Allocate temporary variables.
   dates = list()
   pressure = np.zeros( ndates )
   temperature = np.zeros( ndates )
   dewpoint = np.zeros( ndates )
   windspeed = np.zeros( ndates )
   winddir = np.zeros( ndates )
   vis = np.zeros ( ndates )

   for ii in range( ndates ) : 
      #print( lines[ii] )
      if ( lines[ii][59:66] != '       '  ) :
         pressure[ii] = float( lines[ii][59:66] )
      else  :
         pressure[ii] = undef
      if ( lines[ii][22:27] != '     '  ) :
         temperature[ii] = float( lines[ii][22:27] )
      else  :
         temperature[ii] = undef
      if ( lines[ii][46:50] != '    '  ) :
         dewpoint[ii] = float( lines[ii][46:50] )
      else  :
         dewpoint[ii] = undef
      if ( lines[ii][37:40] != '   '  ) :
         winddir[ii] = float( lines[ii][37:40] )
      else  :
         winddir[ii] = undef
      if ( lines[ii][41:44] != '   '  ) :
         windspeed[ii] = float( lines[ii][41:44] )
      else  :
         windspeed[ii] = undef
      if ( lines[ii][29:32] != '   '  ) :
         vis[ii] = float( lines[ii][29:32] )
      else  :
         vis[ii] = undef

      if ( lines[ii][19] == ' ' ) :
         mystrdate =  lines[ii][8:16] + '0' + lines[ii][20:21] 
      else :
         mystrdate =  lines[ii][8:16] + lines[ii][19:21] 
      #Convert the date to a date object. 
      dates.append( dt.strptime( mystrdate , '%d%m%Y%H' ) )
          
      
   rh = rh_from_dewpoint( temperature , dewpoint , undef )
   
   kmvis = synopvis_to_kmvis( vis , undef )

   data['dates'] = dates
   data['temperature'] = temperature
   data['dewpoint'] = dewpoint
   data['windspeed'] = windspeed   
   data['winddir'] = winddir
   data['vis'] = kmvis
   data['rh'] = rh
   data['pressure'] = pressure
   data['undef'] = undef


   return data
   
         
def rh_from_dewpoint( T , Td , undef ) :
    
    #T and Td in degrees celsious
    #This function uses Bolton's formula.
    es_t = 6.112 * np.exp( 17.67 * T / ( T + 243.5 ) )
    es_td = 6.112 * np.exp( 17.67 * Td / ( Td + 243.5 ) )
    rh = es_td / es_t 
    rh[ np.logical_or(T == undef , Td == undef) ] = undef 
    rh[ Td > T ] = undef 
    
    return rh 


def synopvis_to_kmvis( synop_vis , undef ) :
    
#%%%%%TABLA DE CONVERSION DE VISIBILIDAD
#%00 <100m   %50 5 km                  %80 30 km      %96 4km
#%01 100m    %51,52,53,54,55 no se usan%81 35km       %97 10 km
#%02 200m    %56 6 km                  %82 40 km      %98 20 km
#%03 300m    %57 7 km                  %83 45 km      %99 >=50 km 
#%04 400m    %58 8 km                  %84 50 km 
#%05 500m    %59 9 km                  %85 55 km
#%06 600m    %60 10 km                 %86 60 km
#%07 700m    %61 11 km                 %87 65 km
#%08 800m    %62 12 km                 %88 70 km
#%09 900m    %63 13km                  %89 >70 km
#%10 1 km    %.....                    %90 <50m
#%11 1.1 km  %70 20 km                 %91 50m
#%12 1.2 km  %71 21 km                 %92 200m
#%13 1.3 km                            %93 500m
#%.....                                %94 1 km
#                                      %95 2 km

  km_vis = np.zeros( synop_vis.shape )
  ndates = km_vis.size
  for ii in range( ndates ) :
     if synop_vis[ii] == undef:
        km_vis[ii] = undef 
     if synop_vis[ii] < 50 and synop_vis[ii] > 0.0 :
        km_vis[ii] = synop_vis[ii] * 0.1  #Convert visibility to km. 
     if synop_vis[ii] >= 56 and synop_vis[ii] <= 80 :
        km_vis[ii] = synop_vis[ii] - 50.0 
     if synop_vis[ii] == 81 :
        km_vis[ii] = 35.0
     if synop_vis[ii] == 82 :
        km_vis[ii] = 40.0
     if synop_vis[ii] == 83 :
        km_vis[ii] = 45.0
     if synop_vis[ii] == 84 :
        km_vis[ii] = 50.0
     if synop_vis[ii] == 85 :
        km_vis[ii] = 55.0
     if synop_vis[ii] == 86 :
        km_vis[ii] = 60.0
     if synop_vis[ii] == 87 :
        km_vis[ii] = 65.0
     if synop_vis[ii] == 88 :
        km_vis[ii] = 70.0
     if synop_vis[ii] == 89 :
        km_vis[ii] = 70.0 #Technically this should be greater than 70.
        
     if synop_vis[ii] == 90 :
        km_vis[ii] = 0.0
     if synop_vis[ii] == 91 :
        km_vis[ii] = 0.05
     if synop_vis[ii] == 92 :
        km_vis[ii] = 0.2
     if synop_vis[ii] == 93 :
        km_vis[ii] = 0.5
     if synop_vis[ii] == 94 :
        km_vis[ii] = 1.0
     if synop_vis[ii] == 95 :
        km_vis[ii] = 2.0
     if synop_vis[ii] == 96 :
        km_vis[ii] = 4.0                
     if synop_vis[ii] == 97 :
        km_vis[ii] = 10.0        
     if synop_vis[ii] == 98 :
        km_vis[ii] = 20.0        
     if synop_vis[ii] == 99 :
        km_vis[ii] = 50.0        

        
  return km_vis 



