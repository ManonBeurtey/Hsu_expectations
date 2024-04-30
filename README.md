# Hsu_expectations
Design:
Two cue tones of distinct frequencies (1318 Hz and 1046 Hz; 150 ms duration) signalled the probability of the time-interval between target and cue (“SOA”), creating the conditions of high and low temporal expectation. In the condition of high temporal expectation, the time interval (SOA) is always 1250ms, in the low temporal condition, the time interval was chosen in a range from 350 to 950 ms and 1550 to 2150 ms, with logarithmic 3 steps between each. In the condition of high spectral expectation, the frequency of the target tone was always 1975 Hz (50 ms duration) so that participants can be certain of the identity of the upcoming target tone. In the condition of low spectral expectation, the frequency of the target tone was chosen in the range of 1725–1925 Hz and 2025–2225 Hz, with 5 logarithmic steps between each (50 ms duration) so that participants cannot be certain of the identity of the upcoming target tone. It's a 2 by 2 within subject design, with a total of 100 trials of each temporal condition counterbalanced, target duration is 50 ms and cue duration is 150ms, within 12 blocks of spectral condition counterbalanced. The participant has to press a key (detection task) as soon as the target is perceived.
Note that when using the term "chosen" it means not randomly, but with the exact same frequency, but shuffled.

Code: 
* Definition of the levels of the conditions within blocks and trials.
* Definition of the function that calculated the logarithmic steps
* Definition of the variables (cues frequencies, target frequencies, SOA, using the steps function)
* Making two shuffle list of variable_SOA and variable_target
* Initialisation of expyriment
* Making function linking blocks/trials with sitmuli
* Making function linking stimuli with tones loading and presenting, runnning experiment
* Making for loop in order to link everything together
