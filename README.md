Spatially resolved WHAN diagnotic diagram for MaNGA galaxies
------------------------------------------------------------

Python tool for the visualization of the spatially resolved WHAN diagnotic diagram for galaxies in the `MaNGA survey` (<https://www.sdss4.org/surveys/manga/>).

This code contains the visualisation tools developed for the A&A Article `A MaNGA view of isolated galaxy mergers in the star-forming Main Sequence` (<https://ui.adsabs.harvard.edu/abs/2025arXiv250210078V/abstract>) by P. Vasquez-Bustos, M. Argudo-Fernández, M. Boquien, N. Castillo-Baeza, A. Castillo-Rencoret, and D. Ariza-Quintana.
The code has been developed by Nora Castillo, Paulo Vásquez-Bustos, and Maria Argudo-Fernández, taking advantage of the `Marvin tools` (<https://github.com/sdss/marvin>) for the analysis of MaNGA data. This code aims to help in the understanding and visualisation of the spatially distributed emission in galaxies in 3D, using the WHAN diagnostic diagram by Cid Fernandez et al 2011. Using the MaNGA data emission of NII and Hα, the function created a colour gradient ionization WHAN map for any galaxy in MaNGA, providing the plate-ifu or MaNGA ID of the galaxy. This function is an updated version of the existing example tutorial for the creation of a WHAN map available in the `Marvin documentation` (<https://sdss-marvin.readthedocs.io/en/stable/tutorials/exercises.html>). 

The WHAN colour scheme
----------------------

We define the following color categories, based on the original definition of the WHAN categories:


* [royalblue to lightblue]

  Pure starforming galaxies (PSF): log[NII]/Hα < −0.4 and WHα > 3 Å 

* [plum to darkviolet]
  
  Strong AGN (sAGN): log[NII]/Hα > −0.4 and WHα > 6 Å 

* [seagreen to palegreen]
  
  Weak AGN (wAGN): log[NII]/Hα > −0.4 and 3 < WHα < 6 Å 

* [peachpuff to tomato]
  
  Retired galaxies (RG): WHα < 3 Å 

* [red]
  
  Passive galaxies (PG): WHα < 0.5 Å and WNII < 0.5 Å 


Theese are the default colour schemes per category, with a number of 8 bin for the colour gradient. The user can choose a different colour scheme, following the available colours in the matplotlib library, and a different number of bins. 


