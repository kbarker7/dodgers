#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 23:16:51 2020

@author: kevinbarker

    with open(csv_title, 'a') as data_file:
        csv_list = []
"""

import csv
import pandas as pd

def write_headers_to_file(csv_title):
    with open(csv_title, 'a') as data_file:
        csv_writer = csv.writer(data_file)
        header_list = ['Pitcher', 'Throws', 'Unique AB Name', 'Expected AB Name', 'K% Diff', 'BB% Diff', 'Strike %', 
                       'Called Strike %', 'Swinging Strike %', 'Swing %', 'In Play %',
                       'BA', 'wOBA', 'Avg. No. Pitches', 'No. Unique AB', 'No. Expected AB',
                       'Unique AB Pitches', 'Expected AB Pitches']
        csv_writer.writerow(header_list)


def generate_csv_for_comparison_data(csv_title, pitcher, pitcher_handedness, comp_list):
    with open(csv_title, 'a') as data_file:
        csv_writer = csv.writer(data_file)

        csv_list = []
        for c in comp_list:
            temp_list = []
            temp_list.append(pitcher)
            temp_list.append(pitcher_handedness)            
            temp_list.append(c.unique_name)
            temp_list.append(c.expected_name)
            temp_list.append(c.d_k_rate)
            temp_list.append(c.d_bb_rate)
            temp_list.append(c.d_strike_rate)
            temp_list.append(c.d_called_str_rate)
            temp_list.append(c.d_swing_str_rate)
            temp_list.append(c.d_percent_swings)
            temp_list.append(c.d_in_play_rate)
            temp_list.append(c.d_bat_avg)
            temp_list.append(c.d_woba_avg)
            temp_list.append(c.d_avg_pitch_count)
            temp_list.append(c.u_abs)
            temp_list.append(c.e_abs)
            temp_list.append(c.u_pitches)
            temp_list.append(c.e_pitches)
            csv_list.append(temp_list)
        
        csv_writer.writerows(csv_list)
        
def create_data_frame_of_comps(pitcher, comp_list):
    df_list = []
    for c in comp_list:
        s_h = 0
        if (c.p_h == c.b_h):
            s_h = (1)
        temp_list = []
        #temp_list.append(pitcher)
        #temp_list.append(c.p_h)
        #temp_list.append(c.b_h)
        temp_list.append(s_h)
        temp_list.append(c.pattern)
        #temp_list.append(c.pattern + ': ' + str(s_h))         
        #temp_list.append(c.unique_name)
        #temp_list.append(c.expected_name)
        temp_list.append(c.d_k_rate)
        temp_list.append(c.d_bb_rate)
        temp_list.append(c.d_strike_rate)
        temp_list.append(c.d_called_str_rate)
        temp_list.append(c.d_swing_str_rate)
        temp_list.append(c.d_percent_swings)
        temp_list.append(c.d_in_play_rate)
        temp_list.append(c.d_bat_avg)
        temp_list.append(c.d_woba_avg)
        temp_list.append(c.d_avg_pitch_count)
        temp_list.append(c.u_abs)
        temp_list.append(c.e_abs)
        temp_list.append(c.u_pitches)
        temp_list.append(c.e_pitches)
        df_list.append(temp_list)
        
    cols = [ 'same_handedness', 'pattern', #'pitcher', 'p_throws', 'b_stands', 'key_flag', 'unexpected', 'expected', 
            'k_rate', 'bb_rate', 'str_rate', 'called_str_rate', 
            'swing_str_rate', 'swing_rate', 'inplay_rate', 'ba_avg', 'woba_avg', 
            'avg_pitch_count', 'u_abs', 'e_abs', 'u_pitches', 'e_pitches']
    
    return pd.DataFrame(df_list, columns=cols)
    

def generate_csv_for_summary_data(csv_title, summary_dictionary):
    with open(csv_title, 'a') as data_file:
        csv_list = []
        for k, s in summary_dictionary.items():
            summ_list = []
            if s.name.startswith('l'):
                summ_list.append('l')
            else:
                summ_list.append('r')
            summ_list.append(s.name)
            summ_list.append(s.total_num_of_abs)
            summ_list.append(s.total_num_of_pitches)
            summ_list.append(s.avg_pitch_count)
            summ_list.append(s.total_b)
            summ_list.append(s.total_s)
            summ_list.append(s.total_x)
            summ_list.append(s.ball_rate)
            summ_list.append(s.strike_rate)
            summ_list.append(s.in_play_rate)
            summ_list.append(s.called_strikes)
            summ_list.append(s.called_str_rate)
            summ_list.append(s.swing_strikes)
            summ_list.append(s.swing_str_rate)
            summ_list.append(s.fouled_strikes)
            summ_list.append(s.foul_str_rate)
            summ_list.append(s.percent_swings)
            summ_list.append(s.k_total)
            summ_list.append(s.k_looking)
            summ_list.append(s.k_swinging)
            summ_list.append(s.bb_total)
            summ_list.append(s.hbp_total)
            summ_list.append(s.hits)
            summ_list.append(s.outs)
            summ_list.append(s.bat_avg)
            summ_list.append(s.woba_avg)
            summ_list.append(s.krate)
            summ_list.append(s.brate)
            summ_list.append(s.kbbrate)
            summ_list.append(s.all_other)
            csv_list.append(summ_list)
            
        header_list = ['stand', 'name', 'abs', 'pitches', 'avg pitch #', 'balls', 'strikes', 
                   'in play', 'ball %', 'strike %', 'in play %', 'called strikes',
                   'called %', 'swing strikes', 'swing str %', 'fouled strikes', 'foul %', 
                   'all swing %', 'total k', 'k looking', 'k swinging', 'total bbs', 'total hbp', 
                   'hits', 'outs', 'bat avg', 'woba avg', 'k%', 'bb%', 'k-bb%', 'other count']
            
        csv_writer = csv.writer(data_file)
        csv_writer.writerow(header_list)
        csv_writer.writerows(csv_list)