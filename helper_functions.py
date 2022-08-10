# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 15:33:20 2022

@author: Richard
"""

from copy import copy

import numpy as np


def prepare_events(events):
    """Standardize event functions and extract is_terminal and direction."""
    prepared_events = []
    
    if events is None:
        events = ()
    elif callable(events):
        events = (events,)
    
    for event in events:
        prepared_event = copy(event)
        try:
            prepared_event.is_terminal = event.terminal
        except AttributeError:
            prepared_event.is_terminal = False
        
        prepared_events.append(prepared_event)
    return prepared_events


def evaluate_events(ti, yi, events):
    "Evaluates all given events and returns True if termination conditions were met, False otherwise"
    events = prepare_events(events)
    terminations = np.array(
        [
            (np.isclose(event(ti, yi), 0) and event.is_terminal)
            for event in events
        ], dtype=bool
    )
    
    return np.any(terminations)