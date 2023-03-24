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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    argParser.add_argument("-a", "--alcohol", type=str, help="yesterdays alcohol intake  1-4 scale where 1 is none and 4 is excessive")
    
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
        user_stress_yesterday = user_manual_values.stress
    except KeyError:
        user_stress_yesterday = None
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
    try:
        user_alcohol_yesterday = user_manual_values.alcohol
    except Keyerror:
        user_alcohol_yesterday = None
###### withings.com
    if config.use_service_withings =='True':
        # read withings
        print('reading withings.com values ...')

        result_withings_values = withings.readvalues(config.withings_delta, withingstoken) # values of the last delta days
        if result_withings_values == None:
            result_withings_values = {}
            print(f'{bcolors.FAIL}Fail: No withings result!{bcolors.ENDC}')
        try:
            withings_values = result_withings_values[0]
            withings_values_today = result_withings_values[1]
        except KeyError:
            withings_values = {}
            withings_values_today = {}
            print(f'{bcolors.FAIL}Fail: No withings values!{bcolors.ENDC}')
            
        if user_weight_today == None:
            try:
                user_weight_today = withings_values_today['weight']
            except KeyError:
                print(f'{bcolors.WARNING}Warning: withings weight is unknown.{bcolors.ENDC}')
        if user_bodyfat_today == None:
            try:
                user_bodyfat_today = withings_values_today['bodyfat']
            except KeyError:
                print(f'{bcolors.WARNING}Warning: withings bodyfat is unknown.{bcolors.ENDC}')
        if user_diastolic_today == None:
            try:
                user_diastolic_today = withings_values_today['diastolic']
            except KeyError:
                print(f'{bcolors.WARNING}Warning: withings diastolic is unknown.{bcolors.ENDC}')
        if user_systolic_today == None:
            try:
                user_systolic_today = withings_values_today['systolic']
            except KeyError:
                print(f'{bcolors.WARNING}Warning: withings systolic is unknown.{bcolors.ENDC}')
        if user_temperature_today == None:
            try:
                user_temperature_today = withings_values_today['temperature']
            except KeyError:
                print(f'{bcolors.WARNING}Warning: withings temperature is unknown.{bcolors.ENDC}')
        print(f'{bcolors.OKGREEN}  \u2713  {bcolors.ENDC} {bcolors.OKBLUE}reading withings done.{bcolors.ENDC}')
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
            print(f'{bcolors.WARNING}Warning: garmin restingHeartRate is unknown.{bcolors.ENDC}')
            user_restingHeartRate_today = None
        
        time.sleep(3)
        garmin_today_sleep_values = garmin.read_value(today,'c')
        try:
            garmin_today_sleepdata_values = garmin_today_sleep_values['dailySleepDTO']
            if garmin_today_sleepdata_values == None:
                garmin_today_sleepdata_values = {}
                print(f'{bcolors.FAIL}Fail: garmin no today sleepdata!{bcolors.ENDC}')
        except KeyError:
            print(f'{bcolors.FAIL}Fail: garmin daily Sleep Values not found.{bcolors.ENDC}')
            garmin_today_sleepdata_values = None
        
        try:
            user_sleepTimeseconds_today = garmin_today_sleepdata_values['sleepTimeSeconds']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin sleepTimeSeconds is unknown.{bcolors.ENDC}')
            user_sleepTimeseconds_today = None
        try:
            user_deepSleepSeconds_today = garmin_today_sleepdata_values['deepSleepSeconds']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin deepSleepSeconds is unknown.{bcolors.ENDC}')
            user_deepSleepSeconds_today = None
        try:
            user_lightSleepSeconds_today = garmin_today_sleepdata_values['lightSleepSeconds']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin lightSleepSeconds is unknown.{bcolors.ENDC}')
            user_lightSleepSeconds_today = None
        try:
            user_remSleepSeconds_today = garmin_today_sleepdata_values['remSleepSeconds']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin remSleepSeconds is unknown.{bcolors.ENDC}')
            user_remSleepSeconds_today = None
        try:
            user_awakeSleepSeconds_today = garmin_today_sleepdata_values['awakeSleepSeconds']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin awakeSleepSeconds is unknown.{bcolors.ENDC}')
            user_awakeSleepSeconds_today = None
        try:
            user_averageSpO2HRSleep_today = garmin_today_sleepdata_values['averageSpO2HRSleep']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin averageSpO2HRSleep is unknown.{bcolors.ENDC}')
            user_averageSpO2HRSleep_today = None
        try:
            user_averageSpO2Value_today = garmin_today_sleepdata_values['averageSpO2Value']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin averageSpO2Value is unknown.{bcolors.ENDC}')
            user_averageSpO2Value_today = None
            
        garmin_today_sleep_values_sleepScores = garmin_today_sleepdata_values['sleepScores']
        garmin_today_sleep_values_sleepScores_overall = garmin_today_sleep_values_sleepScores['overall']
        try:
            user_sleepscore_today = garmin_today_sleep_values_sleepScores_overall['value']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin sleepscore value is unknown.{bcolors.ENDC}')
            user_sleepscore_today = None
        try:
            user_sleepquality_today = garmin_today_sleep_values_sleepScores_overall['qualifierKey']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin sleepquality is unknown.{bcolors.ENDC}')
            user_sleepquality_today = None
        
        ## yesterday values
        garmin_yesterday_values = garmin.read_value(yesterday,'7')
        try:
            user_steps_yesterday = garmin_yesterday_values['totalSteps']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin totalSteps is unknown.{bcolors.ENDC}')
            user_steps_yesterday = None
        try:
            user_restingHeartRate_yesterday = garmin_yesterday_values['restingHeartRate']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin restingHeartRate is unknown.{bcolors.ENDC}')
            user_restingHeartRate_yesterday = None
        try:
            user_floors_yesterday = garmin_yesterday_values['floorsAscended']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin floors are unknown is unknown.{bcolors.ENDC}')
            user_floors_yesterday = None
        try:
            user_averageStressLevel_yesterday = garmin_yesterday_values['averageStressLevel']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin average Stresslevel is unknown.{bcolors.ENDC}')
            user_averageStressLevel_yesterday = None
        try:
            user_averageRespirationValue_yesterday = garmin_yesterday_values['avgWakingRespirationValue']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin average Respiration is unknown.{bcolors.ENDC}')
            user_averageRespirationValue_yesterday = None
        try:
            user_consumedKilocalories_yesterday = garmin_yesterday_values['consumedKilocalories']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin consumed kilocalories are unknown. unknown.{bcolors.ENDC}')
            user_consumedKilocalories_yesterday = None
        try:
            user_activeKilocalories_yesterday = garmin_yesterday_values['activeKilocalories']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin average Respiration is unknown.{bcolors.ENDC}')
            user_activeKilocalories_yesterday = None
        try:
            user_netCalorieGoal_yesterday = garmin_yesterday_values['netCalorieGoal']
        except KeyError:
            print(f'{bcolors.WARNING}Warning: garmin net calorie-goal is unknown.{bcolors.ENDC}')
            user_netCalorieGoal_yesterday = None
        print( f'{bcolors.OKGREEN}  \u2713 {bcolors.ENDC} {bcolors.OKBLUE} reading garmin connect done{bcolors.ENDC}')
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
        
        # Create dictionary for yesterday
        intervals_yesterday_data = {}
        intervals_yesterday_data["id"] = str(yesterday)
        if user_steps_yesterday:
            intervals_yesterday_data[config.intervals_steps_field] = user_steps_yesterday
        if user_alcohol_yesterday and config.intervals_alcohol_field:
            intervals_yesterday_data[config.intervals_alcohol_field] = int(user_alcohol_yesterday)
        if user_floors_yesterday and config.intervals_floors_field:
            intervals_yesterday_data[config.intervals_floors_field] = user_floors_yesterday
        if user_averageStressLevel_yesterday and config.intervals_stress_field: # 0–25: recreation 26–50: low Stress 51–75: avg Stress 76–100: high Stress
