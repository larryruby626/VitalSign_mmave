import numpy as np

center_fz = 60 * 10 ** 9
wavelength = 3 * 10 ** 8 / center_fz
max_breath_amp = 12 * 10 ** -3  # ~1-12 mm
max_heart_amp = 0.5 * 10 ** -3  # ~0.1-0.5 mm

def distance2phasediff(distance):
    out_phase_diff = distance * (4 * np.pi) / wavelength
    return out_phase_diff

def phasediff2distance(phase_diff):
    distance = wavelength * phase_diff / (4 * np.pi)
    print("phase different : {} is  {} cm distance change".format(phase_diff, \
                get_round(distance * 10 ** 3)))
    return distance

def calc_max_phase_1frame(phase, frequency):
    framenum = 1 / frequency * 20  # 20 --> fps
    print(framenum,phase/framenum)

def get_round(data, num=2):
    out = np.round(data, num)
    return out


if __name__ == "__main__":
    calc_max_phase_1frame(distance2phasediff(max_breath_amp), 0.1)
    calc_max_phase_1frame(distance2phasediff(max_breath_amp), 0.5)
    phasediff2distance(3)
    phasediff2distance(2)
    phasediff2distance(0.05)

