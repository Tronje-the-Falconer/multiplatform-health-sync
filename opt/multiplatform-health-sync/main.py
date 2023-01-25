#!/usr/bin/python3
"""
    healthvalues sync
"""
######################################################
# config section 
######################################################
import os
import sys

import json
import requests
import webbrowser
from datetime import datetime, timedelta
import time
import argparse

import config
import withings
import garmin
import matlab
import intervals



def get_script_arguments():
    argParser = argparse.ArgumentParser()
    # argParser.add_argument("-n", "--name", help="your name")
    # argParser.add_argument("-i", "--int", type=int, help="your numeric age ")
    argParser.add_argument("-m", "--mood", type=int, help="todays mood 1-4 scale where 1 is good and 4 is bad")
    argParser.add_argument("-s", "--stress", type=int, help="todays stress 1-4 scale where 1 is good and 4 is bad")
    argParser.add_argument("-f", "--fatigue", type=int, help="todays fatigue pre training 1-4 scale where 1 is good and 4 is bad")
    argParser.add_argument("-w", "--weight", type=float, help="todays weight in kg")
    argParser.add_argument("-bf", "--bodyfat", type=float, help="todays bodyfat in %")
    
    user_manual_values = argParser.parse_args()
    
    return user_manual_values


######################################################
## Start of Main Script
######################################################
def main():
    today = datetime.fromtimestamp(time.time()).date()
    yesterday = datetime.today().date() - timedelta(1)
    
    user_manual_values = get_script_arguments()
    try:
        user_mood_today = user_manual_values.mood
    except Keyerror:
        user_mood_today = None
    try:
        user_stress_today = user_manual_values.stress
    except KeyError:
        user_stress_today = None
    try:
        user_fatigue_today = user_manual_values.fatigue
    except KeyError:
        user_fatigue_today = None
    
    # possible automated values
    try:
        user_bodyfat_today = user_manual_values.bodyfat
    except KeyError:
        user_bodyfat_today = None
    try:
        user_weight_today = user_manual_values.weight
    except KeyError:
        user_weight_today = None
    
###### withings.com
    if config.use_service_withings =='True':
        # read withings
        print('reading withings.com values ...')
        
        result_withings_values = withings.readvalues(config.withings_delta) # values of the last delta days
        withings_values = result_withings_values[0]
        withings_values_today = result_withings_values[1]
        
        if user_weight_today == None:
            try:
                user_weight_today = withings_values_today['weight']
            except KeyError:
                print('weight is unknown.')
                user_weight_today = None
        if user_bodyfat_today == None:
            try:
                user_bodyfat_today = withings_values_today['bodyfat']
            except KeyError:
                print('bodyfat is unknown.')
                user_bodyfat_today = None
        try:
            user_diastolic = withings_values_today['diastolic']
        except KeyError:
            print('diastolic is unknown.')
            user_diastolic = None
        try:
            user_systolic = withings_values_today['systolic']
        except KeyError:
            print('systolic is unknown.')
            user_systolic = None
        try:
            user_temperature = withings_values_today['temperature']
        except KeyError:
            print('temperature is unknown.')
            user_temperature = None
        
    else:
        print('withings.com is not used ...')
    
