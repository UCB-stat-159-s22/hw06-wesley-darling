import matplotlib
matplotlib.use('Agg')
from ligotools import utils
from ligotools import readligo as rl
import pytest
from scipy.interpolate import interp1d
import matplotlib.mlab as mlab
import json
import os
import numpy as np
import matplotlib.pyplot as plt


data_path = 'data/'
fnjson = "BBH_events_v3.json"
events = json.load(open(data_path+fnjson,"r"))
eventname = 'GW150914' 
event = events[eventname]
fn_H1 = event['fn_H1']   
fs = event['fs'] 

	
def test_whiten():
	assert len(utils.whiten(strain_H1,psd_H1,dt)) == 131072

def test_write_wavfile():
	cwd = os.getcwd()
	utils.write_wavfile("audio/_H1_whitenbp_TEMPORARY.wav",int(fs), utils.whiten(strain_H1,psd_H1,dt))
	assert any(File.endswith(".wav") for File in os.listdir("audio/")) == True
	os.remove("audio/_H1_whitenbp_TEMPORARY.wav")

def test_reqshift():
	assert len(utils.reqshift(strain_H1,fshift=400.,sample_rate=fs)) == 131072

	
	
NFFT = 4*fs
strain_H1, time_H1, chan_dict_H1 = rl.loaddata(data_path+fn_H1, 'H1')
time = time_H1
dt = time[1] - time[0]
data = strain_H1.copy()
Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = NFFT)
psd_H1 = interp1d(freqs, Pxx_H1)
data_psd, freqs = mlab.psd(data, Fs = fs, NFFT = NFFT)
data_fft = np.fft.fft(data) / fs
datafreq=np.fft.fftfreq(utils.whiten(strain_H1,psd_H1,dt).size)*fs
power_vec = np.interp(np.abs(datafreq), freqs, data_psd)
template_fft=utils.whiten(strain_H1,psd_H1,dt)
f = freqs
df = f[2]-f[1]
optimal = data_fft * template_fft.conjugate() / power_vec
optimal_time = 2*np.fft.ifft(optimal)*fs
sigmasq = 1*(template_fft * template_fft.conjugate() / power_vec).sum() * df
sigma = np.sqrt(np.abs(sigmasq))
SNR_complex = optimal_time/sigma
peaksample = int(data.size / 2)  # location of peak in the template
SNR_complex = np.roll(SNR_complex,peaksample)
SNR = abs(SNR_complex)
indmax = np.argmax(SNR)
timemax = time[indmax]
SNRmax = SNR[indmax]
tevent = event['tevent']

	
def test_plotter():
	utils.plotter(time=time, timemax=timemax, SNR=SNR, pcolor='g', det='L1', figures_path='figures/', eventname=eventname, plottype='pdf', tevent=tevent, strain_whitenbp=utils.whiten(strain_H1,psd_H1,dt), template_match=utils.whiten(strain_H1,psd_H1,dt), template_fft=utils.whiten(strain_H1,psd_H1,dt), datafreq=np.fft.fftfreq(utils.whiten(strain_H1,psd_H1,dt).size)*fs, d_eff=8, freqs=8, data_psd=8, fs=fs)
	assert sum([File.endswith(".pdf") for File in os.listdir("figures/")]) == 3
	test = os.listdir('figures/')
	for item in test:
		if item.endswith(".pdf"):
			os.remove(os.path.join('figures/', item))

