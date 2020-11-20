#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 17:25:38 2020

@author: kevinbarker
"""

import pandas as pd
import csv
import numpy as np
import deception_util as du
import deception_methods as dm
import object_creation_methods as ocm
import printing_methods as pm
import statsmodels.api as sm



'''
All files located in: /data
data/
sch_ver: scherzer, verlander: 36059
les_bau: lester, bauer: 35129
col_gre: cole, greinke: 34725
por_deg: porcello, degrom: 33519
qui_ker: quintana, kershaw: 31970
arr_hen: arrieta, hendricks: 31650
teh_sal: teheran, sale: 31413
keu_gib: keuchal, gibson: 31047
roa_hap: roark, happ: 30564
fie_odo: fiers, odorizzi: 29908
arc_gon: archer, gonzalez: 29727
tan_cor: tanaka, corbin: 29627
bum_ham: bumgarner, hamels: 29527
ray_lyn: ray, lynn: 28924
gau_gra: gausman, gray: 28018

testing data/kershaw_actual
'''

du.get_current_time('start')

## Use this array if planning to run for multiple pitchers
pitcher_data_list = ['sch_ver', 'les_bau', 'col_gre', 'por_deg',
                    'qui_ker', 'arr_hen', 'teh_sal', 'keu_gib',
                    'roa_hap', 'fie_odo','arc_gon', 'tan_cor', 
                    'bum_ham', 'ray_lyn', 'gau_gra']
'''
## Use array with single variable if planning to run for single pitcher
pitcher_data_list = ['kershaw_actual']
'''
# These are the two products to examine
df_final_list = pd.DataFrame()
freeze_rates = {}

handedness = ['r_', 'l_']
#The three grouping patterns to organize at bats by
id_terms = ['_percent_of_ab', '_last_pitch_abs', '_first_pitch_abs']
results_file_name = 'complete_results.csv'

for pdl_id in pitcher_data_list:
    file_name = 'data/' + pdl_id + '.csv'
    mydataset = pd.read_csv(file_name)
    df_all = pd.DataFrame(mydataset)
    df_by_pitcher = df_all.groupby(['pitcher'])
    
    print('beginning scan of data from', file_name, 'row count:', len(df_all))
    
    for p in df_by_pitcher:
        pitcher = p[0]
        df = p[1]
        pitcher_name = df['player_name'].iloc[0]
        pitcher_handedness = df['p_throws'].iloc[0]
        print('reading data for', pitcher, pitcher_name)
        
        # Clean data. Drop null pitch/zone types. Remove all Intentional pitches
        # Remove all z > 5 and z < 0 and x > 2 and x < -2
        pre_cleaning_length = len(df)
        df = df.dropna(axis=0, subset=['pitch_type', 'zone'])
        df = df[df['pitch_type'] != 'IN']
        df = df[df['game_year'] >= 2015]
        df = df[df['plate_x'] >= -2]
        df = df[df['plate_x'] <= 2]
        df = df[df['plate_z'] >= 0]
        df = df[df['plate_z'] <= 4.5]
        post_cleaning_length = len(df)
        print(pre_cleaning_length - post_cleaning_length, 'records dropped during cleaning')

        ## Group data by handedness and count and create count
        df['ab_count'] = df.apply (lambda row: du.create_count(row), axis=1)
        df_r = df[df['stand'] == 'R']
        df_l = df[df['stand'] == 'L']
        r_by_count = df_r.groupby('ab_count').apply(lambda dfg: dfg.drop('ab_count', axis=1).to_dict(orient='list')).to_dict()
        l_by_count = df_l.groupby('ab_count').apply(lambda dfg: dfg.drop('ab_count', axis=1).to_dict(orient='list')).to_dict()
        d = {}
        d['r'] = dm.create_dictionary_for_handedness(r_by_count)
        d['l'] = dm.create_dictionary_for_handedness(l_by_count)
        
        #For more in depth look into raw data. Instead of dictionary with percentages, keep raw hard count instead
        #d_count = {}
        #d_count['r'] = dm.create_dictionary_for_handedness_with_hard_count(r_by_count)
        #d_count['l'] = dm.create_dictionary_for_handedness_with_hard_count(l_by_count)
        
        #Group by at bat to then sort into three patterns
        r_by_at_bat = df_r.groupby(['game_date', 'at_bat_number'])
        l_by_at_bat = df_l.groupby(['game_date', 'at_bat_number'])
        print('finished preparing data for', pitcher_name)
        
        unexpected_dictionary = {}
        expected_dictionary = {}
                
        l_first_pitch_grouping = dm.group_at_bats_via_first_pitch(l_by_at_bat, d.get('l'), 50)
        r_first_pitch_grouping = dm.group_at_bats_via_first_pitch(r_by_at_bat, d.get('r'), 50)
        print('first pitch group done for', pitcher_name)
        freeze_rates[pitcher_name + '_first_pitch_l'] = (l_first_pitch_grouping.get('u_called') - l_first_pitch_grouping.get('e_called')) * 100
        freeze_rates[pitcher_name + '_first_pitch_r'] = (r_first_pitch_grouping.get('u_called') - r_first_pitch_grouping.get('e_called')) * 100        

        l_last_pitch_grouping = dm.group_at_bats_via_last_pitch(l_by_at_bat, d.get('l'), 50)
        r_last_pitch_grouping = dm.group_at_bats_via_last_pitch(r_by_at_bat, d.get('r'), 50)
        print('last pitch group done for', pitcher_name)
        freeze_rates[pitcher_name + '_last_pitch_l'] = (l_last_pitch_grouping.get('u_called') - l_last_pitch_grouping.get('e_called')) * 100
        freeze_rates[pitcher_name + '_last_pitch_r'] = (r_last_pitch_grouping.get('u_called') - r_last_pitch_grouping.get('e_called')) * 100     

        l_majority_pitch_grouping = dm.group_at_bats_with_via_majority_of_pitches(l_by_at_bat, d.get('l'), 50, .5)
        r_majority_pitch_grouping = dm.group_at_bats_with_via_majority_of_pitches(r_by_at_bat, d.get('r'), 50, .5)
        print('majority of pitches group done for', pitcher_name)
        freeze_rates[pitcher_name + '_percent_of_ab_l'] = (l_majority_pitch_grouping.get('u_called') - l_majority_pitch_grouping.get('e_called')) * 100
        freeze_rates[pitcher_name + '_percent_of_ab_r'] = (r_majority_pitch_grouping.get('u_called') - r_majority_pitch_grouping.get('e_called')) * 100       

        unexpected_dictionary['r_unique_percent_of_ab'] = r_majority_pitch_grouping.get('u')
        unexpected_dictionary['r_unique_last_pitch_abs'] = r_last_pitch_grouping.get('u')
        unexpected_dictionary['r_unique_first_pitch_abs'] = r_first_pitch_grouping.get('u')
        
        unexpected_dictionary['l_unique_percent_of_ab'] = l_majority_pitch_grouping.get('u')
        unexpected_dictionary['l_unique_last_pitch_abs'] = l_last_pitch_grouping.get('u')
        unexpected_dictionary['l_unique_first_pitch_abs'] = l_first_pitch_grouping.get('u')
        
        expected_dictionary['r_expected_percent_of_ab'] = r_majority_pitch_grouping.get('e')
        expected_dictionary['r_expected_last_pitch_abs'] = r_last_pitch_grouping.get('e')
        expected_dictionary['r_expected_first_pitch_abs'] = r_first_pitch_grouping.get('e')
        
        expected_dictionary['l_expected_percent_of_ab'] = l_majority_pitch_grouping.get('e')
        expected_dictionary['l_expected_last_pitch_abs'] = l_last_pitch_grouping.get('e')
        expected_dictionary['l_expected_first_pitch_abs'] = l_first_pitch_grouping.get('e')
        
        comp_list = []
        for b_h in handedness:
            for pattern in id_terms:
                comp_list.append(ocm.generate_comparison_object(pitcher_handedness, b_h, pattern, unexpected_dictionary, expected_dictionary))
                print(b_h, pattern, 'comps generated for', pitcher_name)
        
        temp_df = pm.create_data_frame_of_comps(pitcher_name, comp_list)
    
        df_final_list = df_final_list.append(temp_df)
        print('completed writing to df for', pitcher_name)

du.get_current_time('end')

