"""Deliberately redundant control: (X, X, NOT X), period three.

This lies outside the P,D,M grammar. It tests whether the existing native-rule,
decoder, and nonconstant-field criteria alone exclude a trivial tower.
"""
import numpy as np

NAME = 'copy-copy-complement-control'

def choices(target_dimension, path):
    yield {'geometry': 'copy_complement', 'projection': 'X,X,notX'}

def field_names(choice):
    return ['X', 'X', 'notX']

def lift(state, derivative, choice):
    center = state[..., 1:-1]
    return np.stack((center, center, 1-center), axis=1)
