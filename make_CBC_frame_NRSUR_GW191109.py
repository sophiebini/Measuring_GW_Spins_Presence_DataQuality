#script to produce .gwf frame containining CBC + glitch signal
import bilby
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries
import json

#frame with glitch model into Gaussian noise in Livingston
frame_L1 = '/home/rhiannon.udall/CaltechUBCGlitchProject/WaveletResidualAnalyses/FrameFiles/GW191109/phi_3.14-time_02/L1_unsubtracted_data.gwf' 
#read glitch frame file
data_L1 = TimeSeries.read(frame_L1, channel='L1:GLITCH-INJECTION-FAKE-STRAIN')

#same for LIGO Hanford
frame_H1 = '/home/rhiannon.udall/CaltechUBCGlitchProject/WaveletResidualAnalyses/FrameFiles/GW191109/H1_original_data.gwf'
data_H1 = TimeSeries.read(frame_H1, channel='H1:GLITCH-INJECTION-FAKE-STRAIN')

duration = 4
sampling_frequency = 1024

#CBC injections parameters for GW191109
with open("/home/rhiannon.udall/CaltechUBCGlitchProject/MarginalizationComparison/Heavy-Moderate/phi_3.14-time_02/gw191109_injection.json", "r") as f:
    params = json.load(f)
    injection_parameters = params["injections"]

# specify waveform arguments
waveform_arguments = dict(
    waveform_approximant="NRSur7dq4",  # waveform approximant name
    minimum_frequency= 20,
    maximum_frequency= 448.0,
    reference_frequency=20,
)

# set up the waveform generator
waveform_generator = bilby.gw.WaveformGenerator(

    sampling_frequency=sampling_frequency,
    duration=duration,
    frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
    parameters=injection_parameters,
    start_time = 1257296853,
    waveform_arguments=waveform_arguments,
)

#specify PSD
psd_L1 = bilby.gw.detector.psd.PowerSpectralDensity(psd_file='/home/rhiannon.udall/BayesianScattering2.0/GW191109/LVK_LLO_PSD.dat')
psd_H1 = bilby.gw.detector.psd.PowerSpectralDensity(psd_file='/home/rhiannon.udall/BayesianScattering2.0/GW191109/LVK_LHO_PSD.dat')

#inject CBC into glitch frame file
injection_L1 = bilby.gw.detector.inject_signal_into_gwpy_timeseries(data_L1, waveform_generator, injection_parameters, 'L1', power_spectral_density=psd_L1)
injection_H1 = bilby.gw.detector.inject_signal_into_gwpy_timeseries(data_H1, waveform_generator, injection_parameters, 'H1', power_spectral_density=psd_H1)

#save on .gwf file
injection_L1[0].write('L1_GW191109_GLITCH-INJECTION-FAKE-STRAIN-unsubracted_1257296853.gwf')
injection_H1[0].write('H1_GW191109_GLITCH-INJECTION-FAKE-STRAIN-original_1257296853.gwf')
