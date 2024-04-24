import random
import time

temporal_expectation = ["fixed_SOA","variable_SOA"]
spectral_expectation = ["fixed_spectral", "variable_spectral"]
temporal_expectation_trials = ["fixed_SOA","variable_SOA"]*50
spectral_expectation_blocks = ["fixed_spectral", "variable_spectral"]*6

def get_trial_parameters(spectral, temporal):
    if temporal == "fixed_SOA":
        cue_freq = 1318
        SOA = 1250
    else:  # variable_SOA
        cue_freq = 1046
        SOA = random.choice([20, 30])
    if spectral == "fixed_spectral":
        target_freq = 1975
    else: # variable spectral
        target_freq = random.choice([40, 50])
    return cue_freq, SOA, target_freq 


def run_trial(cue_freq, SOA, target_freq):
    cue_sound = "tonpur_{cue_freq}"
    target_sound = "tonpur_{target_freq}"
    print(cue_sound)
    time.sleep(SOA/1000.0) # programmation défensive
    print(target_sound)

for i, block in enumerate(spectral_expectation_blocks):
    spectral_expectation_value = block 
    random.shuffle(temporal_expectation_trials)
    for j, trial in enumerate(temporal_expectation_trials):
        temporal_expectation_value = trial
        cue_freq, SOA, target_freq  = get_trial_parameters(spectral_expectation_value, temporal_expectation_value)
        print(i, j)
        run_trial(cue_freq, SOA, target_freq)
        


#######################################################################################################

import expyriment
import random

## Initialisation
exp = expyriment.design.Experiment(name="Hsu task") 
expyriment.control.set_develop_mode(on=True)
expyriment.control.initialize(exp)

N = 100 # number of trials
Inter = 1250 # Inter-trial duration
target_duration = 50 # Target duration
cue_duration = 150 # Cue duration

# Cue tones (High and Low temporal expectations)
high_cue_frequency = 1318
low_cue_frequency = 1046

# Target tones (High and Low spectral expectations)
high_target_tone = 1975 
low_target_range = [1725, 1775, 1825, 1875, 1925, 2025, 2075, 2125, 2175, 2225]

# Stimuli
high_cue = expyriment.stimuli.Tone(cue_duration, frequency = high_cue_frequency)
high_cue.preload()

low_cue = expyriment.stimuli.Tone(cue_duration, frequency = low_cue_frequency)
low_cue.preload()

high_target_tone = expyriment.stimuli.Tone(target_duration, frequency = high_target_tone)
high_target_tone.preload()

for f in low_target_range:
    low_target_tone = expyriment.stimuli.Tone(target_duration, frequency = f) 
low_target_tone.preload()

# Creation of the blocks
Tblock = expyriment.design.Block(name="Temporal condition block") 
Sblock = expyriment.design.Block(name="Spectral condition block") 

for i in range (N//2): 
    trial = expyriment.design.Trial()
    trial.add_stimulus(high_cue)
    trial.set_factor('cue', "high")
    Tblock.add_trial(trial)

for i in range (N//2):    
    trial = expyriment.design.Trial()
    trial.add_stimulus(low_cue)
    trial.set_factor('cue', "low")
    Tblock.add_trial(trial)

Tblock.shuffle_trials()
Sblock.shuffle_trials()

exp.add_block(Tblock) # add the block to the experiment
exp.add_block(Sblock) # add the block to the experiment

