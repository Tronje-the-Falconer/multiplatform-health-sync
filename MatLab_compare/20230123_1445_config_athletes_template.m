%%%% ATHLETES CONFIGURATION
%You can set as many athletes as you want
%Use  ONE line for each athlete. Remove lines that are not required
%   Name = whatever name you want to be displayed by the app for each athlete
%   ID = athlete's ID from intervals.icu account
%   APIKey = athlete's APIKey from intervals.icu account

athletes =   {
                 'Name_1', 'ID_1', 'APIKey_1';
                 'Name_2', 'ID_2', 'APIKey_2';
                 'Name_3', 'ID_3', 'APIKey_3'
              };

%%%% SETTINGS

myTimeZone = '+01:00'; %use following format to set your Time Zone info '+HH:MM' or '-HH:MM'

yesterdayActivity = 'HighestLoad'; %use one of the following options 'Last', 'Longest', 'HighestLoad'

trainingAdviceMustBeSentToIntervals = false; % set to true if you want to overwrite the "Training Advice" wellness custom field

%%%% NEW SETTINGS
daysForShortTermTrend = 7; %enter a positive integer representing num days
daysForLongTermTrend = 60; %enter a positive integer representing num days
multiplier_X_StdDev_ForLongTermTrendRange = 0.75; %enter a positive value representing num days

showValuesInTrendCharts = true; % set to true/false if you want/don't want values in trend charts

FIELD_rMSSD = "hrv"; % modify only in case you want to pull the value from a custom field
FIELD_SDNN = "hrvSDNN"; % modify only in case you want to pull the value from a custom field
FIELD_RHR = "restingHR"; % modify only in case you want to pull the value from a custom field

fontSizeForAdvice = 'normal'; % 'normal' 'medium' 'small' modify in case that you find any issue related to font size
fontSizeForSummaryPanel = 'normal'; % 'normal' 'medium' 'small' modify in case that you find any issue related to font size
