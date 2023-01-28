%%%%%%%
% VERSION 2.10 (02/01/2023)
%%%%%%%


function PopulateImReady4()

    currentVersion = "2.10";

    %Read athletes credentials for intervals.icu
    settings = readSettings();
    
    numAthletes = size(settings.athletes, 1);
    firstAthlete = 1;
    lastAthlete = numAthletes;
    days = displayMenu();
    
    if (days ~= 0)
        disp(['Populating training advice since:  ' datestr(datetime('now','TimeZone',settings.timeZone)-days+1,"yyyy-mm-dd")]);
        disp(" ");
        for j = firstAthlete:lastAthlete
            username = 'API_KEY';
            password = cell2mat(settings.athletes(j,3));
            ID = cell2mat(settings.athletes(j,2));
            name = cell2mat(settings.athletes(j,1));
        
            options = weboptions('HeaderFields',{'Authorization', ['Basic ' matlab.net.base64encode([username ':' password])]});
            formatOut = 'yyyy-mm-dd';
            endDate = datestr(datetime('now','TimeZone',settings.timeZone), formatOut);
            initDate = datestr(datetime('now','TimeZone',settings.timeZone) - (days + 30), formatOut);
            url = strcat('https://intervals.icu/api/v1/athlete/', string(ID),...
                        '/wellness.csv?oldest=', initDate, '&newest=', endDate,...
                        '&cols=',settings.FIELD_RHR,',',settings.FIELD_rMSSD,',',settings.FIELD_SDNN);
            resp = webread(url, options);
            
            [numDays, ~] = size(resp);

            RHR = resp(:,settings.FIELD_RHR).(1);
            rMSSD = resp(:,settings.FIELD_rMSSD).(1);
            HRV_rMSSD = 20*log(rMSSD);
        
            SDNN = resp(:,settings.FIELD_SDNN).(1);
            HRV_SDNN = 20*log(SDNN);
    
            dates = resp(:,"date").date;
            n = min([10000 numDays]);
            scoreHRV = zeros(n,1);
            scoreRHR = zeros(n,1);
            for i = 1:days
                last = min([numDays (i + 29)]);
                m = mean(HRV_rMSSD(i:last), 'omitnan');
                s = std(HRV_rMSSD(i:last),1, 'omitnan');
                scoreHRV(i) = (HRV_rMSSD(i) - m) / s;
                m = mean(RHR(i:last), 'omitnan');
                s = std(RHR(i:last), 1, 'omitnan');
                scoreRHR(i) = (RHR(i) - m) / s;
            end
            for i = days:-1:1
                [s, d, c] = getScore(scoreHRV(i), scoreRHR(i));
                if (settings.trainingAdviceMustBeSentToIntervals)
                    formatOut = 'yyyy-mm-dd';
                    iDateStr = datestr(dates(i), formatOut);
                    sendTrainingAdviceToIntervals(iDateStr, c, ID, password);
                end
            end
        end
    else
        disp("Training Advice populated for 0 days")
    end
end

function [score, detail, code] = getScore(scoreHRV, scoreRHR)
    if isnan(scoreRHR) || isnan(scoreHRV)
        score = "...?";
        detail = [{"No HRV data Today"};{"Take a measurement."}];
        code = 7;   
    elseif (scoreRHR <= 1) && (scoreRHR > -1) && (scoreHRV > 1)
        score = "HIT";
        detail = [{"Ready for"};{"Intensive Training"}];
        code = 1;
    elseif (scoreRHR <= -2 && scoreHRV >= -1 && scoreHRV < 0)
        score = "LIT";
        detail = "Low intensity training";
        code = 2;
    elseif (scoreRHR <= -2 && scoreHRV >= 0)
        score = "LIT!";
        detail = [{"Keep calm!"};{"Accute fatigue signs"}];
        code = 3;
    elseif (scoreRHR < 1.7 && scoreHRV >= -1)
        score = "Normal";
        detail = [{"Go on!"};{"Train as planned."}];
        code = 4;
    elseif (scoreHRV >= -1)
        score = "LIT";
        detail = "Low intensity training";
        code = 2;
    elseif (scoreRHR <= -2)
        score = "Rest";
        detail = [{"Time to recover"};{"Avoid overtraining"}];
        code = 5;
    elseif (scoreRHR <= 1.7)
        score = "LIT";
        detail = [{"Low intensity training"};{"Recovery is not complete"}];
        code = 3;
    else
        score = "REST!";
        detail = [{"Be careful!"};{"Illness or stress detected"}];
        code = 6;
    end

end

function settings = readSettings()
    oldPath = cd;
    currentFile = mfilename( 'fullpath' );
    [pathstr,~,~] = fileparts( currentFile );
    cd(pathstr);
    newRelPath = strcat('..', filesep, 'ImReady4_data');
    cd(newRelPath);
    dataPath = cd;
    data = fullfile( dataPath, 'config_athletes.m' ); 
    
    myTimeZone = 'local';
    athletes = [];
    yesterdayActivity = 'Last';
    trainingAdviceMustBeSentToIntervals = false;
    
    daysForShortTermTrend = 7;
    daysForLongTermTrend = 60;
    multiplier_X_StdDev_ForLongTermTrendRange = 0.75;
    
    showValuesInTrendCharts = true;
    FIELD_rMSSD = "hrv";
    FIELD_SDNN = "hrvSDNN";
    FIELD_RHR = "restingHR";

    run(data);
    
    settings.athletes = athletes;
    settings.timeZone = myTimeZone;
    settings.yesterdayActivity = yesterdayActivity;
    settings.trainingAdviceMustBeSentToIntervals = trainingAdviceMustBeSentToIntervals;

    settings.FIELD_rMSSD = FIELD_rMSSD;
    settings.FIELD_SDNN = FIELD_SDNN;
    settings.FIELD_RHR = FIELD_RHR;
   
    settings.showValuesInTrendCharts = showValuesInTrendCharts;
    settings.daysForShortTermTrend = daysForShortTermTrend;
    settings.daysForLongTermTrend = daysForLongTermTrend;
    settings.multiplier_X_StdDev_ForLongTermTrendRange = multiplier_X_StdDev_ForLongTermTrendRange;

    cd(oldPath);
end
function response = sendTrainingAdviceToIntervals(date, code, ID, password)
    switch code
        case 1
            adviceCode = 4;
        case 2
            adviceCode = 2;
        case 3
            adviceCode = 2;
        case 4
            adviceCode = 3;
        case 5
            adviceCode = 1;
        case 6
            adviceCode = 1;
        case 7
            adviceCode = '';
        otherwise
            adviceCode = '';
    end

    try
        url = strcat('https://intervals.icu/api/v1/athlete/', string(ID), '/wellness/', date);
        username = 'API_KEY';
        body = struct('TrainingAdvice', adviceCode);
        options = weboptions(...
            'RequestMethod', 'put',...
            'MediaType', 'application/json',...
            'HeaderFields', {
                'accept', '*/*',
                'Authorization', ['Basic ' matlab.net.base64encode([username ':' password])]
            }...
        );
        response = webwrite(url, body, options);
        s = sprintf("%s -- Training Advice: %d", date, adviceCode);
        disp(s)
    catch
        s = sprintf("%s -- ERROR sending Training Advice", date);
        disp(s)
    end
end

function days = displayMenu()
    days = input("\nEnter number of days to be populated:  ");
    if not(isnumeric(days))
        days = 0;
        disp("Enter a correct number")
    elseif (days < 0)
        days = 0;
        disp("Enter a correct number")
    end

end
