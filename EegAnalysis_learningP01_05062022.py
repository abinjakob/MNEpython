#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:31:09 2022

@author: abinjacob
"""

#%% Libraries

import mne
# import numpy as np 
# import pandas as pd
from matplotlib import pyplot as plt


#%% importing data in mne 

my_data_location = '/Users/abinjacob/Documents/04. NIMHANS/EEG Basics/mne_data/MNE-sample-data/MEG/sample/sample_audvis_raw.fif'

#reading fif file 
raw_data = mne.io.read_raw(my_data_location) 

#summary of the data 
raw_data.info 

#know sample frequency
raw_data.info['sfreq']

#know chanels names
# raw_data.ch_names 

#%% Events
events = mne.find_events(raw_data)

#plot markers
# mne.viz.plot_events(events)

#renaming the events
#The numbers are replaced with sensible names

event_id = {
    'Auditory/Left': 1,
    'Auditory/Righ': 2,
    'Visual/Left': 3,
    'Visual/Right': 4,
    'Smiley': 5,
    'Button': 32
    }
event_id


#plot markers with new names given to the events
# mne.viz.plot_events(event_id = event_id, events= events)

#%% Plotting

#see the data 
raw_data.plot()

#see data with the markers
raw_data.plot(events=events, event_id=event_id)

#see the electrodes/sensors placement using the head map 
raw_data.plot_sensors(ch_type='eeg')


#%% Add a particular channel as bad 

raw_data.info['bads'] += ['EEG 051']
raw_data.plot_sensors(ch_type='eeg')


#%% Selecting the required subset of channels
#Always take a copy of the original file before making any modifications
#Syntax: filename.copy()

raw_eeg = raw_data.copy().pick_types(meg= False,
                                     eeg= True,
                                     eog= True,
                                     exclude=[])
#To know the length of the array
len(raw_eeg.ch_names)


#Take only 100 seconds of data
raw_eeg_cropped = raw_eeg.copy().crop(tmax= 100)
raw_eeg_cropped.times[-1]

#Filter the data
raw_eeg_cropped.load_data()
raw_eeg_cropped_filtered = raw_eeg_cropped.copy().filter(l_freq=0.1,
                                                         h_freq=40)

#%%

