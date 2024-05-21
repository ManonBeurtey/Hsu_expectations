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

instructions_end = expyriment.stimuli.TextScreen("It's finished", 
                                             " Thank you for your time ",text_font= "Monospace")

exp.data_variable_names = ["Cue","SOA","Target","Key","RT", "ITI"]

# Fixation crosses
cross = expyriment.stimuli.FixCross(size=(50, 50), line_width=4, colour=expyriment.misc.constants.C_WHITE) # Original cross
cross.preload()

cross_detection = expyriment.stimuli.FixCross(size=(50, 50), line_width=4, colour=expyriment.misc.constants.C_GREEN) # Detection cross
cross_detection.preload()

# Blocks & Trials
spectral_expectation_blocks = ["fixed_spectral", "variable_spectral"]*6
random.shuffle(spectral_expectation_blocks) # 12 blocks counterbalanced

temporal_expectation_trials = ["fixed_SOA","variable_SOA"]*60 # 120 trials 

# Logarithmic steps for low expectations conditions (SOA and target)
def log_steps(start_freq, end_freq, num_steps, avoid_values):
    log_steps = numpy.int_(numpy.logspace(numpy.log10(start_freq), numpy.log10(end_freq), num=num_steps))
    return [step for step in log_steps if not any(numpy.isclose(step, value, atol=50) for value in avoid_values)]

# Variables
N = 120 # number of trials
target_duration = 50 
cue_duration = 250

high_cue_freq = 1318 # Cues frequencies
low_cue_freq = 1046

fixed_SOA = 1250 # SOA duration
variable_SOA = log_steps(350, 2150, 10, [1250]) # 10 steps in total

fixed_target_freq = 1975 # Targets frequencies
variable_target_freq = log_steps(2225, 1725, 12, [1975]) # 10 steps in total

# Lists variable SOA and variable targets
variable_SOA_list = variable_SOA * 6
random.shuffle(variable_SOA_list)

variable_target_list = variable_target_freq * 6
random.shuffle(variable_target_list)

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
        cross_detection.present() 
        exp.clock.wait(100)  
        cross.present()

    ITI = int(numpy.random.normal(1375, 62.5))
    ITI = max(min(ITI, 1500), 1250)
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
if keys and expyriment.misc.constants.K_ESCAPE in keys:
    expyriment.control.end()
    print("Experiment terminated by the participant.")
    exit()

instructions_end.present()
expyriment.control.end()




