##### Services used #####
## False not used True will use it
service_intervals='False'
service_whithings='False'
service_garmin='False'
service_matlab='False'
service_wahoo='False'
service_strava='False'


##### API Settings #####

## intervals.icu
intervals_athlete_id='INTERVALS_ATHLETE_ID'
intervals_api_key='INTERVALS_API_KEY'

## withings.com
withings_client_id='WITHINGS_CLIENT_ID'
withings_client_secret='WITHINGS_CLIENT_SECRET'
withings_redirect_uri='WITHINGS_REDIRECT_URI' # client_id and client_secret from withings app - register on https://developer.withings.com/dashboard/

## wahoo
wahoo_client_id='WAHOO_CLIENT_ID'
wahoo_secret='WAHOO_SECRET'
wahoo_redirect_uri='WAHOO_REDIRECT_URI'

## strava.com
strava_athlete_id='STRAVA_ATHLETE_ID'
strava_client_secret='STRAVA_SECRET'

## garmin
garmin_email='GARMIN_MAIL_ADRESS'
garmin_password='GARMIN_PASSWORD'


##### Intervals Settings #####
########   fields - set to blank to not push them to intervals
########   fields must exist as wellness fields (custom or default)
########         example to not check for bpm values:
########           intervals_diastolic_field = ''
########           intervals_systolic_field = ''

intervals_weight_field = '' #weight
intervals_bodyfat_field = '' #bodyFat
intervals_diastolic_field = '' #diastolic
intervals_systolic_field = '' #systolic
intervals_sleepscore_field = '' #sleepScore
intervals_sleepquality_field = '' #sleepQuality
intervals_averageSpO2HRSleep_field = '' #avgSleepingHR
intervals_averageSpO2Value_field = ''# spO2
intervals_restingHeartRate_field = '' #restingHR
intervals_fatigue_field = '' #fatigue
intervals_stress_field = '' #stress
intervals_mood_field = '' #mood
intervals_temperature_field = '' #
## Custom Fields
intervals_steps_field = '' #Customfield (might be Steps)
intervals_sleepTimeseconds_field = '' #Customfield (might be sleepSecs)
intervals_deepSleepSeconds_field = '' #Customfield (might be DeepSleep)
intervals_lightSleepSeconds_field = '' #Customfield (might be LightSleep)
intervals_remSleepSeconds_field = '' #Customfield (might be REMSleep)
intervals_awakeSleepSeconds_field = '' #Customfield (might be AwakeTime)

##### Withing Settings #####
withings_delta = 7 # days in past to update