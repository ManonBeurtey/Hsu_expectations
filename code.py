import expyriment
import random
import numpy
import sleep

temporal_expectation = ["fixed_SOA","variable_SOA"]
spectral_expectation = ["fixed_spectral", "variable_spectral"]
temporal_expectation_trials = ["fixed_SOA","variable_SOA"]*50
random.shuffle(temporal_expectation_trials) # trials are counterbalanced

spectral_expectation_blocks = ["fixed_spectral", "variable_spectral"]*6
random.shuffle(spectral_expectation_blocks) # bloks are counterbalanced

# logarithmic steps for stimuli 
def steps(start_range1, stop_range1, start_range2, stop_range2, number):
    start1 = numpy.log10(start_range1)
    end1 = numpy.log10(stop_range1)
    start2 = numpy.log10(start_range2)
    end2 = numpy.log10(stop_range2)
    ranged_int_list = list(numpy.int_(numpy.concatenate((numpy.logspace(start1, end1, num=number), numpy.logspace(start2, end2, num=number)))))
    return ranged_int_list

# Variables
N = 100 # number of trials
target_duration = 50 
cue_duration = 150

high_cue_freq = 1318 # Cues frequencies
low_cue_freq = 1046

fixed_SOA = 1250 # SOA duration
variable_SOA = steps(350, 950, 1550, 2150, 3)

fixed_target_freq = 1975 # Targets frequencies
variable_target_freq = steps(1725, 1925, 2025, 2225, 5)

# Lists variable SOA and variable targets
variable_target_list = variable_target_freq * (N//2)
random.shuffle(variable_target_list)
variable_SOA_list = variable_SOA * (N//2)
random.shuffle(variable_SOA_list)

# Trials parameters

def get_trial_parameters(spectral, temporal):
    if temporal == "fixed_SOA":
        cue_freq = high_cue_freq
        SOA = fixed_SOA
    else:  # variable_SOA
        cue_freq = low_cue_freq
        for var in variable_SOA_list:
            SOA = var
    if spectral == "fixed_spectral":
        target_freq = fixed_target_freq
    else: # variable spectral
        for tar in variable_target_list:
            target_freq = tar
    return cue_freq, SOA, target_freq

# Run experiment

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

# Initialisation
exp = expyriment.design.Experiment(name="Hsu task") 
expyriment.control.set_develop_mode(on=True)
expyriment.control.initialize(exp)

# Cue stimuli
high_cue = expyriment.stimuli.Tone(cue_duration, frequency = high_cue_f)
high_cue.preload()
low_cue = expyriment.stimuli.Tone(cue_duration, frequency = low_cue_f)
low_cue.preload()



block1 = expyriment.design.Block(name="block1") 
block2 = expyriment.design.Block(name="block2") 

high_cue = expyriment.stimuli.Tone(cue_duration, frequency = high_cue_f)
high_cue.preload()

low_cue = expyriment.stimuli.Tone(cue_duration, frequency = low_cue_f)
low_cue.preload()

high_target_tone = expyriment.stimuli.Tone(target_duration, frequency = high_target_f)
high_target_tone.preload()

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