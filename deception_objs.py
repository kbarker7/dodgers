#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:17:50 2020

@author: kevinbarker
"""

class SummaryObject:
    def __init__(self, name):
        self.name = name
    
    total_num_of_abs = 0
    total_num_of_pitches = 0
    avg_pitch_count = 0
    total_b = 0
    total_s = 0
    total_x = 0
    ball_rate = 0
    strike_rate = 0
    in_play_rate = 0
    called_strikes = 0
    called_str_rate = 0
    swing_strikes = 0
    swing_str_rate = 0
    fouled_strikes = 0
    foul_str_rate = 0
    percent_swings = 0
    k_total = 0
    k_looking = 0
    k_swinging = 0
    bb_total = 0
    hbp_total = 0
    hits = 0
    outs = 0
    bat_avg = 0
    woba_avg = 0
    krate = 0
    brate = 0
    kbbrate = 0
    all_other = 0
    other_array = []

a='_first_pitch_'
b = a.replace('_', ' ').strip()
print(b)

class ComparisonObject:
    def __init__(self, p_handedness, b_handedness, pattern, unique_name, expected_name):
        self.p_h = p_handedness
        self.b_h = b_handedness.replace('_', '').upper()
        self.pattern = pattern.replace('_', ' ').strip()
        self.unique_name = unique_name
        self.expected_name = expected_name
        
    def add_base_data(self, u_abs, e_abs, u_pitches, e_pitches):
        self.u_abs = u_abs
        self.e_abs = e_abs
        self.u_pitches = u_pitches
        self.e_pitches = e_pitches
    
    def add_k_rate(self, u_k_rate, e_k_rate):
        self.u_k_rate = u_k_rate
        self.e_k_rate = e_k_rate
        self.d_k_rate = (u_k_rate - e_k_rate) * 100

    def add_bb_rate(self, u_bb_rate, e_bb_rate):
        self.u_bb_rate = u_bb_rate
        self.e_bb_rate = e_bb_rate
        self.d_bb_rate = (u_bb_rate - e_bb_rate) * 100
        
    def add_strike_rate(self, u_strike_rate, e_strike_rate):
        self.u_strike_rate = u_strike_rate
        self.e_strike_rate = e_strike_rate
        self.d_strike_rate = (u_strike_rate - e_strike_rate) * 100
        
    def add_called_str_rate(self, u_called_str_rate, e_called_str_rate):
        self.u_called_str_rate = u_called_str_rate
        self.e_called_str_rate = e_called_str_rate
        self.d_called_str_rate = (u_called_str_rate - e_called_str_rate) * 100
        
    def add_swing_str_rate(self, u_swing_str_rate, e_swing_str_rate):
        self.u_swing_str_rate = u_swing_str_rate
        self.e_swing_str_rate = e_swing_str_rate
        self.d_swing_str_rate = (u_swing_str_rate - e_swing_str_rate) * 100
        
    def add_percent_swings_rate(self, u_percent_swings, e_percent_swings):
        self.u_percent_swings = u_percent_swings
        self.e_percent_swings = e_percent_swings
        self.d_percent_swings = (u_percent_swings - e_percent_swings) * 100
        
    def add_in_play_rate(self, u_in_play_rate, e_in_play_rate):
        self.u_in_play_rate = u_in_play_rate
        self.e_in_play_rate = e_in_play_rate
        self.d_in_play_rate = (u_in_play_rate - e_in_play_rate) * 100
        
    def add_bat_avg_rate(self, u_bat_avg, e_bat_avg):
        self.u_bat_avg = u_bat_avg
        self.e_bat_avg = e_bat_avg
        self.d_bat_avg = u_bat_avg - e_bat_avg
        
    def add_woba_avg_rate(self, u_woba_avg, e_woba_avg):
        self.u_woba_avg = u_woba_avg
        self.e_woba_avg = e_woba_avg
        self.d_woba_avg = u_woba_avg - e_woba_avg
        
    def add_avg_pitch_count_rate(self, u_avg_pitch_count, e_avg_pitch_count):
        self.u_avg_pitch_count = u_avg_pitch_count
        self.e_avg_pitch_count = e_avg_pitch_count
        self.d_avg_pitch_count = u_avg_pitch_count - e_avg_pitch_count
    