#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 13:34:16 2020

@author: melissafasol
"""

###IMPORT LIBRARIES

import glob
import os

import mne
from OpenEphys import *
from initial_processes import *
from numpy import transpose
from matplotlib import pyplot as plt
from mne.time_frequency import (tfr_multitaper, tfr_stockwell, tfr_morlet,
                                tfr_array_morlet)
from seizure_finder import *
from power_spectrum import *
from Multi_channel_analysis import *
import parameters
prm = parameters.Parameters()
import xlsxwriter

global w

###

###DEFINE PARAMETERS

def init_params(): #Defines initial parameters used throughout.
    prm.set_filepath('//Users/melissafasol/code/MNE_Alfredo/190604/2019-06-04_15-07-13')#E:\\ERUK\\Tethered Recordings\\ERUK Animals\\180917\\2018-09-17_11-11-58\\
    prm.set_filename('seizure_1_793.xlsx')
    prm.set_excelpath('C://Users//melissafasol/code/MNE_Alfredo/')
    prm.set_excelname('seizure_1_793.xls')
    prm.set_channel_combo_name('channel_combo_hpc_m_i.xlsx')
    prm.set_sampling_rate(1000)
    prm.set_starttime(256) #using as experiment
    prm.set_endtime(286)   
    prm.set_starttime2(256) #using as control.
    prm.set_endtime2(286)
    prm.set_windowtype('hann')
    prm.set_stimfreq(10)
    prm.set_headstages(4)
    prm.set_stimduration(30)
    
    
#initialisetheparameters
    init_params()
    
###
    
###IMPORT DATA
    
    
    a
'loads the data in MNE format'
def load_16channel_opto_mne(headstage_number):
    
    'Function below loads the data and makes the MNE data object, specify how many headstages'
    custom_raw=load_16_channel_opto_mne(4)
    
    'Specific times to analyse, load excel spreadsheet below'
    analysis_times=import_spreadsheet(prm.set_excelpath() + prm.set_excelname()) #importsexcelspreadsheet

    'This is to get the channel combination array' 
    channel_combo=import_spreadsheet(prm.set_excelpath() + prm.set_channel_combo_name())


    data=loadFolderToArray(prm.get_filepath(), channels = 'all', chprefix = 'CH', dtype = float, session = '0', source = '102')#######load file
    data_adc=loadFolderToArray(prm.get_filepath(), channels = 'all', chprefix = 'ADC', dtype = float, session = '0', source = '102')#######load file8

    if headstage_number == 4:
    
        data= np.append(data,(np.zeros((data.shape[0],1), dtype=int64)), axis=1) #a copy of arr with values appended to axis (axes are defined for arrays with more than one dimension)
        #data[:,64]=(data_adc[:,0]*300) #Multiply by 300 to have about the same scale for optogenetics.
        
        datatp=data.transpose()#Array from openephys has to be transposed to match RawArray MNE function to create.
        del data
        #del data_adc
        
        'Below I make the channel names and channel types, this should go in the parameters file later.'
        
        n_channels=65
        
        channel_names=['hpc_m_i_a', 'hpc_m_i_b', 'somato_a', 'somato_b', 'BLANK', 
                       'hpc_r_c_a', 'hpc_r_c_b', 'hpc_m_c_a', 'hpc_m_c_b', 'hpc_c_c_a', 
                       'hpc_c_c_b', 'EMG', 'cb_a', 'cb_b', 'hpc_c_i_a', 'hpc_c_i_b',
                       'hpc_m_i_a_2', 'hpc_m_i_b_2', 'somato_a_2', 'somato_b_2', 'BLANK_2', 
                       'hpc_r_c_a_2', 'hpc_r_c_b_2', 'hpc_m_c_a_2', 'hpc_m_c_b_2', 'hpc_c_c_a_2', 
                       'hpc_c_c_b_2', 'EMG_2', 'cb_a_2', 'cb_b_2', 'hpc_c_i_a_2', 'hpc_c_i_b_2',
                       'hpc_m_i_a_3', 'hpc_m_i_b_3', 'somato_a_3', 'somato_b_3', 'BLANK_3', 
                       'hpc_r_c_a_3', 'hpc_r_c_b_3', 'hpc_m_c_a_3', 'hpc_m_c_b_3', 'hpc_c_c_a_3', 
                       'hpc_c_c_b_3', 'EMG_3', 'cb_a_3', 'cb_b_3', 'hpc_c_i_a_3', 'hpc_c_i_b_3',
                       'hpc_m_i_a_4', 'hpc_m_i_b_4', 'somato_a_4', 'somato_b_4', 'BLANK_4', 
                       'hpc_r_c_a_4', 'hpc_r_c_b_4', 'hpc_m_c_a_4', 'hpc_m_c_b_4', 'hpc_c_c_a_4', 
                       'hpc_c_c_b_4', 'EMG_4', 'cb_a_4', 'cb_b_4', 'hpc_c_i_a_4', 'hpc_c_i_b_4',
                       'Opto']
        channel_types=['eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','emg','eeg','eeg','eeg','eeg',
                       'eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','emg','eeg','eeg','eeg','eeg',
                       'eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','emg','eeg','eeg','eeg','eeg',
                       'eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','emg','eeg','eeg','eeg','eeg',
                       'stim']
    
        'This creates the info that goes with the channels, which is names, sampling rate, and channel types.'
        info = mne.create_info(channel_names, prm.get_sampling_rate(), channel_types)
    
        'This makes the object that contains all the data and info about the channels.'
        'Computations like plotting, averaging, power spectrums can be performed on this object'
        custom_raw = mne.io.RawArray( datatp, info)
        del datatp
        return custom_raw
        
'Large function to calculate individual coherence for individual time windows and channel combinations in multi-channel recording'
def global_coherence(analysis_times, channel_combo, custom_raw):  ##Do individual coherence for series of channels.
    #Analysis times is times to compare, see brain state function and channel combo function.
    
    cc_num_rows, cc_num_cols=channel_combo.shape  #Here getting size of channel combination array.
    at_num_rows, at_num_cols=analysis_times.shape  #Get size of analysis times array.
    coh_array = zeros(shape=((at_num_rows)*(cc_num_rows), 1001)) #Make array of zeros to put data in.
  

#    print(at_num_rows)
#    print(cc_num_rows)
 
    
    for m in range(0, at_num_rows): #For loop to run through all analyis times.

        start_time=(analysis_times.item(m,1))
        prm.set_starttime(start_time)
        end_time=(analysis_times.item(m,2))
        prm.set_endtime(end_time)
      
       
        
        for n in range(0, cc_num_rows):  #For loop to run through all channel combinations.
            
            chan_1=(channel_combo.item(n,0))
            prm.set_channel_1(int(chan_1)) 
            chan_2=(channel_combo.item(n,1))
            prm.set_channel_2(int(chan_2))
            
            #Below is an MNE function to get index from data object.
            t_idx=custom_raw.time_as_index([prm.get_starttime(), prm.get_endtime()])
            sub_data1, times =custom_raw[prm.get_channel_1(), t_idx[0]:t_idx[1]] #Here retrieve specified indexed and channel data/
            sub_data2, times =custom_raw[prm.get_channel_2(), t_idx[0]:t_idx[1]]
               
            f, coh=coherence_values(sub_data1, sub_data2, prm.get_sampling_rate) #use coherence_values function to get coherence.
            coh_array_index=int(n+cc_num_rows*m)  #Figure out index of where to place data,
            coh_array[coh_array_index,:]=coh

        print('Calculating global coherence')
    coh_average=average(coh_array, 0) #Calculate averages and STDs which will be returned,
    coh_std=std(coh_array, 0)