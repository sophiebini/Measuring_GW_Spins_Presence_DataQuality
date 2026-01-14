#script to generate glitch injections in L1. Glitch parameters (time, frequency, amplitude, quality factor and phase )  draw from prior. Amplitude is rescaled to the desired SNR.

from bayeswavecpp_bindings.autoload_cppyy import Cpp
from bayeswavecpp_bindings import bilby_helpers
from bayeswavecpp_bindings import utils
from bayeswavecpp_bindings import waveform_utils
import matplotlib.pyplot as plt
import numpy as np
from gwpy.timeseries import TimeSeries
from bayeswavecpp_bindings.model_collection_posterior import ModelCollectionPosterior
from bayeswavecpp_bindings.model_collection_and_data_wrapper import ModelCollectionAndDataWrapper
from bayeswavecpp_bindings.bayeswave_post_utils import SNRManager
import matplotlib as mpl
mpl.use('Agg')
import copy 
import json


def make_injection(initial_injection, model_and_data_wrapper, desired_glitch_SNR=25, desired_frequency=None):
    #From Sophie Hourihane
    #scale amplitude to desired SNR, change frequency
    model_and_data_wrapper.setModelCollectionState(initial_injection)
    new_injection = copy.deepcopy(initial_injection)
    if desired_frequency is not None:
        for ifo, dict_list in new_injection['glitch'].items():
            for glitch_dict in dict_list:
                glitch_dict['frequencyHz'] = desired_frequency


    snr_dict = model_and_data_wrapper.compute_snr_dict_of_model(['gravitationalWave', 'glitch'])

    # scale distance for glitch to make SNR desired SNR
    amplitude_scale = desired_glitch_SNR / snr_dict['glitch']['network']
    for ifo, dict_list in new_injection['glitch'].items():
        for glitch_dict in dict_list:
            glitch_dict['amplitude'] *= amplitude_scale
            glitch_dict['timeSec'] += 1.5  #add 2 seconds to the time of each wavelet to center them in the 4s window


    model_and_data_wrapper.setModelCollectionState(new_injection)
    snr_dict = model_and_data_wrapper.compute_snr_dict_of_model(['gravitationalWave', 'glitch'])

    return new_injection 

#define data where to inject the glitch
RUN_DIR = "/home/sophie.bini/BW/BW_CPP/glitch_residual"
run_path = RUN_DIR + "/O3_glitch_prior_Dfixed3"  #pre-existing BayesWave folder to import the priors. In this example, number of wavelets = 3
result_glitch = ModelCollectionPosterior(run_path + '/bayeswave_output_1/', burnIn=100)

#define glitch model
command_line = f"bw_cpp  --gw-cbc --glitch  --Niter 1000000 --Nchain 20 --Nthread 20 --checkpoint --data-directory {run_path}/cached_data_0 --outputDir {run_path}/bayeswave_output_1"
data_command_line=f"""data_command
--ifo L1
--L1-cache interp:/home/sophie.bini/BW/BW_CPP/glitch_residual/GW191109_ASD_LLO_LVK.dat
--L1-psd /home/rhiannon.udall/BayesianScattering2.0/GW191109/LVK_LLO_PSD.dat
--dont-dump-extras  --psdlength 4.0 --padding 0.4 --L1-flow 16.0 --trigtime 1257293145.2 --segment-start 1257293143 --srate 2048.0 --seglen 4.0 --L1-timeslide 0.0 --overwrite --data-directory test_data --dataseed 100"""

command_line_input = Cpp.CommandLine.Input(len(data_command_line.split()), data_command_line.split())
dataBuilder = Cpp.LalDataBuilder(command_line_input)

cbc_glitch_model = ModelCollectionAndDataWrapper(commandLineArgs=command_line, dataBuilder=dataBuilder)

injections_increasing_SNR = []

for i in range(0,50):
    print('Iteration: ', i)
    random_number_seed = i
    priorStateInjector = Cpp.PriorDrawStateInjector(random_number_seed)
    priorStateInjector.injectState(result_glitch.modelCollection)
    glitch_json = Cpp.buildJsonString(result_glitch.modelCollection).decode('ascii')   #save results as string
    glitch_dict = json.loads(glitch_json)  #save glitch injection as dictionary

    for glitch_SNR in [5, 10, 20, 30, 40, 50]: 
        injection_SNR = make_injection( glitch_dict, cbc_glitch_model, desired_glitch_SNR=glitch_SNR)
        
        print(f'glitch_SNR {glitch_SNR:.2f}')
        injections_increasing_SNR.append(copy.deepcopy(injection_SNR))

#save wavelet parameters to txt file
with open('injection_files/glitch_injections.txt', 'w') as f:
    for dictionary in injections_increasing_SNR:
        json.dump(dictionary, f)
        f.write('\n')


