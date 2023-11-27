#WHAN Diagram plots code


Work by Nora Castillo and Maria Argudo Fernandez. This code presents a new way to understand the WHAN diagram by Cid Fernandez et al 2011. Using the MaNGA data emission of NII and Hα, we make a degraded ionization WHAN map for any galaxy in MaNGA. We define the following color categories:


[royalblue to lightblue]:


Pure starforming galaxies (PSF): log[NII]/Hα < −0.4 and WHα > 3 Å 


[plum to darkviolet]:


Strong AGN (sAGN): log[NII]/Hα > −0.4 and WHα > 6 Å 


[seagreen to palegreen]:


Weak AGN (wAGN): log[NII]/Hα > −0.4 and 3 < WHα < 6 Å 


[peachpuff to tomato]:


Retired galaxies (RG): WHα < 3 Å 


[red]:


Passive galaxies (PG): WHα < 0.5 Å and WNII < 0.5 Å 



The code is based manly in the degraded colors, you can change the number of bins for the degraded,
