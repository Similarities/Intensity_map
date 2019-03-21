#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 15:14:28 2019

@author: julia
"""


import matplotlib.pyplot as plt
import numpy as np





class Open_and_Plot_Picture:
        def __init__(self, filename,EL,GVD,ND_filter,filedescription):
            self.filename = filename
            # px size full picture * usually 0 - 2048

            self.ND_filter= ND_filter
            # defined Roi in x to avoid boarder effects

            # integration ROI y for each HHG line
            self.EL = EL
            self.picture = np.empty([])
            self.integrated = np.empty([])
            
            
                        #size of picture --> make to readout
            self.x_max = 1600
            self.y_max = 1200
            
            self.x_backsubstracted = np.zeros([self.y_max, self.x_max])
           # self.x_min = 0
            

            # Group velocity dispersion in fs^2
            self.GVD = GVD
            
            self.filedescription = filedescription
            
            #transmission of beamline 
            
            self.beamline_T = 0.56
            
            #(tauL in femtoseconds)
            self.tauL = 20






        def open_file(self):
            
            self.picture = plt.imread(self.filename)

            
            #plt.figure()
            
            #plt.imshow(self.picture)
            
            
            return self.picture
            
      
            
            
            
   
        def Intensity_map(self):

            self.x_backsubstracted[::,::] = self.picture[::,::]
            
            #constant background substraction - is a bit higher than the real background
            # sets all values below threshold to 0
            self.x_backsubstracted[self.x_backsubstracted < 1700]=0
            #print(self.x_backsubstracted[:,2],"linout background")
            
            #0.24um per px includes magnification
            area_per_pixel = (0.24*1E-4)**2
            
            # ND filter calculation, 2.6 is the strongest ND filter used
            # to which we norm the less attentuated picutres
            
            resulting_ND =10**(2.6-self.ND_filter)
            
            print(resulting_ND, "ND difference", 1/resulting_ND, "correction")
            
            #total count numbers in picture
            integrated_density = np.sum(self.x_backsubstracted[::,::])
            print(integrated_density, 'integrated counts')
            
                        
            EL_per_count = self.beamline_T*self.EL / (integrated_density*resulting_ND)
            
            #pulse duration + calculation for longer pulses by chirp via GVD
            tauL_long = 20*1E-15*(1+self.GVD/(self.tauL**2))
            
            intensity_per_pixel = EL_per_count/(area_per_pixel*tauL_long)
            
            #map
            self.x_backsubstracted = self.x_backsubstracted*intensity_per_pixel

            
            
            
            plt.figure()
            
            plt.imshow(self.x_backsubstracted,label=self.filedescription)
            plt.colorbar()
            plt.draw()
            plt.title(self.filedescription)
            plt.savefig(self.filedescription+".png",  bbox_inches="tight", dpi = 1000)


           
        def extract_mean_ROI(self):
            #note: integration of Intensity over some pixels is WRONG! 
            # since intensity is a function of the Area which we already set to 1px- size
            # mean value of some AREA is better approach
            integrated_sub_ROI = np.mean(self.x_backsubstracted[1100:1200,1300:1400])
            print(integrated_sub_ROI, "sub_ROI")
            
 



class Batch_Baker:  
    
    
    def __init__(self, filename,EL,GVD):
        
            self.filename = filename
            
            #ND filter value given in filename
            self.ND_filter= float(filename[24:27])
            
            print("ND:", self.ND_filter)

            #starting value for laser energy in J (small for batch energy, one value for batch GVD)
            self.EL = EL
            
            self.GVD = GVD
            
            self.filedescription = filename[17:22]          
            print(self.filedescription,"filedescription")
            

            
            
    def batch_energy(self):
        
        for i in range (0, 7):
            
            x = self.EL +0.5*i
            
            defocus = (20820-int(self.filedescription))*5
            
            print(defocus, "defocus")
            
            string_value1 = str(x) + "J "+self.filedescription + str(defocus) +"um"+str(self.GVD)
            
            print(string_value1, "string value")
            
            Picture1=Open_and_Plot_Picture(self.filename, x, self.GVD, self.ND_filter, string_value1)
            
            Picture1.open_file()
#Picture1.background()
            Picture1.Intensity_map()
            
            Picture1.extract_mean_ROI()
            
            
    def batch_GVD(self):
        
        for i in range (1, 5):
            
            self.GVD = self.GVD + 300

            defocus = (20820-int(self.filedescription))*5            
            
            string_value1 = str(self.EL) + "J "+self.filedescription + str(defocus) +"um"+"GVD"+str(self.GVD)
            
            print(string_value1, "string value")
            
            Picture1=Open_and_Plot_Picture(self.filename, self.EL, self.GVD, self.ND_filter, string_value1)
            
            Picture1.open_file()

            Picture1.Intensity_map()
            
           # Picture1.extract_mean_ROI()
            
            
            
        
            
   
            
    
    
    
   
Batch_Baker1 = Batch_Baker("tiff/focus_tisa_-20920a_2.6ND_vac.tif",3.5,0.)
#Batch_Baker1.batch_energy()
Batch_Baker1.batch_GVD()

            
       

    