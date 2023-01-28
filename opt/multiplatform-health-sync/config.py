#!/usr/bin/python3
"""
    Load .env file and environment settings
"""
import os
import sys


from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'env.env')
load_dotenv(dotenv_path)

## used services
use_service_intervals = os.getenv('service_intervals')
use_service_withings = os.getenv('service_whithings')
use_service_garmin = os.getenv('service_garmin')
use_service_matlab = os.getenv('service_matlab')
use_service_wahoo = os.getenv('service_wahoo')
use_service_strava = os.getenv('service_strava')

## Withings api credentials
withings_client_id = os.getenv('withings_client_id')
withings_client_secret = os.getenv('withings_client_secret')
withings_redirect_uri = os.getenv('withings_redirect_uri')

withings_cfg=os.path.join(os.path.dirname(__file__), 'withings.json')
withings_api='https://wbsapi.withings.net/v2'

withings_delta=(int(os.getenv('withings_delta'))-1) #0-based

## intervals.icu api credentials
intervals_athlete_id = os.getenv('intervals_athlete_id')
intervals_api_key = os.getenv('intervals_api_key')
intervals_api = 'https://intervals.icu/api/v1/athlete/%s' % intervals_athlete_id

## intervals Fields
intervals_weight_field = os.getenv('intervals_weight_field')
if (intervals_weight_field == ''):
    intervals_weight_field = None
intervals_bodyfat_field = os.getenv('intervals_bodyfat_field')
if (intervals_bodyfat_field == ''):
    intervals_bodyfat_field = None
intervals_diastolic_field = os.getenv('intervals_diastolic_field')
if (intervals_diastolic_field == ''):
    intervals_diastolic_field = None
intervals_systolic_field = os.getenv('intervals_systolic_field')
if (intervals_systolic_field == ''):
    intervals_systolic_field = None
intervals_temperature_field = os.getenv('intervals_temperature_field')
if (intervals_temperature_field == ''):
    intervals_temperature_field = None
intervals_steps_field = os.getenv('intervals_steps_field')
if (intervals_steps_field == ''):
    intervals_steps_field = None
intervals_sleepTimeseconds_field = os.getenv('intervals_sleepTimeseconds_field')
if (intervals_sleepTimeseconds_field == ''):
    intervals_sleepTimeseconds_field = None
intervals_deepSleepSeconds_field = os.getenv('intervals_deepSleepSeconds_field')
if (intervals_deepSleepSeconds_field == ''):
    intervals_deepSleepSeconds_field = None
intervals_lightSleepSeconds_field = os.getenv('intervals_lightSleepSeconds_field')
if (intervals_lightSleepSeconds_field == ''):
    intervals_lightSleepSeconds_field = None
intervals_remSleepSeconds_field = os.getenv('intervals_remSleepSeconds_field')
if (intervals_remSleepSeconds_field == ''):
    intervals_remSleepSeconds_field = None
intervals_awakeSleepSeconds_field = os.getenv('intervals_awakeSleepSeconds_field')
if (intervals_awakeSleepSeconds_field == ''):
    intervals_awakeSleepSeconds_field = None
intervals_sleepscore_field = os.getenv('intervals_sleepscore_field')
if (intervals_sleepscore_field == ''):
    intervals_sleepscore_field = None
intervals_sleepquality_field = os.getenv('intervals_sleepquality_field')
if (intervals_sleepquality_field == ''):
    intervals_sleepquality_field = None
intervals_averageSpO2HRSleep_field = os.getenv('intervals_averageSpO2HRSleep_field')
if (intervals_averageSpO2HRSleep_field == ''):
    intervals_averageSpO2HRSleep_field = None
intervals_averageSpO2Value_field = os.getenv('intervals_averageSpO2Value_field')
if (intervals_averageSpO2Value_field == ''):
    intervals_averageSpO2Value_field = None
intervals_restingHeartRate_field = os.getenv('intervals_restingHeartRate_field')
if (intervals_restingHeartRate_field == ''):
    intervals_restingHeartRate_field = None
intervals_stress_field = os.getenv('intervals_stress_field')
if (intervals_stress_field == ''):
    intervals_stress_field = None
intervals_mood_field = os.getenv('intervals_mood_field')
if (intervals_mood_field == ''):
    intervals_mood_field = None
intervals_fatigue_field = os.getenv('intervals_fatigue_field')
if (intervals_fatigue_field == ''):
    intervals_fatigue_field = None

## Strava api credentials
strava_athlete_id = os.getenv('strava_athlete_id')
strava_client_secret = os.getenv('strava_client_secret')
strava_cfg=os.path.join(os.path.dirname(__file__), 'strava.json')
strava_url='https://www.strava.com/oauth'
strava_api='https://www.strava.com/api/v3'

## Wahoo API access
wahoo_client_id = os.getenv('wahoo_client_id')
wahoo_secret = os.getenv('wahoo_secret')
wahoo_redirect_uri = os.getenv('wahoo_redirect_uri')
wahoo_api='https://api.wahooligan.com'
wahoo_cfg=os.path.join(os.path.dirname(__file__), 'wahoo.json')
wahoo_scopes='user_write+email+workouts_read+workouts_write+power_zones_read+power_zones_write+offline_data+user_read'

## Garmin credentials
garmin_email = os.getenv('garmin_email')
garmin_password = os.getenv('garmin_password')
garmin_cfg=os.path.join(os.path.dirname(__file__), 'garmin.json')
