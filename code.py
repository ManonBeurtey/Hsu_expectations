import random
import sleep

temporal_expectation = ["fixed_SOA","variable_SOA"]
spectral_expectation = ["fixed_spectral", "variable_spectral"]
temporal_expectation_trials = ["fixed_SOA","variable_SOA"]*50
random.shuffle(temporal_expectation_trials) # trials are counterbalanced

spectral_expectation_blocks = ["fixed_spectral", "variable_spectral"]*6
random.shuffle(spectral_expectation_blocks) # bloks are counterbalanced
print(temporal_expectation_trials, spectral_expectation_blocks)


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
        

######## previous draft code ###########

import expyriment
import random
import numpy

# Initialisation
exp = expyriment.design.Experiment(name="Hsu task") 
expyriment.control.set_develop_mode(on=True)
expyriment.control.initialize(exp)

N = 100 # number of trials
target_duration = 50 # Target duration
cue_duration = 150 # Cue duration

# logarithmic steps for stimuli 
def log(a, b, c, d, step):
    start1 = numpy.log10(a)
    end1 = numpy.log10(b)
    start2 = numpy.log10(c)
    end2 = numpy.log10(d)
    result = numpy.concatenate((numpy.logspace(start1, end1, num=step), numpy.logspace(start2, end2, num=step)))
    return(result)

# Cue stimuli
high_cue_f = 1318
low_cue_f = 1046
high_cue = expyriment.stimuli.Tone(cue_duration, frequency = high_cue_f)
high_cue.preload()
low_cue = expyriment.stimuli.Tone(cue_duration, frequency = low_cue_f)
low_cue.preload()

# SOA
high_SOA = 1250 
low_SOA = log(350, 950, 1550, 2150, 3)

#Target tone - à refaire
high_target_f = [1975]
low_target_f = log(1725, 1925, 2025, 2225, 5)
low_targets = [low_target_f]* (N//2)
random.shuffle(low_targets)
high_targets = [high_target_f]* (N//2)
targets = high_targets+low_targets
random.shuffle(targets)

# Temporal block
Tblock = expyriment.design.Block(name="Temporal condition block") 

high_cue = expyriment.stimuli.Tone(cue_duration, frequency = high_cue_f)
high_cue.preload()

low_cue = expyriment.stimuli.Tone(cue_duration, frequency = low_cue_f)
low_cue.preload()

cues = [high_cue, low_cue] * N//2 
random.shuffle(cues)

# Spectral block
Sblock = expyriment.design.Block(name="Spectral condition block") 

high_target_tone = expyriment.stimuli.Tone(target_duration, frequency = high_target_f)
high_target_tone.preload()

for f in low_target_f:
    low_target_tone = expyriment.stimuli.Tone(target_duration, frequency = f) 
low_target_tone.preload()

#Experiment

#A refaire:
for temporal in cues:
    if temporal == high_cue:
        trial = expyriment.design.Trial()
        high_cue.present()
        exp.clock.wait(high_inter)
        high_target_tone.present()
        trial.add_stimulus(high_cue)
        trial.set_factor('cue', "high")
        Tblock.add_trial(trial)
    else:
        .....


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


kb = exp.keyboard  # response device
exp.add_data_variable_names(['tone', 'waiting_time', 'key', 'rt'])

## Run the experiment
expyriment.control.start()

instructions.present()
kb.wait()

fixcross.present(update=True, clear=True)

for b in exp.blocks:
    for t in b.trials:
        exp.clock.wait(ITI)
        tone = t.stimuli[0]
        waiting_time = 1000 + random.random() * 1000 
        exp.clock.wait(waiting_time)
        tone.present()
        key, rt = kb.wait(keys='j', duration=2000)
        exp.data.add([t.get_factor('tone'), waiting_time, key, rt])

expyriment.control.end()