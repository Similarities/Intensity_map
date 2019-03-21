# Intensity_map
data_evaluation, image calculation

calculates intensity map (laser energy/(pulse duration * px)) for an imaged laser focus. Chirped pulse duration via GVD can be added, for different recordings 
ND filter can be normed to a given one.
Some constants (magnification, beamline transmission bla bla) need to be changed in the code itself.
The intereseting part here: does remove the background counts via a threshold 

Batch version has to be aligned to the filename * if GVD defocusing values are given there*
batch version saves pictures with the calculated colorbar scaling (either different energies, or different GVD)
unti now every picture has to be loaded manually.





