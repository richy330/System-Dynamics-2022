# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 15:33:20 2022

@author: Richard
"""

from copy import copy

import numpy as np


def prepare_events(events):
    """
    Standardize event functions and set boolean attributes 'terminal' and 'state_modifier' 
    to False if not set before.
    """
    prepared_events = []
    
    if events is None:
        events = ()
    elif callable(events):
        events = (events,)
    
    for event in events:
        try:
            event.terminal
        except AttributeError:
            event.terminal = False
        try:
            event.state_modifier
        except AttributeError:
            event.state_modifier = False
        
        prepared_events.append(event)
    return prepared_events



def evaluate_events(ti, yi, events):
    """
    Evaluates all given events and returns tuple(boolean, list). Boolean is indicating if termination 
    conditions were met, list contains all events that triggered modifications to the state vector
    """
    events = prepare_events(events)
    
    triggered_events = [event for event in events if np.isclose(event(ti, yi), 0)]
    
    termination_occured = np.any([event.terminal for event in triggered_events])
    state_change_events = [event for event in triggered_events if event.state_modifier]
    
    return termination_occured, state_change_events



def handle_events(ti, yi, events):
    """
    Takes a timevalue, state-vector and events (callable, iterable of callables or None, for details
    see documentation of ODE solvers) and returns tuple(boolean, state-vector). 
    Returned boolean is indicating if termination conditions were met, returned state-vector is 
    state-vector after state-modification occured.
    Note: State modifications are applied in order. If multiple state modifications trigger at once,
    results may be unexpected.
    """
    events = prepare_events(events)
    
    termination_occured, state_change_events = evaluate_events(ti, yi, events)
    for event in state_change_events:
        yi = event.modify_state(ti, yi)
    return termination_occured, yi