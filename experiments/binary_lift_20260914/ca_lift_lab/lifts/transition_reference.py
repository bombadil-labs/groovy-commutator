"""Period-three transition-reference lift. Edit this module to try a recipe.

Arrays have axes (source word, newest old axis, ..., oldest old axis, x).
The parent state has two horizontal halo cells more than its derivative.
The source derivative is primitive; parent derivatives are its induced action
on prepared encodings, never a choice of off-image rule completion.
"""
import numpy as np

NAME = 'transition-reference'
MASKS = ('birth', 'death', 'stay_one', 'stay_zero')

def choices(target_dimension, path):
    signs = (-1, 1) if not path else (path[0]['shift'],)
    crosses = (0,) if not path else (0, -1, 1)
    for sign in signs:
        for cross in crosses:
            offsets = () if not path else (cross,) + (0,) * (target_dimension - 3)
            for mask in MASKS:
                yield {'shift': sign, 'offsets': list(offsets), 'mask': mask,
                       'geometry': 'straight' if cross == 0 else ('transverse_minus' if cross < 0 else 'transverse_plus')}

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
