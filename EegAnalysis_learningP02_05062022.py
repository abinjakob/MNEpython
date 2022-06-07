#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 20:08:22 2022

@author: abinjacob
"""

import matplotlib
import pathlib
import mne
from matplotlib import pyplot as plt

#%% Loading Data

raw_path = '/Users/abinjacob/Documents/04. NIMHANS/EEG Basics/mne_data/MNE-sample-data/MEG/sample/sample_audvis_raw.fif'
raw = mne.io.read_raw(raw_path)
raw

# raw.info

raw.plot()

#%% Events
events = mne.find_events(raw)

#plot markers
# mne.viz.plot_events(events)

#renaming the events
#The numbers are replaced with sensible names

event_id = {
    'Auditory/Left': 1,
    'Auditory/Right': 2,
    'Visual/Left': 3,
    'Visual/Right': 4,
    'Smiley': 5,
    'Button': 32
    }
event_id

#ADDITIONAL OPERATIONS
#find a particular event in the data | eg: with event 32
# [:,2] means all columns selected and raw 3 selected

# events[events[:,2] == 32]

#find the total number of events 
# len(events[events[:,2] == 32]) 
#OR
# len(events[events[:,2] == event_id['Auditory/Left']]) 

#to know the total number of events from 2 markers
# len(events[events[:,2] == event_id['Auditory/Right']])+ len(events[events[:,2] == event_id['Auditory/Left']])


#Plotting Raw data with markers on them 
raw.plot(events = events, event_id = event_id)


#%% Visualise the Sensors on topoplot 

raw.plot_sensors (ch_type='eeg')

#%% Adding a EEG channel as Bad 

#Channel 051 is added to the Bad list 
raw.info['bads']
raw.info['bads'] += ['EEG 051']
raw.plot_sensors(ch_type='eeg') #plotting again


#%% Choosing only a subset of the channels

#Always make a copy of the original data before any modifications 

raw_eeg = raw.copy().pick_types(meg=False, eeg=True, eog=True, exclude=[]) 
#exclude=[] is kept blank so that it does not ommit any channels. If not it will exclude the Bad channel
len(raw_eeg.ch_names)

# raw_eeg.info

#plotting the eeg channels
raw_eeg.plot(events=events, event_id=event_id)

#%% Cropping and Filtering

#cropping the data for first 100ms
raw_eeg_cropped = raw_eeg.copy().crop(tmax=100)
raw_eeg_cropped.times[-1] #looking at the last element [-1] of the timepoint after cropping 


#Filtering = adding low pass and high pass filter 
#Here as the data was not loaded in line 17 properly as it takes only a snipet of the information we have to load the file before filtering

raw_eeg_cropped.load_data()
raw_eeg_cropped_filtered = raw_eeg_cropped.copy().filter(l_freq=0.1, h_freq=40)


#Plotting unfiltered data | Also added a title for the plot as Unfiltered
raw_eeg_cropped.plot(events = events, event_id = event_id, title = 'Unfiltered') 

#Plotting filtered data | Also added a title for the plot as Filtered
raw_eeg_cropped_filtered.plot(events = events, event_id = event_id, title = 'Filtered')



#Plotting Unfiltered data and Filtered data in same figure as subplots 
fig, ax = plt.subplots(2)

raw_eeg_cropped.plot_psd(ax = ax[0], show=False)
raw_eeg_cropped_filtered.plot_psd(ax = ax[1], show=False) 

ax[0].set_title('PSD before filtering')
ax[1].set_title('PSD after filtering')
ax[1].set_xlabel('Frequency (Hz)')
fig.set_tight_layout(True)
plt.show()

#%% Save the Data 

#Choose the file on the dropbox of spyder on top left corner and create a folder named 'out_data' to save the file to the location
raw_eeg_cropped_filtered.save(pathlib.Path('out_data') / 'eeg_cropped_filt_raw.fif',
                              overwrite = True)

