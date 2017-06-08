#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 22:43:41 2017

@author: ning mei
The function (time frequency convolution) takes .tfc files and return attributions in the file. 
Translation from BESA Matlab functions.
"""

import numpy as np
def attribution(line,name):
    return [attr for attr in line.split(' ') if (name in attr)][0].split('=')[-1]
def tfc(filename):
    result ={'data':[]};ch_count,freq_count=0,0;cnt=0
    with open(filename) as f:
        for ii,line in enumerate(f.readlines()):
            if line != '\n':
                
                #print(line)

                if ii == 0:
                    #print(line.split(' '),'\n\n\n')
                    for attr in line.split(' '):
                        if 'DataType' in attr:
                            result['DataType']=attr.split('=')[-1]
                        elif 'NumberTrials' in attr:
                            result['NumberTrials']=int(attr.split('=')[-1])


                    result['NumberTimeSamples'] = float(attribution(line,'NumberTimeSamples'))
                    result['TimeStartInMS'] = float(attribution(line,'TimeStartInMS'))
                    result['TimeIntervalInMS'] = float(attribution(line,'IntervalInMS'))
                    result['NumberFrequencies'] = float(attribution(line,'NumberFrequencies'))
                    result['FreqStartInHZ'] = float(attribution(line,'FreqStartInHz'))
                    result['FreqIntervalInHZ'] = float(attribution(line,'FreqIntervalInHz'))
                    result['NumberChannels'] = float(attribution(line,'NumberChannels'))
                    # handle time
                    result['time']=np.linspace(result['TimeStartInMS'],
                                              result['TimeStartInMS']+result['TimeIntervalInMS']*(result['NumberTimeSamples']-1),
                                              result['NumberTimeSamples'])

                    # handle frequency
                    result['Frequency']=np.linspace(result['FreqStartInHZ'],
                                                   result['FreqStartInHZ']+result['FreqIntervalInHZ']*(result['NumberFrequencies']-1),
                                                   result['NumberFrequencies'])
                    result['data'] = np.zeros((int(result['NumberChannels']),
                                              int(result['NumberTimeSamples']),
                                              int(result['NumberFrequencies'])))
                elif len(line.split(' '))-1 == result['NumberChannels']:
                    result['Channel']=line.split(' ')[:-1]
                else:
                    #print(ch_count,freq_count)
                    if len(line) > 2:
                        result['data'][ch_count,:,freq_count]=np.array([float(n) for n in line.split('\t')[:-1]])
                        if freq_count >= result['NumberFrequencies']-1:
                            freq_count = 0
                            ch_count +=1
                        else:
                            freq_count +=1
    
                        cnt += 1
        
    return result