#            try:
#                if user_averageStressLevel_yesterday <= 25:
#                    user_stress_yesterday_intervals = 1
#                elif user_averageStressLevel_yesterday >25 and user_averageStressLevel_yesterday <= 50:
#                    user_stress_yesterday_intervals = 2
#                elif user_averageStressLevel_yesterday >50 and user_averageStressLevel_yesterday <= 75:
#                    user_stress_yesterday_intervals = 3
#                elif user_averageStressLevel_yesterday >75:
#                    user_stress_yesterday_intervals = 4
#            except:
#                print ('error in calculating stress for intervals')
#            intervals_yesterday_data[config.intervals_stress_field] = user_stress_yesterday_intervals
            intervals_yesterday_data[config.intervals_StressScore_field] = user_averageStressLevel_yesterday
        if user_stress_yesterday and config.intervals_stress_field:
            intervals_yesterday_data[config.intervals_stress_field] = user_stress_yesterday
        if user_averageRespirationValue_yesterday and config.intervals_averageRespiration_field:
            intervals_yesterday_data[config.intervals_averageRespiration_field] = user_averageRespirationValue_yesterday
        if user_netCalorieGoal_yesterday and config.intervals_netCalorieGoal_field:
            intervals_yesterday_data[config.intervals_netCalorieGoal_field] = user_netCalorieGoal_yesterday
        if user_activeKilocalories_yesterday and config.intervals_activeCalories_field:
            intervals_yesterday_data[config.intervals_activeCalories_field] = user_activeKilocalories_yesterday
        if user_netCalorieGoal_yesterday and user_activeKilocalories_yesterday and config.intervals_CalorieGoal_field:
            user_CalorieGoal_yesterday = user_netCalorieGoal_yesterday + user_activeKilocalories_yesterday
            intervals_yesterday_data[config.intervals_CalorieGoal_field] = user_CalorieGoal_yesterday
        if user_consumedKilocalories_yesterday and config.intervals_consumedCalories_field:
            intervals_yesterday_data[config.intervals_consumedCalories_field] = user_consumedKilocalories_yesterday
        if user_consumedKilocalories_yesterday and user_CalorieGoal_yesterday and config.intervals_GoalConsumedDifferenceCalories_field:
            user_CaloriesDifference = user_CalorieGoal_yesterday - user_consumedKilocalories_yesterday
            intervals_yesterday_data[config.intervals_GoalConsumedDifferenceCalories_field] = user_CaloriesDifference
        
        
        # write data
        print (intervals_today_data)
        intervals.set_wellness(intervals_today_data, today)
        print (intervals_yesterday_data)
        intervals.set_wellness(intervals_yesterday_data, yesterday)
        print(f'{bcolors.OKGREEN}  \u2713  {bcolors.ENDC} {bcolors.OKBLUE}writing to intervals.icu done{bcolors.ENDC}')
    else:
        print('intervals.icu is not used ...')

    if config.use_service_wahoo =='True' and user_weight_today is not None:
        print ('writing to wahoo ...')
        wahoo.write_to_wahoo(user_weight_today)
        print(f'{bcolors.OKGREEN}  \u2713  {bcolors.ENDC} {bcolors.OKBLUE}writing to wahoo done{bcolors.ENDC}')
    else:
        print('wahoo is not used... or user weight is None')

    if config.use_service_strava == 'True' and user_weight_today is not None:
        print('writing values to strava.com ...')
        
        print(f'{bcolors.OKGREEN}  \u2713  {bcolors.ENDC} {bcolors.OKBLUE}writing to strava done{bcolors.ENDC}')
    else:
        print('strava is not used ... or user weight is None')

    ## execute external scripts
    print('running external scripts ...')
###### matlab
#    if config.use_service_matlab == 'True':
#        print('starting script on matlab ...')
#        matlab.runImReady4()
#    else:
#        print('matlab is not used ...')
    print(f'{bcolors.OKGREEN}  \u2713 \u2713 {bcolors.ENDC}{bcolors.OKCYAN}all done{bcolors.ENDC}')

if __name__ == '__main__': exit(main())

def convert(seconds): 
            return time.strftime("%H:%M:%S", time.gmtime(seconds)) 