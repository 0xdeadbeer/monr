#!/usr/bin/python3

import random
import math
from datetime import datetime, timedelta

def calculate_ef(easiness_factor, grade): 
    if (grade == 0): 
        easiness_factor -= 0.8
    else: 
        easiness_factor += 0.1
    
    if (easiness_factor < 1.3): 
        easiness_factor = 1.3
    
    return easiness_factor

def calculate_repetitions(grade, repetitions):
    if (grade == 0):
        return 0
    return repetitions + 1

def calculate_interval(interval, repetitions, easiness_factor):
    now = datetime.now() 
    output_interval = 0  
    
    if (repetitions == 0): 
        output_interval = 1
    elif (repetitions == 1):
        output_interval = 10
    elif (repetitions == 2):
        output_interval = 15
    else: 
        output_interval = round(interval * easiness_factor)
    
    return {
        "interval_date": now + timedelta(minutes=output_interval),
        "interval_number": output_interval
    } 

def calculate_schedule(interval, repetitions, easiness_factor, grade):
    easiness_factor = calculate_ef(easiness_factor, grade)
    repetitions = calculate_repetitions(grade, repetitions)
    interval = calculate_interval(interval, repetitions, easiness_factor)
    return {
        "easiness_factor": easiness_factor,
        "repetitions": repetitions,
        "interval_date": interval["interval_date"],
        "interval_number": interval["interval_number"],
    }