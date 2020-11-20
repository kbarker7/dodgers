#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 23:17:04 2020

@author: kevinbarker
"""

import math
import deception_util as du
from deception_objs import SummaryObject, ComparisonObject

def generate_comparison_object(p_h, h, it, unexpected_dictionary, expected_dictionary):
    u_set_id = h + 'unique' + it
    e_set_id = h + 'expected' + it
    u_summ = generate_summary_data_for_at_bats(u_set_id, unexpected_dictionary.get(u_set_id))
    e_summ = generate_summary_data_for_at_bats(e_set_id, expected_dictionary.get(e_set_id))
    
    comp_obj = ComparisonObject(p_h , h, it, u_summ.name, e_summ.name)
    comp_obj.add_base_data(u_summ.total_num_of_abs, e_summ.total_num_of_abs, u_summ.total_num_of_pitches, e_summ.total_num_of_pitches)
    comp_obj.add_k_rate(u_summ.krate, e_summ.krate)
    comp_obj.add_bb_rate(u_summ.brate, e_summ.brate)
    comp_obj.add_strike_rate(u_summ.strike_rate, e_summ.strike_rate)
    
    comp_obj.add_called_str_rate(u_summ.called_str_rate, e_summ.called_str_rate)
    comp_obj.add_swing_str_rate(u_summ.swing_str_rate, e_summ.swing_str_rate)

    comp_obj.add_percent_swings_rate(u_summ.percent_swings, e_summ.percent_swings)
    comp_obj.add_in_play_rate(u_summ.in_play_rate, e_summ.in_play_rate)
    
    comp_obj.add_bat_avg_rate(u_summ.bat_avg, e_summ.bat_avg)
    comp_obj.add_woba_avg_rate(u_summ.woba_avg, e_summ.woba_avg)
    comp_obj.add_avg_pitch_count_rate(u_summ.avg_pitch_count, e_summ.avg_pitch_count)
    
    return comp_obj


def generate_summary_data_for_at_bats(name, unique_ab_list):
    s = SummaryObject(name)
    total_num_of_abs = 0
    hits = 0
    outs = 0
    all_other = 0
    total_num_of_pitches = 0
    total_s = 0
    total_b = 0
    total_x = 0
    called_strikes = 0
    swing_strikes = 0
    fouled_strikes = 0
    k_total = 0
    k_looking = 0
    k_swinging = 0
    bb_total = 0
    hbp_total = 0
    intent_ball = 0
    all_wobas = []
    contact_wo_woba = 0
    other_array = []
    non_ab_count = 0
    for i in unique_ab_list:
        total_num_of_abs += 1
        curr_ab = i[1]
        total_num_of_pitches += len(curr_ab.pitch_type.values)
        descriptions = curr_ab.description.values
        events = curr_ab.events.values
        descs = curr_ab.des.values
        outcome_types = curr_ab.type.values
        est_wobas = curr_ab.estimated_woba_using_speedangle.values
        for j in range(0, len(outcome_types)):
            if outcome_types[j] == 'S':
                total_s += 1
                if descriptions[j].startswith('called_'):
                    called_strikes += 1
                elif descriptions[j].startswith('swinging_'):
                    swing_strikes += 1
                else:
                    fouled_strikes += 1
                if not du.isnan(events[j]):
                    if events[j].startswith('strikeout'):
                        k_total += 1
                        if descriptions[j].startswith('called_'):
                            k_looking += 1
                        elif descriptions[j].startswith('swinging_') or descriptions[j].startswith('foul_') or descriptions[j].startswith('missed_'):
                            k_swinging += 1
                        else:
                            all_other += 1
                            other_array.append(curr_ab)
            elif outcome_types[j] == 'B':
                if descriptions[j] != 'intent_ball':
                    total_b += 1
                    if not du.isnan(events[j]):
                        non_ab_count += 1
                        if events[j] == 'walk':
                            bb_total += 1
                        elif events[j] == 'hit_by_pitch':
                            hbp_total += 1
                        else:
                            all_other += 1
                            other_array.append(curr_ab)
                else:
                    intent_ball += 1
            else:
                total_x += 1
                if events[j] == 'field_out' or events[j] == 'grounded_into_double_play' or events[j] == 'double_play' or events[j] == 'field_error' or events[j].startswith('fielders_choice') or events[j] == 'force_out':
                    outs += 1
                elif events[j] == 'sac_fly' or events[j].startswith('sac_bunt'):
                    outs += 1
                    non_ab_count += 1
                elif events[j] == 'single' or events[j] == 'double' or events[j] == 'triple' or events[j] == 'home_run':
                    hits += 1
                else:
                    all_other += 1
                    other_array.append(curr_ab)
                if math.isnan(est_wobas[j]):
                    contact_wo_woba += 1
                else:
                    all_wobas.append(est_wobas[j])
    s.total_num_of_abs = total_num_of_abs
    s.total_num_of_pitches = total_num_of_pitches
    s.avg_pitch_count = total_num_of_pitches/total_num_of_abs
    s.total_b = total_b
    s.total_s = total_s
    s.total_x = total_x
    s.ball_rate = total_b/total_num_of_pitches
    s.strike_rate = total_s/total_num_of_pitches
    s.in_play_rate = total_x/total_num_of_pitches
    s.called_strikes = called_strikes
    s.swing_strikes = swing_strikes
    s.fouled_strikes = fouled_strikes
    s.called_str_rate = called_strikes/total_num_of_pitches
    s.swing_str_rate = swing_strikes/total_num_of_pitches
    s.foul_str_rate = fouled_strikes/total_num_of_pitches
    s.percent_swings = (total_x + swing_strikes + fouled_strikes)/total_num_of_pitches
    s.k_total = k_total
    s.k_looking = k_looking
    s.k_swinging = k_swinging
    s.bb_total = bb_total
    s.hbp_total = hbp_total
    s.hits = hits
    s.outs = outs
    s.bat_avg = hits/(total_num_of_abs - non_ab_count)
    s.woba_avg = sum(all_wobas)/(total_x - contact_wo_woba)
    s.krate = k_total/total_num_of_abs
    s.brate = bb_total/total_num_of_abs
    s.kbbrate = s.krate - s.brate
    s.all_other = all_other
    s.other_array = other_array
    
    return s