import numpy as np
import matplotlib.pyplot as plt
from  larry_common_usage.DSP.band_pass_filter import band_pass

def Phase_filter_proecss(Phase_input):

    phase_RR = band_pass(0.1, 0.5, Phase_input, 20)
    phase_HB = band_pass(0.8, 2, Phase_input, 20)
    phase_both = band_pass(0.1, 4, Phase_input, 20)

    return  phase_RR , phase_HB ,phase_both