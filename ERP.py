#ERP.py


import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy as sp
import scipy.io
import math

def plotERP(D,onset,fs):
#Given a electrodesXtimeXtrials matrix, generates ERPs with 1 sec on 
#either side of the (user defined) onset
#Transposed from Ben Dichter's plotERP.m
#David Conant 12/17/14 

    ERP = np.nanmean(D,axis=2);
    ERPerr = np.nanstd(D,axis=2)/D.shape[2]
    
    minall = np.nanmin(D)
    maxall = np.nanmax(D)
    
    ind = np.arange(onset-fs,onset+fs,1)
    ind = ind.astype(int)
    t = ind/float(fs) - onset/fs
    
    
    fig, axes = plt.subplots(figsize=(30,24))
    axes.axis('off')
    for e in range(256):

        ax = fig.add_subplot(16,16,e)
        d = ERP[e,ind]
        err = ERPerr[e,ind]
        plt.plot(t,d)
        plt.fill_between(t,d-err,d+err)
        plt.ylim([-1,2])
        if e == 0:
            plt.yticks([-1,2])
        elif (e+1)%16.0 == 0:
            plt.xticks([-1,0,1])
        else:
            plt.xticks([])
            plt.yticks([])
        
        
    plt.tight_layout()    
        
    rcParams['font.family'] = 'sans-serif'
    rcParams['text.usetex'] = False
    rcParams['axes.labelsize'] = 10
    rcParams['xtick.labelsize'] = 10
    rcParams['ytick.labelsize'] = 10
    rcParams['legend.fontsize'] = 10
        
    #savefig("EC34_Vowel_ERPs.pdf") 
    
