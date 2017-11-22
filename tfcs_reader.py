# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:18:45 2017

@author: ning

The function (time frequency convolution) takes .tfcs files and return attributions in the file. 
Translation from BESA Matlab functions.
"""
import numpy as np
import re
def tfcs_reader(fileName):
    with open(fileName,'r') as fp:
        tfc_data = {}
        n_trials = 0
        n_channels = 0
        n_freqs = 0
        for ii, tline in enumerate(fp.readlines()):
            tline = tline.strip()
            #print(tline)
            if 'Trial' in tline:
                n_trials += 1
                n_channels = 0
                n_freqs = 0
                tfc_data['trial%d'%n_trials] = {}
            elif 'Channel' in tline:
                n_channels += 1
                n_freqs = 0
                tfc_data['trial%d'%n_trials]['channel%d'%n_channels] = {}
            else:
                tline = tline.strip()
                temp = re.split('\t',tline)
                n_samples = np.array(temp).shape[0]
                n_freqs += 1
                tfc_data['trial%d'%n_trials]['channel%d'%n_channels]['freq%d'%n_freqs] = []
                for jj in range(n_samples):
                    two_reals = temp[jj]
                    a,b = re.findall('\d+\.\d+',two_reals)
                    value = np.complex(float(a),float(b))
                    tfc_data['trial%d'%n_trials]['channel%d'%n_channels]['freq%d'%n_freqs].append(value)

    results = np.zeros((len(tfc_data.keys()),
                        len(tfc_data['trial1'].keys()),
                        len(tfc_data['trial1']['channel1'].keys()),
                        len(tfc_data['trial1']['channel1']['freq1'])))

    for ii, key_trial in enumerate(tfc_data.keys()):
        for jj, key_ch in enumerate(tfc_data[key_trial].keys()):
            for kk,key_freq in enumerate(tfc_data[key_trial][key_ch].keys()):
                results[ii,jj,kk,:] = np.array(tfc_data[key_trial][key_ch][key_freq])
    return results,tfc_data