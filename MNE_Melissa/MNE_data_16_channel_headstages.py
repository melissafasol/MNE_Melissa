
"""
Created on Tue Jun 26 16:54:00 2018

@author: Alfredo Gonzalez-Sulser, University of Edinburgh
email: agonzal2@staffmail.ed.ac.uk

This makes the objects for MNE.
"""

import glob
import os

import mne
from OpenEphys import *
from initial_processes import *
from numpy import transpose
from matplotlib import pyplot as plt
from mne.time_frequency import (tfr_multitaper, tfr_stockwell, tfr_morlet,
                                tfr_array_morlet)
from power_spectrum import *
import parameters
prm = parameters.Parameters()
import xlsxwriter
import pandas as pd
global w



def init_params(): #Defines initial parameters used throughout.
    prm.set_filepath('//Users/melissafasol/code/MNE_Alfredo/190608/2019-06-08_15-24-33')#E:\\ERUK\\Tethered Recordings\\ERUK Animals\\180917\\2018-09-17_11-11-58\\
    prm.set_filename('')
    prm.set_excelpath('//Users/melissafasol/code/MNE_Alfredo/')
    prm.set_excelname('seizure_1_793.xlsx')
#    prm.get_channel_combo_name('channel_combo_seizure1_793.xlsx')
    prm.set_sampling_rate(512)
    prm.set_starttime(260) #using as experiment
    prm.set_endtime(270)   
    prm.set_windowtype('hann')
    prm.set_headstages(4)
    

'Initialize the parameters'
init_params()
 


#stimulations = actual_stim_times(data,  prm.get_sampling_rate(), prm.get_headstages())  


'Function below loads each 16-channel-headstage individually.'
#data=load_16channel_opto_individually(4)


'Functions below load the data and make the MNE data object, specify how many headstages'
#Below loads 16 channel arrays.


custom_raw=load_16_channel_opto_mne(prm.get_headstages(), 'Entorhinal')

#Below loads 32-channel array.
#custom_raw=load_32_EEG("100")

'This is to make MNE array of filtered data through MNE filt function.'
#filt=custom_raw.filter(0, 480, fir_design='firwin')


'If you have specific times to analyse, load excel spreadsheet of them below.'

#analysis_times=import_spreadsheet(prm.get_excelpath() + prm.get_excelname()) #Imports spreadsheet
#stim=create_epochs(stimulations, prm.get_sampling_rate()) #Creates stim time array that MNE can read.

'This is if brain state epoch array is available'
#analysis_times=import_brain_state(prm.get_excelpath() + prm.get_excelname()) 

'This is if channel combination array is available for coherence is cross-frequency coupling analyses'
#channel_combo=import_channel_combo(prm.get_excelpath() + prm.get_channel_combo_name()) #

'This below is a function to get actual stimulation times. Load one individual headstage, non-MNE format.'
#stimulations = actual_stim_times(data,  prm.get_sampling_rate(), prm.get_headstages())    
#


'To do a basic plot below. The following can be added for specifc order of channels order=[4, 5, 3, 0, 1, 14, 15, 16]'
#colors=dict(mag='darkblue', grad='b', eeg='k', eog='k', ecg='m',
#     emg='g', ref_meg='steelblue', misc='k', stim='b',
#     resp='k', chpi='k')
#
#custom_raw.plot(None, 5, 20, 8,color = colors, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],show_options = "true" )#


'This is to plot coherence below'
#multiple_coherence(analysis_times, custom_raw)

'The following is to calculate coherence'

#coh_average, coh_std, f= global_coherence(analysis_times, channel_combo, custom_raw)

'Below is an MNE function to get index from data object.'
#t_idx=custom_raw.time_as_index([prm.get_starttime(), prm.get_endtime()])
#print(t_idx)
#sub_data1, times =custom_raw[0, t_idx[0]:t_idx[1]] #Here retrieve specified indexed and channel data/
#sub_data2, times =custom_raw[5, t_idx[0]:t_idx[1]]
               
#f, coh=coherence_values(sub_data1, sub_data2, prm.get_sampling_rate) #use coherence_values function to get coherence.
            
#coh2=np.transpose(coh)

#plt.plot(f,coh2)

print(custom_raw)

