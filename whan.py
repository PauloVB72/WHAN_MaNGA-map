import numpy as np, matplotlib.pyplot as plt

from colour import Color

from matplotlib import colors
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.pyplot import cm

import marvin
from marvin import config
from marvin.tools import Cube, Image
from marvin.tools.quantities.map import Map
#from marvin.tools import Maps 
from marvin.tools.maps import Maps
import marvin.utils.plot.map as mapplot

import warnings
warnings.filterwarnings('ignore')


def color_wcat(col1,col2,num): 
    
    c1 = Color(col1)
    c2 = Color(col2)
    colors = list(c1.range_to(c2,num))        
    return colors


class WHAN:
    
    """MODULE WHAN, this creates a WHAN diagram and map considering the emission of each spaxel in a MaNGA galaxy"""
    
    def __init__(self,plateifu,snr=1,**kwargs):
        
        self.__dict__.update(kwargs)
        
        
        self.plateifu = plateifu
        self.maps = Maps(plateifu=self.plateifu)
        
        self.niiha = self.maps.emline_gflux_nii_6585/self.maps.emline_gflux_ha_6564
        self.ewha = self.maps['emline_sew_ha_6564']
        self.ewnii = self.maps['emline_sew_nii_6585']
        
        self.logniiha = np.log10(self.niiha.value)
        
        self.niiha_low_snr = mapplot.mask_low_snr(self.niiha.value, self.niiha.ivar, snr_min=snr)
        self.ewha_low_snr = mapplot.mask_low_snr(self.ewha.value, self.ewha.ivar, snr_min=snr)
        self.ewnii_low_snr = mapplot.mask_low_snr(self.ewnii.value, self.ewnii.ivar, snr_min=snr)
        self.low_snr = np.logical_or(self.niiha_low_snr,self.ewha_low_snr, self.ewnii_low_snr)
        
        
        self.ivar = self.ewha.value.copy()
        self.ivar[self.low_snr] = 0
        self.nocov = self.ewha.pixmask.get_mask('NOCOV')
        
        
    def map_plot(self, num=8, path=None, **kwargs):
        
        plateifus = self.plateifu

        niiha_range1 = np.linspace(-0.58,-0.4,num)[::-1]
        niiha_range2 = np.linspace(-0.4,-0.25,num)
        ewha_range1 = np.linspace(3,6.,num+1)[::-1]
        ewha_range2 = np.linspace(1.,3.,num)[::-1]

        value = self.ewha.value.copy()

        #PSF
        for indx in range(num):
            if indx != np.max(num)-1:
                psf = (self.logniiha < niiha_range1[indx]) & (self.logniiha > niiha_range1[indx+1]) & (self.ewha.value > 3)
                value[psf] = float(indx)+1

            else:
                psf = (self.logniiha < niiha_range1[indx]) & (self.ewha.value > 3)
                value[psf] = float(indx)+1

        #SAGN       
        for indx in range(num):
            if indx != np.max(num)-1:
                sagn = (self.logniiha > niiha_range2[indx]) & (self.logniiha < niiha_range2[indx+1]) & (self.ewha.value > 6)
                value[sagn] = float(indx)+1+num

            else:
                sagn = (self.logniiha > niiha_range2[indx]) & (self.ewha.value > 6)
                value[sagn] = float(indx)+1+num
        #WAGN
        for indx in range(num):
            if indx != np.max(num)-1:
                wagn = (self.logniiha> -0.4) & ((self.ewha.value > ewha_range1[indx+1]) & (self.ewha.value < ewha_range1[indx]))
                value[wagn] = float(indx)+1+2*num

            else:
                wagn = (self.logniiha> -0.4) & ((self.ewha.value > ewha_range1[indx+1]) & (self.ewha.value < ewha_range1[indx]))
                value[wagn] = float(indx)+1+2*num

        #RG
        for indx in range(num):
            if indx != np.max(num)-1:
                rg = (self.ewha.value < ewha_range2[indx]) & (self.ewha.value > ewha_range2[indx+1])
                value[rg] = float(indx)+1+3*num
            else:
                rg = (self.ewha.value < ewha_range2[indx])
                value[rg] = float(indx)+1+3*num

        #PG
        pg = (self.ewha.value < 0.5) & (self.ewnii.value < 0.5)
        value[pg] = float(4*num +2)

        #Colour range for each WHAN category

        color_1= [str(color_wcat('lightblue','royalblue',num)[i]) for i in range(num)]
        color_2= [str(color_wcat('plum','darkviolet',num)[i]) for i in range(num)]
        color_3= [str(color_wcat('seagreen','palegreen',num)[i]) for i in range(num)]
        color_4= [str(color_wcat('peachpuff','tomato',num)[i]) for i in range(num)]

        color_tot = [color_1+color_2+color_3+color_4+['red']]  
        cmap = colors.ListedColormap(color_tot[0])
        cb_num = len(color_tot[0])


        fig, ax, cb = mapplot.plot(value=value, ivar=self.ivar, mask=self.nocov, cmap=cmap, 
                                   use_masks='NOCOV', return_cb=True, cbrange=(cb_num,1),
                                   title='WHAN Map {}'.format(plateifus))

        cb_tick = np.arange(0,cb_num)
        cb_tickla = []
        
        for i in range(cb_num):
            lab = ''
            if i == int(num/2):
                lab = 'PSF'
                cb_tickla.append(lab)
            elif i == 1+int(num/2)+num:
                lab = 'sAGN'
                cb_tickla.append(lab)
            elif i == 1+int(num/2)+2*num:
                lab = 'wAGN'
                cb_tickla.append(lab)
            elif i == 1+int(num/2)+3*num:
                lab = 'RG'
                cb_tickla.append(lab)
            elif i == np.max(cb_num)-1:
                lab = 'PG'
                cb_tickla.append(lab)
            else: 
                cb_tickla.append(lab)

        cb.set_ticks(cb_tick)
        cb.set_ticklabels(cb_tickla)
        
        if path == None:
            pass
        else:
            plt.savefig(path+'map_'+self.plateifu+'.png', 
                        bbox_inches='tight', pad_inches=0.2, transparent=True, facecolor='w')
            
        plt.show()
        
    def diagram_plot(self, num=8, path=None, **kwargs):
        
        niiha_range1 = np.linspace(-0.58,-0.4,num)[::-1]
        niiha_range2 = np.linspace(-0.4,-0.25,num)
        ewha_range1 = np.linspace(3,6.,num+1)[::-1]
        ewha_range2 = np.linspace(1.,3.,num)[::-1]
        
        
        plateifus = self.plateifu
        mask = self.nocov | self.low_snr
        logniiha = self.logniiha[mask == 0]
        ewha = self.ewha.value[mask == 0]
        ewnii = self.ewnii.value[mask == 0]

        value = ewha.copy()

        color_1= [str(color_wcat('lightblue','royalblue',num)[i]) for i in range(num)]
        color_2= [str(color_wcat('plum','darkviolet',num)[i]) for i in range(num)]
        color_3= [str(color_wcat('seagreen','palegreen',num)[i]) for i in range(num)]
        color_4= [str(color_wcat('peachpuff','tomato',num)[i]) for i in range(num)]

        plt.figure()

        for indx in range(num):
            if indx != np.max(num)-1:
                psf = (logniiha < niiha_range1[indx]) & (logniiha > niiha_range1[indx+1]) & (ewha > 3)
                plt.plot(logniiha[psf], ewha[psf], 'o', color=color_1[indx], alpha=0.7)

            else:
                psf = (logniiha < niiha_range1[indx]) & (ewha > 3)
                plt.plot(logniiha[psf], ewha[psf], 'o', color=color_1[indx], alpha=0.7,label=r'$\rm PSF$')

        #SAGN       
        for indx in range(num):
            if indx != np.max(num)-1:
                sagn = (logniiha > niiha_range2[indx]) & (logniiha < niiha_range2[indx+1]) & (ewha > 6)
                plt.plot(logniiha[sagn], ewha[sagn], 'o', color=color_2[indx], alpha=0.7)

            else:
                sagn = (logniiha > niiha_range2[indx]) & (ewha > 6)
                plt.plot(logniiha[sagn], ewha[sagn], 'o', color=color_2[indx], alpha=0.7, label=r'$\rm sAGN$')
        #WAGN

        for indx in range(num):
            if indx != np.max(num)-1:
                wagn = (logniiha> -0.4) & ((ewha > ewha_range1[indx+1]) & (ewha < ewha_range1[indx]))
                plt.plot(logniiha[wagn], ewha[wagn], 'o', color=color_3[indx], alpha=0.7)

            else:
                wagn = (logniiha> -0.4) & ((ewha > ewha_range1[indx+1]) & (ewha < ewha_range1[indx]))
                plt.plot(logniiha[wagn], ewha[wagn], 'o', color=color_3[indx], alpha=0.7, label=r'$\rm wAGN$')

        #RG
        for indx in range(num):
            if indx != np.max(num)-1:
                rg = (ewha < ewha_range2[indx]) & (ewha > ewha_range2[indx+1])
                plt.plot(logniiha[rg], ewha[rg], 'o', color=color_4[indx], alpha=0.7)

            else:
                rg = (ewha < ewha_range2[indx])
                plt.plot(logniiha[rg], ewha[rg], 'o', color=color_4[indx], alpha=0.7, label=r'$\rm RG$')

        pg = (ewha < 0.5) & (ewnii < 0.5)
        plt.plot(logniiha[pg], ewha[pg], 'o', color='red', alpha=0.7, label=r'$\rm Passive$')

        plt.yscale('log')
        plt.title(r'$\rm WHAN~Diagram~ {}$'.format(plateifus), fontsize=10)
        plt.xlabel(r'$\rm log~[N_{II}]/H_\alpha$', fontsize=14)
        plt.ylabel(r'$\rm W_{H_\alpha}~[\AA]$', fontsize=14)
        plt.legend()

        if path == None:
            pass
        else:
            plt.savefig(path+'diagram_'+self.plateifu+'.png', 
                        bbox_inches='tight', pad_inches=0.2, transparent=True, facecolor='w')
        
        plt.show()
