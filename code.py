import expyriment
import random
import numpy

# Initialisation of the experiment

exp = expyriment.design.Experiment(name="Hsu task") 
expyriment.control.set_develop_mode(on=True)
expyriment.control.initialize(exp)
instructions = expyriment.stimuli.TextScreen("Instructions", 
                                             " You will hear pairs of tones. "
                                             "Press the SPACEBAR as quickly as possible upon hearing the second tone. " 
                                             "Press ENTER to start", text_font= "Monospace")
instructions_break = expyriment.stimuli.TextScreen("Break", 
                                             " You can take a break. Press ENTER to go back to the experiment ",text_font= "Monospace")

exp.data_variable_names = ["Cue","SOA","Target","Key","RT", "ITI"]

# Fixation crosses
cross = expyriment.stimuli.FixCross(size=(50, 50), line_width=4, colour=expyriment.misc.constants.C_WHITE) # Original cross
cross.preload()

cross_red = expyriment.stimuli.FixCross(size=(50, 50), line_width=4, colour=expyriment.misc.constants.C_RED) # Detection cross
cross_red.preload()

# Blocks & Trials
spectral_expectation_blocks = ["fixed_spectral", "variable_spectral"]*6
random.shuffle(spectral_expectation_blocks) # 12 blocks counterbalanced

temporal_expectation_trials = ["fixed_SOA","variable_SOA"]*60 # 120 trials 

# Logarithmic steps for low expectations conditions (SOA and target)
def steps(start_range1, stop_range1, start_range2, stop_range2, number1, number2):
    start1 = numpy.log10(start_range1)
    end1 = numpy.log10(stop_range1)
    start2 = numpy.log10(start_range2)
    end2 = numpy.log10(stop_range2)
    ranged_int_list = list(numpy.int_(numpy.concatenate((numpy.logspace(start1, end1, num=number1), numpy.logspace(start2, end2, num=number2)))))
    return ranged_int_list

# Variables
N = 120 # number of trials
target_duration = 50 
cue_duration = 250

high_cue_freq = 1318 # Cues frequencies
low_cue_freq = 1046

fixed_SOA = 1250 # SOA duration
variable_SOA = steps(350, 950, 1550, 2150, 3, 3) # 6 steps in total

fixed_target_freq = 1975 # Targets frequencies
variable_target_freq = steps(1725, 1925, 2025, 2225, 5, 5) # 10 steps in total

# Lists variable SOA and variable targets
variable_target_list = variable_target_freq * 6
random.shuffle(variable_target_list)

variable_SOA_list = variable_SOA * 10
random.shuffle(variable_SOA_list)

# Functions
def get_trial_parameters(spectral, temporal, trial_index):
    if temporal == "fixed_SOA":
        cue_freq = high_cue_freq
        SOA = fixed_SOA
    else:  # variable_SOA
        cue_freq = low_cue_freq
        SOA = variable_SOA_list[trial_index % len(variable_SOA_list)]
    if spectral == "fixed_spectral":
        target_freq = fixed_target_freq
    else: # variable spectral
        target_freq = variable_target_list[trial_index % len(variable_target_list)]
    return cue_freq, SOA, target_freq

def run_trial(cue_freq, SOA, target_freq):
    cross.present()
    cue_sound = expyriment.stimuli.Tone(cue_duration, frequency=cue_freq)
    cue_sound.preload()
    target_sound = expyriment.stimuli.Tone(target_duration, frequency=target_freq)
    target_sound.preload()
    cue_sound.present()
    exp.clock.wait(SOA)
    
    target_presentation_time = exp.clock.time
    target_sound.present()
    key, rt = exp.keyboard.wait(duration=2000)    
    if key and (exp.clock.time - target_presentation_time < 2000):
        cross_red.present() 
        exp.clock.wait(100)  
        cross.present()

    ITI = random.randint(1250, 1500) # Intertrial duration
    exp.clock.wait(ITI)
    cross.present()
    return key, rt, ITI

# Running experiment
expyriment.control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait()
cross.present()

for i, block in enumerate(spectral_expectation_blocks):
    spectral_expectation_value = block 
    random.shuffle(temporal_expectation_trials)
    for j, trial in enumerate(temporal_expectation_trials):
        temporal_expectation_value = trial
        cue_freq, SOA, target_freq  = get_trial_parameters(spectral_expectation_value, temporal_expectation_value, j)
        key, rt, ITI = run_trial(cue_freq, SOA, target_freq)
        print(i,j)
        exp.data.add([cue_freq, SOA, target_freq, key, rt, ITI])

        if j == (N-1):
            instructions_break.present()        
            exp.keyboard.wait(keys=[expyriment.misc.constants.K_RETURN])

# Escape
keys = exp.keyboard.check()
if expyriment.misc.constants.K_ESCAPE in keys:
    expyriment.control.end()
    print("Experiment terminated by the participant.")
    exit()

expyriment.control.end()




