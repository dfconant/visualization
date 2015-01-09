#ERP.py


import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy as sp
import scipy.io
import math
import plotly.plotly as py 
import bisect

def plotERP(D,onset,fs,anatomy,iPy):
#Given a electrodesXtimeXtrials matrix, generates ERPs with 1 sec on 
#either side of the (user defined) onset
#Transposed from Ben Dichter's plotERP.m
#David Conant 12/17/14 

    ERP = np.nanmean(D,axis=2);
    ERPerr = np.nanstd(D,axis=2)/math.sqrt(D.shape[2])
    
    minall = np.nanmin(D)
    maxall = np.nanmax(D)
    
    ind = np.arange(onset-fs,onset+fs,1)
    ind = ind.astype(int)
    t = ind/float(fs) - onset/fs
    
    c = np.empty([256,3],dtype=int)
    c[:] = [0,0,0]
    if anatomy:
        anat = sp.io.loadmat('EC56_anat.mat')
        vsmc = np.concatenate([anat['anatomy'][0][0][3],anat['anatomy'][0][0][4]],axis=1)
        stg = anat['anatomy'][0][0][6]
        vsmc = vsmc -1; stg = stg -1;
        c[vsmc] = [0,0,1]
        c[stg] = [0,1,0]
        
    fig, axes = plt.subplots(figsize=(24,16))
    axes.axis('off')
    for e in range(256):

        ax = fig.add_subplot(16,16,e+1)
        d = ERP[e,ind]
        err = ERPerr[e,ind]
        plt.plot(t,d,color=c[e])
        plt.fill_between(t,d-err,d+err,color=c[e])
        plt.ylim([-1,2])
        plt.text(-.9,1.2,str(e+1))
        plt.plot([0,0],[-1,2])
        if e == 0:
            plt.yticks([-1,2])
            plt.xticks([])
        elif (e+1) > 240:
            plt.xticks([-1,0,1])
            plt.yticks([])
        else:
            plt.xticks([])
            plt.yticks([])
            
    plt.tight_layout()    
    plt.subplots_adjust(hspace=0.1,wspace=0.1)
    '''
    if iPy:
        import plotly.tools as tls
        tls.set_credentials_file(
        username="dfconant", 
        api_key="7iicqah00e")
        mpl_fig1 = plt.gcf()
        py.iplot_mpl(mpl_fig1, filename='EC34_Vowel_ERPs')
    '''
    #savefig("EC34_Vowel_ERPs.pdf") 
    


def plotERPcategories(D,onset=400,fs=400,anatomy=0,cat=[],ofInterest = range(9),scaling = []):
    ERP = []; ERPerr = []; h = []; l = [];
    
    #All vowels
    for i in ofInterest:
        ERP.append(np.nanmean(D[:,:,np.where(cat==i)[0]],axis=2))
        ERPerr.append(np.nanstd(D[:,:,np.where(cat==i)[0]],axis=2)/math.sqrt(D.shape[2]))
        h.append(np.nanmax(ERP[-1]))
        l.append(np.nanmin(ERP[-1]))
    
    squares = np.square(range(17))
    numFeats = D.shape[0]
    if math.sqrt(numFeats).is_integer():
        spDim = numFeats
    else:
        spDim = squares[bisect.bisect_right(squares,numFeats)]
    
    if not scaling:
        scaling = [np.nanmin(l),np.nanmax(h)]
    
    ind = np.arange(onset-fs,onset+fs,1)
    ind = ind.astype(int)
    t = ind/float(fs) - onset/fs
    
    c = np.empty([256,3],dtype=int)
    c[:] = [0,0,0]
    '''
    if anatomy:
        anat = sp.io.loadmat('EC56_anat.mat')
        vsmc = np.concatenate([anat['anatomy'][0][0][3],anat['anatomy'][0][0][4]],axis=1)
        stg = anat['anatomy'][0][0][6]
        vsmc = vsmc -1; stg = stg -1;
        c[vsmc] = [0,0,1]
        c[stg] = [0,1,0]
    '''
    cm = plt.get_cmap('hsv')
    vowels = np.array(['AA','AE','AH','EH','ER','IH','IY','UH','UW'])
    fig, axes = plt.subplots(figsize=(24,16))
    axes.axis('off')
    ax = [0]*len(ofInterest)
    for c in range(len(ofInterest)):
        col = cm(1.*c/len(ofInterest))
        for e in range(numFeats):
            fig.add_subplot(math.sqrt(spDim),math.sqrt(spDim),e+1)               
            d = ERP[c][e,ind]
            err = ERPerr[c][e,ind]

            if e == 0:
                ax[c], = (plt.plot(t,d,color=col))
            else:
                plt.plot(t,d,color=col)

           # plt.plot(t,d,color=col)
            plt.fill_between(t,d-err,d+err,color=col)
            plt.ylim([scaling[0],scaling[1]])
            plt.text(-.9,1.2,str(e+1))
            plt.plot([0,0],[scaling[0],scaling[1]])
            if e == 0:
                plt.yticks([scaling[0],scaling[1]])
                plt.xticks([])
            elif (e+1) > 240:
                plt.xticks([-1,0,1])
                plt.yticks([])
            else:
                plt.xticks([])
                plt.yticks([])
                
    plt.figlegend( ax,vowels[ofInterest],'lower left' )        
    plt.tight_layout()    
    plt.subplots_adjust(hspace=0.1,wspace=0.1)

    #savefig("EC34_Vowel_ERPs.pdf") 