"""Choose a first-floor reference, then reuse it across the newest axis.

Each initial mask/sign is an independent candidate tower. Every later floor
keeps that mask and sign and uses transverse offset +1 on the newest old axis.
There is no later mask, sign, axis, or orientation search.
"""
import numpy as np

NAME = 'fixed-transition-reference-newest-axis-plus'
MASKS = ('birth', 'death', 'stay_one', 'stay_zero')

def choices(target_dimension, path):
    if not path:
        for sign in (-1, 1):
            for mask in MASKS:
                yield {'shift': sign, 'offsets': [], 'mask': mask, 'geometry': 'straight'}
    else:
        yield {'shift': path[0]['shift'],
               'offsets': [1] + [0] * (target_dimension-3),
               'mask': path[0]['mask'], 'geometry': 'transverse_plus'}

def field_names(choice):
    return ['P', 'D', choice['mask']]

def lift(state, derivative, choice):
    center = state[..., 1:-1]
    shifted = state[..., :-2] if choice['shift'] == -1 else state[..., 2:]
    for axis, offset in enumerate(choice['offsets'], 1):
        if offset:
            shifted = np.roll(shifted, -offset, axis=axis)
    spatial = center ^ shifted
    kind = choice['mask']
    if kind == 'birth': reference = (1-center) & derivative
    elif kind == 'death': reference = center & derivative
    elif kind == 'stay_one': reference = center & (1-derivative)
    elif kind == 'stay_zero': reference = (1-center) & (1-derivative)
    else: raise ValueError(kind)
    return np.stack((spatial, derivative, reference), axis=1)