###### garmin connect
    if config.use_service_garmin:
        print('reading garmin connect values ...')
        
        
        # VO2Max
        # Training Advice
        
        #manuell
        # Fatigue
        # stress
        # mood
        
        ## today values
        garmin_today_values = garmin.read_value(today,'7')
        try:
            user_restingHeartRate_today = garmin_today_values['restingHeartRate']
        except KeyError:
            print('restingHeartRate is unknown.')
            user_restingHeartRate_today = None
        
        garmin_today_sleep_values = garmin.read_value(today,'c')
        garmin_today_sleepdata_values = garmin_today_sleep_values['dailySleepDTO']
        try:
            user_sleepTimeseconds_today = garmin_today_sleepdata_values['sleepTimeSeconds']
        except KeyError:
            print('sleepTimeSeconds is unknown.')
            user_sleepTimeseconds_today = None
        try:
            user_deepSleepSeconds_today = garmin_today_sleepdata_values['deepSleepSeconds']
        except KeyError:
            print('deepSleepSeconds is unknown.')
            user_deepSleepSeconds_today = None
        try:
            user_lightSleepSeconds_today = garmin_today_sleepdata_values['lightSleepSeconds']
        except KeyError:
            print('lightSleepSeconds is unknown.')
            user_lightSleepSeconds_today = None
        try:
            user_remSleepSeconds_today = garmin_today_sleepdata_values['remSleepSeconds']
        except KeyError:
            print('remSleepSeconds is unknown.')
            user_remSleepSeconds_today = None
        try:
            user_awakeSleepSeconds_today = garmin_today_sleepdata_values['awakeSleepSeconds']
        except KeyError:
            print('awakeSleepSeconds is unknown.')
            user_awakeSleepSeconds_today = None
        try:
            user_averageSpO2HRSleep_today = garmin_today_sleepdata_values['averageSpO2HRSleep']
        except KeyError:
            print('averageSpO2HRSleep is unknown.')
            user_averageSpO2HRSleep_today = None
        try:
            user_averageSpO2Value_today = garmin_today_sleepdata_values['averageSpO2Value']
        except KeyError:
            print('averageSpO2Value is unknown.')
            user_averageSpO2Value_today = None
            
        garmin_today_sleep_values_sleepScores = garmin_today_sleepdata_values['sleepScores']
        garmin_today_sleep_values_sleepScores_overall = garmin_today_sleep_values_sleepScores['overall']
        try:
            user_sleepscore_today = garmin_today_sleep_values_sleepScores_overall['value']
        except KeyError:
            print('sleepscore value is unknown.')
            user_sleepscore_today = None
        try:
            user_sleepquality_today = garmin_today_sleep_values_sleepScores_overall['qualifierKey']
        except KeyError:
            print('sleepquality is unknown.')
            user_sleepquality_today = None
        
        ## yesterday values
        garmin_yesterday_values = garmin.read_value(yesterday,'7')
        try:
            user_steps_yesterday = garmin_yesterday_values['totalSteps']
        except KeyError:
            print('totalSteps is unknown.')
            user_steps_yesterday = None
        try:
            user_restingHeartRate_yesterday = garmin_yesterday_values['restingHeartRate']
        except KeyError:
            print('restingHeartRate is unknown.')
            user_restingHeartRate_yesterday = None
    else:
        print('garmin connect is not used ...')
    
###### matlab
#    if config.use_service_matlab == 'True':
#        print('starting script on matlab ...')
#        matlab.runImReady4()
#    else:
#        print('matlab is not used ...')
    
