#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 16:54:54 2019

@author: similarities
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
            self.x_backsubstracted = np.empty([1200, 1600])
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

            
            plt.figure(1)
            plt.imshow(self.picture)
            
            
            return self.picture
            
      
        
        def background(self):
            
            back_mean=np.mean(self.picture[self.ymin:self.ymax, :], axis = 0)
            
            i=1
            
            N=len(self.picture)-1
            
            while i<= N:
        
                self.x_backsubstracted[i,::] = self.picture[i,::]- back_mean[i]

                i = i+1
                
                
            plt.figure(2)
            
            plt.imshow(self.x_backsubstracted)
            plt.colorbar()
            plt.draw()
   
        def Intensity_map(self):
            integrated_lines = np.sum(self.x_backsubstracted[:,self.x_min:self.x_max], axis = 1)
            print(integrated_lines)
            integrated_density = np.sum(integrated_lines[:], axis = 0) 
            print(integrated_density)
            
            area_per_pixel = (0.24*1E-4)**2
            
            ND_focus=10**(-2.6)
            print(ND_focus, "focusND")
            
            self.ND2= 10**(-self.ND_filter)
            print(self.ND2, "ND in")
            
            resulting_ND =10**(-2.6+self.ND_filter)
            print(resulting_ND, "ND difference")
            
            tauL_long = 20*1E-15*(1+self.GVD/(self.tauL**2))
            
            EL_per_count = self.beamline_T*self.EL / (integrated_density)
            
            intensity_per_pixel = EL_per_count/(area_per_pixel*tauL_long)
            
            self.x_backsubstracted = self.x_backsubstracted*intensity_per_pixel* resulting_ND
            plt.figure(3)
            
            plt.imshow(self.x_backsubstracted,label=self.filedescription)
            plt.colorbar()
            plt.draw()
            plt.title(self.filedescription)
            plt.savefig(self.filedescription,  bbox_inches="tight", dpi = 1000)
            
   
            
    
    
    
   

   

  

            
       # def save_data(self):
         #   np.savetxt(self.filedescription+"_divergence_mrad"+".txt", self.FWHM_for_N, delimiter=' ', fmt='%1.4e')

            
     
            
            


# class gives the following params: ("filepath/filename',xmin [px], xmax [px],fundamental wavelength[um],ROI_y )
Picture1=Open_and_Plot_Picture('tiff/focus_tisa_-20320a_1.9ND_vac.tif', 3.8, 0.0,1.9,"20190125_20302steps_GVD0")
Picture1.open_file()
Picture1.background()
Picture1.Intensity_map()









