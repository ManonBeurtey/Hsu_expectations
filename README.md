# Hsu_expectations
Design:
Two cue tones of distinct frequencies (1318 Hz and 1046 Hz; 250 ms duration) signalled the probability of the time-interval between target and cue (“SOA”), creating the conditions of high and low temporal expectation. In the condition of high temporal expectation, the time interval (SOA) is always 1250ms, in the low temporal condition, the time interval was chosen in a range from 350 to 2150 ms, with logarithmic 10 steps between each, and avoiding the 1250 ms duration (and 50ms above and below). In the condition of high spectral expectation, the frequency of the target tone (50 ms) was always 1975 Hz so that participants can be certain of the identity of the upcoming target tone. In the condition of low spectral expectation, the frequency of the target tone was chosen in the range of 1725 to 2225 Hz, with 10 logarithmic steps,avoiding the 1975 frequency value (and 50 Hz above and below), so that participants cannot be certain of the identity of the upcoming target tone. It's a 2 by 2 within subject design, with a total of 120 trials of each temporal condition counterbalanced, within 12 blocks of spectral condition counterbalanced. The participant has to press a key (detection task) as soon as the target is perceived. Inter-trial interval was varying between 1250 and 1500 ms.
Note that when using the term "chosen" it means not randomly, but with the exact same frequency, but shuffled.

Code: 
* Importing packages
* Initialisation of the experiment: setting instructions and break_instructions (between blocks)
* Fixation cross: one original and one red for the exact moment when the participant presses the key
* Definition of the levels of the conditions within blocks and trials.
* Definition of the function that calculated the logarithmic steps
* Definition of the variables (cues frequencies, target frequencies, SOA, using the steps function)
* Making two shuffle list of variable_SOA and variable_target
* Making "get_trial_parameters" function linking blocks/trials with sitmuli
* Making "run_trial" function linking stimuli with tones loading and presenting, runnning experiment
* Running experiment making for loop in order to link everything together, setting breaks at the end of each block
* Escape the experiment
