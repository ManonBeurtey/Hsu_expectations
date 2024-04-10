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
for low_target_tone in low_target_range: #NON
    return low_target_tone #NON
    

# Stimuli
high_cue = expyriment.stimuli.Tone(cue_duration, frequency = high_cue_frequency)
high_cue.preload()

low_cue = expyriment.stimuli.Tone(cue_duration, frequency = low_cue_frequency)
low_cue.preload()

high_target_tone = expyriment.stimuli.Tone(target_duration, frequency = high_target_tone)
high_target_tone.preload()

low_target_tone = expyriment.stimuli.Tone(target_duration, frequency = low_target_tone) #NON
low_target_tone.preload() #NON

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
exp.add_block(Tblock) # add the block to the experiment

