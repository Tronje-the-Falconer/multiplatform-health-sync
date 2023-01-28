#!/usr/bin/python3
"""
    This program synchronizes health values from different plattforms like withings.com and garmin connect to intervals.icu, strava, etc.
    You can enter it by commandline with the parameters below for manual values or if checked in the env.env use the services.
    There is also a website availiable where you can enter your current values, which is running this script with these. raspberry
"""
######################################################
# config section 
######################################################
import os
import sys

import json
from datetime import datetime, timedelta
import time
import argparse

import config
import withings
import garmin
import intervals
import strava
import wahoo
import matlab

def get_script_arguments():
    print('reading script arguments ...')
    argParser = argparse.ArgumentParser(description=__doc__ , epilog="You can find the current Version and more informations on GitHub: https://github.com/Tronje-the-Falconer/multiplatform-health-sync")
    # argParser.add_argument("-n", "--name", help="your name")
    # argParser.add_argument("-i", "--int", type=int, help="your numeric age ")
    # argParser.add_argument("-h", "--help", , help="this helptext is displayed")
    argParser.add_argument("-m", "--mood", type=int, help="todays mood 1-4 scale where 1 is good and 4 is bad")
    argParser.add_argument("-s", "--stress", type=int, help="todays stress 1-4 scale where 1 is good and 4 is bad")
    argParser.add_argument("-f", "--fatigue", type=int, help="todays fatigue pre training 1-4 scale where 1 is good and 4 is bad")
    argParser.add_argument("-w", "--weight", type=float, help="todays weight in kg")
    argParser.add_argument("-bf", "--bodyfat", type=float, help="todays bodyfat in %")
    argParser.add_argument("-t", "--temperature", type=float, help="todays temperature in °C")
    argParser.add_argument("-sy", "--systolic", type=int, help="todays systolic")
    argParser.add_argument("-di", "--diastolic", type=int, help="todays diastolic")
    argParser.add_argument("-wt", "--withingstoken", type=str, help="authentication-token from withings for first authentification (url-parameter)")
    argParser.add_argument("-st", "--stravatoken", type=str, help="authentication-token from strava for first authentification (url-parameter)")
    
    user_manual_values = argParser.parse_args()
    
    return user_manual_values


######################################################
## Start of Main Script
######################################################
def main():
    ##reading data
    print ('reading data ...')
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
    try:
        user_temperature_today = user_manual_values.temperature
    except KeyError:
        user_temperature_today = None
    try:
        user_systolic_today = user_manual_values.systolic
    except KeyError:
        user_systolic_today = None
    try:
        user_diastolic_today = user_manual_values.diastolic
    except KeyError:
        user_diastolic_today = None
    # tokens
    try:
        withingstoken = user_manual_values.withingstoken
    except Keyerror:
        withingstoken = None
###### withings.com
    if config.use_service_withings =='True':
        # read withings
        print('reading withings.com values ...')

        result_withings_values = withings.readvalues(config.withings_delta, withingstoken) # values of the last delta days
        withings_values = result_withings_values[0]
        withings_values_today = result_withings_values[1]
        
        if user_weight_today == None:
            try:
                user_weight_today = withings_values_today['weight']
            except KeyError:
                print('withings weight is unknown.')
        if user_bodyfat_today == None:
            try:
                user_bodyfat_today = withings_values_today['bodyfat']
            except KeyError:
                print('withings bodyfat is unknown.')
        if user_diastolic_today == None:
            try:
                user_diastolic_today = withings_values_today['diastolic']
            except KeyError:
                print('withings diastolic is unknown.')
        if user_systolic_today == None:
            try:
                user_systolic_today = withings_values_today['systolic']
            except KeyError:
                print('withings systolic is unknown.')
        if user_temperature_today == None:
            try:
                user_temperature_today = withings_values_today['temperature']
            except KeyError:
                print('withings temperature is unknown.')
        print('reading withings done.')
    else:
        print('withings.com is not used ...')
    
###### garmin connect
    if config.use_service_garmin:
        print('reading garmin connect values ...')
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
        print ('reading garmin connect done')
    else:
        print('garmin connect is not used ...')
    
    ## writing data
    print('writing data ...')
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
        if user_diastolic_today and config.intervals_diastolic_field:
            intervals_today_data[config.intervals_diastolic_field] = user_diastolic_today
        if user_systolic_today and config.intervals_systolic_field:
            intervals_today_data[config.intervals_systolic_field] = user_systolic_today
        if user_temperature_today and config.intervals_temperature_field:
            intervals_today_data[config.intervals_temperature_field] = user_temperature_today
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
        print ('writing to intervals.icu done')
    else:
        print('intervals.icu is not used ...')

    if config.use_service_wahoo =='True':
        print ('writing to wahoo ...')
        wahoo.write_to_wahoo(user_weight_today)
        print ('writing to wahoo done')
    else:
        print('wahoo is not used...')

    if config.use_service_strava == 'True':
        print('writing values to strava.com ...')
        strava.write_to_strava(user_weight_today)
    else:
        print('strava is not used ...')

    ## execute external scripts
    print('running external scripts ...')
###### matlab
#    if config.use_service_matlab == 'True':
#        print('starting script on matlab ...')
#        matlab.runImReady4()
#    else:
#        print('matlab is not used ...')
    
    print('all done!')

 

def convert(seconds): 
            return time.strftime("%H:%M:%S", time.gmtime(seconds)) 

if __name__ == '__main__': exit(main())