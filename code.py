import expyriment
import random
import numpy

# BLOCKS
spectral_expectation = ["fixed_spectral", "variable_spectral"]
spectral_expectation_blocks = ["fixed_spectral", "variable_spectral"]*6
random.shuffle(spectral_expectation_blocks) # 12 blocks counterbalanced

# TRIALS
temporal_expectation = ["fixed_SOA","variable_SOA"]
temporal_expectation_trials = ["fixed_SOA","variable_SOA"]*50

# logarithmic steps for low expectations conditions (SOA and target)
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

# Instructions
instructions = expyriment.stimuli.TextScreen("Instructions",
                                             "You will hear a successions of pairs of tones; Press the 'J' key as quickly as possible upon hearing the second tone. Press the SPACEBAR to start")

kb = expyriment.io.Keyboard()

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

# Experiment

def run_trial(cue_freq, SOA, target_freq): # à changer avec expyriment
    cue_sound = expyriment.stimuli.Tone(cue_duration, frequency = cue_freq)
    cue_sound.preload()
    target_sound = expyriment.stimuli.Tone(target_duration, frequency = target_freq)
    target_sound.preload()

    expyriment.control.start()
    cue_sound.present()
    exp.clock.wait(SOA)
    target_sound.present()
    start_time = exp.clock.time
    key, rt = kb.wait()
    return key, rt, start_time 
    


# Initialisation

exp = expyriment.design.Experiment(name="Hsu task") 
expyriment.control.set_develop_mode(on=True)
expyriment.control.initialize(exp)

exp.data_variable_names = ["Cue","SOA","target","key","response time"]

instructions.present()
   
for i, block in enumerate(spectral_expectation_blocks):
    spectral_expectation_value = block 
    random.shuffle(temporal_expectation_trials)
    for j, trial in enumerate(temporal_expectation_trials):
        temporal_expectation_value = trial
        cue_freq, SOA, target_freq  = get_trial_parameters(spectral_expectation_value, temporal_expectation_value)
        key, response_time = run_trial(cue_freq, SOA, target_freq)
        exp.data.add([cue_freq, SOA, target_freq, key, response_time])


expyriment.control.end()


