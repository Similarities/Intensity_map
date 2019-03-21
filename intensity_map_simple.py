#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 15:14:28 2019

@author: julia
"""


import matplotlib.pyplot as plt
import numpy as np





class Open_and_Plot_Picture:
        def __init__(self, filename,EL,GVD,ND_filter, filedescription):
            self.filename = filename
            # px size full picture * usually 0 - 2048
            self.ymin = 0
            self.ymax = 200
            self.ND_filter= ND_filter
            # defined Roi in x to avoid boarder effects

            # integration ROI y for each HHG line
            self.EL = EL
            self.picture = np.empty([])
            self.integrated = np.empty([])
            self.x_backsubstracted = np.zeros([1200, 1600])
            self.x_min = 0
            self.x_max = 1600
            self.y_max = 1200
            self.GVD = GVD
            self.filedescription = filedescription
            self.beamline_T = 0.56
            #(tauL in femtoseconds)
            self.tauL = 20


        def open_file(self):
            
            self.picture = plt.imread(self.filename)

            
            plt.figure()
            plt.imshow(self.picture)
            
            
            return self.picture
            
      
        
        def background(self):
            
            back_mean=np.mean(self.picture[self.ymin:self.ymax, :], axis = 0)+100
            
            i=1
            
            N=len(self.picture)-1
            
            while i<= N:
                
                self.x_backsubstracted[i,::] = self.picture[i,::]- 1400.
                

                i = i+1
                
                
            plt.figure()
            
            plt.imshow(self.x_backsubstracted)
            plt.colorbar()
            plt.draw()
   
        def Intensity_map(self):

            self.x_backsubstracted[::,::] = self.picture[::,::]
            area_per_pixel = (0.24*1E-4)**2
            
            
            resulting_ND =10**(2.6-self.ND_filter)
            print(resulting_ND, "ND difference", 1/resulting_ND, "correction")
            
            print(np.amax(self.x_backsubstracted),"maximum")

            self.x_backsubstracted[self.x_backsubstracted < 1700]=0
            print(self.x_backsubstracted[:,2],"linout background")
            
            integrated_density = np.sum(self.x_backsubstracted[::,::])
            print(integrated_density, 'integrated counts')
            
            
            tauL_long = 20*1E-15*(1+self.GVD/(self.tauL**2))
            
            EL_per_count = self.beamline_T*self.EL / (integrated_density*resulting_ND)
            
            intensity_per_pixel = EL_per_count/(area_per_pixel*tauL_long)
            
            self.x_backsubstracted = self.x_backsubstracted*intensity_per_pixel

            
            
            
            plt.figure()
            
            plt.imshow(self.x_backsubstracted,label=self.filedescription)
            plt.colorbar()
            plt.draw()
            plt.title(self.filedescription)
            plt.savefig(self.filedescription+".png",  bbox_inches="tight", dpi = 1000)
            
        def extract_mean_ROI(self):
            integrated_sub_ROI = np.mean(self.x_backsubstracted[1100:1200,1300:1400])
            print(integrated_sub_ROI*1E-19, "sub_ROI")
            
            
        
            
   
            
    
    
    
   

   

  

            
       # def save_data(self):
         #   np.savetxt(self.filedescription+"_divergence_mrad"+".txt", self.FWHM_for_N, delimiter=' ', fmt='%1.4e')

            
     
            
            


# class gives the following params: ("filepath/filename',xmin [px], xmax [px],fundamental wavelength[um],ROI_y )



for i in range (0, 7):
    x = 2.+0.5*i
    string_value1 = str(x) + 'J 21320a_m500s_m2.5mm'
    Picture1=Open_and_Plot_Picture('tiff/focus_tisa_-21320a_1.9ND_vac.tif', x, 0.0, 1.9, string_value1)
    Picture1.open_file()
#Picture1.background()
    Picture1.Intensity_map()
    Picture1.extract_mean_ROI()
    