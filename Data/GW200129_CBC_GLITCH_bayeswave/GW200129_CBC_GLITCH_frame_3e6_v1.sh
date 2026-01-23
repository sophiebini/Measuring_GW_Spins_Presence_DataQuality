# Job create_data.00000
/home/sophie.bini/BW/BW_CPP/bayeswave-cpp/build/src/create_data --ifo H1 --ifo L1 --H1-cache /home/sophie.bini/BW/BW_CPP/glitch_residual/Marginalization_Comparison/Frames/H1_GW20129_GLITCH-INJECTION-FAKE-STRAIN-original_1264316114.cache --L1-cache /home/sophie.bini/BW/BW_CPP/glitch_residual/Marginalization_Comparison/Frames/L1_GW20129_GLITCH-INJECTION-FAKE-STRAIN-unsubracted_1264316114.cache --H1-channel H1:GLITCH-INJECTION-FAKE-STRAIN --L1-channel L1:GLITCH-INJECTION-FAKE-STRAIN --H1-psd /home/rhiannon.udall/CaltechUBCGlitchProject/GW200129_Like_Wavelet_Phase_Scans/gw200129_H1_psd.dat --L1-psd /home/rhiannon.udall/CaltechUBCGlitchProject/GW200129_Like_Wavelet_Phase_Scans/gw200129_L1_psd.dat --dont-dump-extras  --psdlength 4.0 --padding 0.4 --H1-flow 20.0 --L1-flow 20.0 --trigtime 1264316116 --segment-start 1264316114 --srate 1024.0 --seglen 4.0 --dataseed 100 --L1-timeslide 0.0 --overwrite  --data-directory cached_data_0

# Job bayeswave.00000
/home/sophie.bini/BW/BW_CPP/bayeswave-cpp/build/src/main --glitch  --glitch-center-gps 1264316115.96 --glitch-window 1 --waveletDmax 10 --gw-cbc  --gw-cbc-fref 20 --gw-cbc-start-frequency 0 --gw-cbc-approximant NRSur7dq4 --gw-cbc-center-gps 1264316116 --gw-cbc-window 0.2 --m1min 20 --m1max 100 --m2min 20 --m2max 100 --extrinsicNcycle 100 --Niter 3000000 --Nchain 20 --Nthread 20 --chainseed 33 --checkpoint  --data-directory cached_data_0 --outputDir bayeswave_output_0

# Job bayeswave_post.00000
/home/sophie.bini/.conda/envs/bayeswave-cpp/bin/bayeswave_post.py --recompute  --burn_in 100 --run_directory bayeswave_output_0