###### intervals.icu
    if config.use_service_intervals == 'True':
        print('writing values to intervals.icu ...')
        # Write to Intervals.icu
        # Create Dictionary for today
        intervals_today_data = {}
        intervals_today_data["id"] = str(today)
        if user_weight_today and config.intervals_weight_field:
            intervals_today_data[config.intervals_weight_field] = user_weight_today
        if user_bodyfat_today and config.intervals_bodyfat_field:
            intervals_today_data[config.intervals_bodyfat_field] = user_bodyfat_today
        if user_diastolic and config.intervals_diastolic_field:
            intervals_today_data[config.intervals_diastolic_field] = user_diastolic
        if user_systolic and config.intervals_systolic_field:
            intervals_today_data[config.intervals_systolic_field] = user_systolic
        if user_temperature and config.intervals_temperature_field:
            intervals_today_data[config.intervals_temperature_field] = user_temperature
        if user_sleepTimeseconds_today and config.intervals_sleepTimeseconds_field:
            intervals_today_data[config.intervals_sleepTimeseconds_field] = user_sleepTimeseconds_today
        if user_deepSleepSeconds_today and config.intervals_deepSleepSeconds_field:
            intervals_today_data[config.intervals_deepSleepSeconds_field] = user_deepSleepSeconds_today
        if user_lightSleepSeconds_today and config.intervals_lightSleepSeconds_field:
            intervals_today_data[config.intervals_lightSleepSeconds_field] = user_lightSleepSeconds_today
        if user_remSleepSeconds_today and config.intervals_remSleepSeconds_field:
            intervals_today_data[config.intervals_remSleepSeconds_field] = user_remSleepSeconds_today
        if user_awakeSleepSeconds_today and config.intervals_awakeSleepSeconds_field:
            intervals_today_data[config.intervals_awakeSleepSeconds_field] = user_awakeSleepSeconds_today
        if user_sleepscore_today and config.intervals_sleepscore_field:
            intervals_today_data[config.intervals_sleepscore_field] = user_sleepscore_today
        if user_sleepquality_today and config.intervals_sleepquality_field: #Garmin= Excellent (1): 90–100, Good(2): 80–89, Fair(3): 60–79, Poor(4): Below 60
            try:
                if user_sleepquality_today == 'EXCELLENT':
                    user_sleepquality_today_intervals = 1
                elif user_sleepquality_today == 'GOOD':
                    user_sleepquality_today_intervals = 2
                elif user_sleepquality_today == 'FAIR':
                    user_sleepquality_today_intervals = 3
                elif user_sleepquality_today == 'POOR':
                    user_sleepquality_today_intervals = 4
                intervals_today_data[config.intervals_sleepquality_field] = user_sleepquality_today_intervals
            except:
                print ('error in transform status to int')
        if user_averageSpO2HRSleep_today and config.intervals_averageSpO2HRSleep_field:
            intervals_today_data[config.intervals_averageSpO2HRSleep_field] = user_averageSpO2HRSleep_today
        if user_averageSpO2Value_today and config.intervals_averageSpO2Value_field:
            intervals_today_data[config.intervals_averageSpO2Value_field] = user_averageSpO2Value_today
        if user_restingHeartRate_today and config.intervals_restingHeartRate_field:
            intervals_today_data[config.intervals_restingHeartRate_field] = user_restingHeartRate_today
        if user_mood_today and config.intervals_mood_field:
            intervals_today_data[config.intervals_mood_field] = user_mood_today
        if user_fatigue_today and config.intervals_fatigue_field:
            intervals_today_data[config.intervals_fatigue_field] = user_fatigue_today
        if user_stress_today and config.intervals_stress_field:
            intervals_today_data[config.intervals_stress_field] = user_stress_today
        
        # Create dictionary for yesterday
        intervals_yesterday_data = {}
        intervals_yesterday_data["id"] = str(yesterday)
        if user_steps_yesterday:
            intervals_yesterday_data[config.intervals_steps_field] = user_steps_yesterday
        
        # write data
        print (intervals_today_data)
        intervals.set_wellness(intervals_today_data, today)
        print (intervals_yesterday_data)
        intervals.set_wellness(intervals_yesterday_data, yesterday)
    else:
        print('intervals.icu is not used ...')

    # if use_service_wahoo('True'):
        # Get Wahoo_access_token or refresh the token
        # wahoo_access_token = wahoo_refresh(json.load(open(wahoo_cfg))) if os.path.isfile(wahoo_cfg) else wahoo_authenticate()
        # wahoo_user_info = get_wahoo_user( wahoo_access_token)
        # print('Retreived Wahoo userid %s for %s %s' % (wahoo_user_info['id'], wahoo_user_info['first'], wahoo_user_info['last']))
        # set_wahoo_user_weight( wahoo_access_token, user_weight_today)
    # else:
        # print('wahoo is not used...')

#    if use_service_strava('True'):
#        print('writing values to strava.com ...')
#        strava.write_to_strava(user_weight_today)
#    else:
#        print('strava is not used ...')

def convert(seconds): 
            return time.strftime("%H:%M:%S", time.gmtime(seconds)) 

if __name__ == '__main__': exit(main())