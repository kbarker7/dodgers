#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 19:56:47 2020

@author: kevinbarker
"""

import deception_util as du
import math

#Make Dictionary
def create_dictionary_for_handedness(pitches_by_count):
    result_dict = {}
    for x in pitches_by_count:
        pitches_seen = []
        pitch_totals = {}
        pitches_in_count = len(pitches_by_count[x]['pitch_type'])
        p_types = pitches_by_count.get(x).get('pitch_type')
        zones = pitches_by_count.get(x).get('zone')
        pitch_details = du.merge(p_types, zones)
        
        for p in pitch_details:
            if p[0] not in pitches_seen:   
                pitches_seen.append(p[0])
                pitch_totals[p[0]] = {}
                pitch_totals[p[0]][p[1]] = 1
            else:
                if p[1] in pitch_totals.get(p[0]):
                    curr_count = pitch_totals.get(p[0]).get(p[1])
                    pitch_totals.get(p[0])[p[1]] = curr_count + 1
                else:
                    pitch_totals.get(p[0])[p[1]] = 1
    
        for pt in pitch_totals:
            pt_zone_data = pitch_totals[pt]
            for zd in pt_zone_data:
                curr_count = pt_zone_data.get(zd)
                pt_zone_data[zd] = curr_count/pitches_in_count * 100
        
        result_dict[x] = pitch_totals
    return result_dict

#Make Dictionary
def create_dictionary_for_handedness_with_hard_count(pitches_by_count):
    result_dict = {}
    for x in pitches_by_count:
        pitches_seen = []
        pitch_totals = {}
        pitches_in_count = len(pitches_by_count[x]['pitch_type'])
        p_types = pitches_by_count.get(x).get('pitch_type')
        zones = pitches_by_count.get(x).get('zone')
        pitch_details = du.merge(p_types, zones)
        
        for p in pitch_details:
            if p[0] not in pitches_seen:   
                pitches_seen.append(p[0])
                pitch_totals[p[0]] = {}
                pitch_totals[p[0]][p[1]] = 1
            else:
                if p[1] in pitch_totals.get(p[0]):
                    curr_count = pitch_totals.get(p[0]).get(p[1])
                    pitch_totals.get(p[0])[p[1]] = curr_count + 1
                else:
                    pitch_totals.get(p[0])[p[1]] = 1
        
        result_dict[x] = pitch_totals
        #print(x, pitches_in_count)
    return result_dict


#For finding at bats where at least 50% of pitches are considered unlikely
def find_at_bats_with_via_majority_of_pitches(pitches_by_at_bat, count_dictionary, prob_percentile, rate, find_unique):
    ab_list = []
    for ab in pitches_by_at_bat:
        balls = ab[1].balls.values
        strikes = ab[1].strikes.values
        pitches = ab[1].pitch_type.values
        zones = ab[1].zone.values
        events = ab[1].events.values
        
        ab_len = len(pitches)
        num_of_identified_pitches_in_ab = 0
        for i in range(0, ab_len):
            curr_ab_count = str(balls[i]) + '-' + str(strikes[i])
            #print(ab[0], curr_ab_count, pitches[i], zones[i])
            pitch_prob_of_occurring = count_dictionary.get(curr_ab_count).get(pitches[i]).get(zones[i])
            prob_for_p_percentile = du.retrieve_percentile_of_set(count_dictionary.get(curr_ab_count), prob_percentile)
            
            #print(ab[0], 'pitch prob', pitch_prob_of_occurring, '50 percentile', prob_for_p_percentile)
            if find_unique:
                if pitch_prob_of_occurring < prob_for_p_percentile:
                    num_of_identified_pitches_in_ab += 1
            else:
                if pitch_prob_of_occurring > prob_for_p_percentile:
                    num_of_identified_pitches_in_ab += 1
        
        percent_unique = num_of_identified_pitches_in_ab/ab_len
        if percent_unique >= rate:
            if du.check_for_completed_at_bats(events[0], ab[0]):
                ab_list.append(ab)
    return ab_list

#For finding at bats where at least 50% of pitches are considered unlikely
def group_at_bats_with_via_majority_of_pitches(pitches_by_at_bat, count_dictionary, prob_percentile, rate):
    ab_list = {}
    expected_at_bat_list = []
    unexpected_at_bat_list = []
    unexpected_pitch_freezes = 0
    total_unexpected_pitches = 0
    expected_pitch_freezes = 0
    total_expected_pitches = 0
    for ab in pitches_by_at_bat:
        balls = ab[1].balls.values
        strikes = ab[1].strikes.values
        pitches = ab[1].pitch_type.values
        zones = ab[1].zone.values
        events = ab[1].events.values
        descs = ab[1].description.values
        
        ab_len = len(pitches)
        num_of_identified_pitches_in_ab = 0
        for i in range(0, ab_len):
            curr_ab_count = str(balls[i]) + '-' + str(strikes[i])
            #print(ab[0], curr_ab_count, pitches[i], zones[i])
            pitch_prob_of_occurring = count_dictionary.get(curr_ab_count).get(pitches[i]).get(zones[i])
            prob_for_p_percentile = du.retrieve_percentile_of_set(count_dictionary.get(curr_ab_count), prob_percentile)
            
            #print(ab[0], 'pitch prob', pitch_prob_of_occurring, '50 percentile', prob_for_p_percentile)
            if pitch_prob_of_occurring < prob_for_p_percentile:
                num_of_identified_pitches_in_ab += 1
                total_unexpected_pitches += 1
                if descs[i] == 'called_strike':
                    unexpected_pitch_freezes += 1
            else:
                total_expected_pitches += 1
                if descs[i] == 'called_strike':
                    expected_pitch_freezes += 1
            
        percent_unique = num_of_identified_pitches_in_ab/ab_len
        if percent_unique >= rate:
            if du.check_for_completed_at_bats(events[0], ab[0]):
                unexpected_at_bat_list.append(ab)
        else:
            if du.check_for_completed_at_bats(events[0], ab[0]):
                expected_at_bat_list.append(ab)
    ab_list['u'] = unexpected_at_bat_list
    ab_list['e'] = expected_at_bat_list 
    ab_list['u_called'] = unexpected_pitch_freezes/total_unexpected_pitches
    ab_list['e_called'] = expected_pitch_freezes/total_expected_pitches
    return ab_list	


#For finding at bats where the final pitch was considered unlikely
def find_at_bats_via_last_pitch(pitches_by_at_bat, count_dictionary, prob_percentile, find_unique):
    ab_list = []
    for ab in pitches_by_at_bat:
        balls = ab[1].balls.values
        strikes = ab[1].strikes.values
        pitches = ab[1].pitch_type.values
        zones = ab[1].zone.values
        events = ab[1].events.values
        
        final_count_of_at_bat = str(balls[0]) + '-' + str(strikes[0])    
        pitch_prob_of_occurring = count_dictionary.get(final_count_of_at_bat).get(pitches[0]).get(zones[0])
        prob_for_p_percentile = du.retrieve_percentile_of_set(count_dictionary.get(final_count_of_at_bat), prob_percentile)
        
        if find_unique:    
            if pitch_prob_of_occurring < prob_for_p_percentile:
                if du.check_for_completed_at_bats(events[0], ab[0]):
                    ab_list.append(ab)
        else:
            if pitch_prob_of_occurring > prob_for_p_percentile:
                if du.check_for_completed_at_bats(events[0], ab[0]):
                    ab_list.append(ab)
    return ab_list

#For finding at bats where the final pitch was considered unlikely
def group_at_bats_via_last_pitch(pitches_by_at_bat, count_dictionary, prob_percentile):
    ab_list = {}
    expected_at_bat_list = []
    unexpected_at_bat_list = []
    unexpected_pitch_freezes = 0
    expected_pitch_freezes = 0
    for ab in pitches_by_at_bat:
        balls = ab[1].balls.values
        strikes = ab[1].strikes.values
        pitches = ab[1].pitch_type.values
        zones = ab[1].zone.values
        events = ab[1].events.values
        descs = ab[1].description.values
        
        final_count_of_at_bat = str(balls[0]) + '-' + str(strikes[0])    
        pitch_prob_of_occurring = count_dictionary.get(final_count_of_at_bat).get(pitches[0]).get(zones[0])
        prob_for_p_percentile = du.retrieve_percentile_of_set(count_dictionary.get(final_count_of_at_bat), prob_percentile)
        
        if pitch_prob_of_occurring < prob_for_p_percentile:
            if descs[0] == 'called_strike':
                unexpected_pitch_freezes += 1
            if du.check_for_completed_at_bats(events[0], ab[0]):
                unexpected_at_bat_list.append(ab)
        else:
            if descs[0] == 'called_strike':
                expected_pitch_freezes += 1
            if du.check_for_completed_at_bats(events[0], ab[0]):
                expected_at_bat_list.append(ab)
    ab_list['u'] = unexpected_at_bat_list
    ab_list['e'] = expected_at_bat_list 
    ab_list['u_called'] = unexpected_pitch_freezes/len(unexpected_at_bat_list)
    ab_list['e_called'] = expected_pitch_freezes/len(expected_at_bat_list)
    return ab_list


#For finding at bats where the first pitch was considered unlikely
def find_at_bats_via_first_pitch(pitches_by_at_bat, count_dictionary, prob_percentile, find_unique):
    unique_ab_list = []
    for ab in pitches_by_at_bat:
        pitches = ab[1].pitch_type.values
        zones = ab[1].zone.values
        events = ab[1].events.values
        first_pitch_index = len(pitches) - 1
        #print(ab[0], pitches[first_pitch_index], zones[first_pitch_index])
        pitch_prob_of_occurring = count_dictionary.get('0-0').get(pitches[first_pitch_index]).get(zones[first_pitch_index])
        prob_for_p_percentile = du.retrieve_percentile_of_set(count_dictionary.get('0-0'), prob_percentile)
        #print(ab[0], pitch_prob_of_occurring, prob_for_p_percentile)
        if find_unique:
            if pitch_prob_of_occurring < prob_for_p_percentile:
                if du.check_for_completed_at_bats(events[0], ab[0]):
                    unique_ab_list.append(ab)
        else:
            if pitch_prob_of_occurring > prob_for_p_percentile:
                if du.check_for_completed_at_bats(events[0], ab[0]):
                    unique_ab_list.append(ab)
    return unique_ab_list

#For finding at bats where the first pitch was considered unlikely
def group_at_bats_via_first_pitch(pitches_by_at_bat, count_dictionary, prob_percentile):
    ab_list = {}
    expected_at_bat_list = []
    unexpected_at_bat_list = []
    unexpected_pitch_freezes = 0
    expected_pitch_freezes = 0
    for ab in pitches_by_at_bat:
        pitches = ab[1].pitch_type.values
        zones = ab[1].zone.values
        events = ab[1].events.values
        balls = ab[1].balls.values
        strikes = ab[1].strikes.values
        descs = ab[1].description.values
        first_pitch_index = len(pitches) - 1
        #Handles when first pitch is dropped via null or too far from plate
        adjusted_first_count = str(balls[first_pitch_index]) + '-' + str(strikes[first_pitch_index])
        #print(ab[0], adjusted_first_count, pitches[first_pitch_index], zones[first_pitch_index])
        pitch_prob_of_occurring = count_dictionary.get(adjusted_first_count).get(pitches[first_pitch_index]).get(zones[first_pitch_index])
        prob_for_p_percentile = du.retrieve_percentile_of_set(count_dictionary.get('0-0'), prob_percentile)
        #print(ab[0], pitch_prob_of_occurring, prob_for_p_percentile)
        if pitch_prob_of_occurring < prob_for_p_percentile:
            if descs[first_pitch_index] == 'called_strike':
                unexpected_pitch_freezes += 1
            if du.check_for_completed_at_bats(events[0], ab[0]):
                unexpected_at_bat_list.append(ab)
        else:
            if descs[first_pitch_index] == 'called_strike':
                expected_pitch_freezes += 1
            if du.check_for_completed_at_bats(events[0], ab[0]):
                expected_at_bat_list.append(ab)
    ab_list['u'] = unexpected_at_bat_list
    ab_list['e'] = expected_at_bat_list
    #print('u', unexpected_pitch_freezes, len(unexpected_at_bat_list))
    #print('e', expected_pitch_freezes, len(expected_at_bat_list))
    ab_list['u_called'] = unexpected_pitch_freezes/len(unexpected_at_bat_list)
    ab_list['e_called'] = expected_pitch_freezes/len(expected_at_bat_list)
    return ab_list

    