# Measuring_GW_Spins_Presence_DataQuality
Codes and notebooks to reproduce the analyses I did for the publication "Inferring the spins of merging black holes in the presence of data-quality issues" R. Udall, S. Bini et al (2025) Arxiv 2510.05029

The repository contains:
1. 'generate_glitch_injection_various_SNR.py' script to generate glitch simulations drawing the wavelets parameters from prior and scaling the SNR to desired values.
2. 'make_CBC_frame_NRSUR_GW191109.py' script to generate frame files with compact binary coalescence (CBC) and glitch. 
3. 'BayesWave_config_files': examples of BayesWave configurations file used to recover CBC and/or glitch signals using glitch only model or the joint CBC and glitch inference
4. 'plot_fig2.ipynb' notebook to reproduce figure 2 in the paper
5. 'visualize_waveform_posteriors.ipynb' notebook to visualize the CBC and glitch waveforms obtained, and the spins posterior distribution inferred. 
   
