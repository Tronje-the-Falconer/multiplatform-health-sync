#!/usr/bin/python3
"""
    matlab.com
"""
# import matlab.engine

def runImReady4():
    eng = matlab.engine.start_matlab()
    eng.triarea(nargout=0)
    print('matlab')
    
    
    
    
    
    
    
    
#######
# VERSION 4.40 (22/01/2023)
#######

def ImReady4()
    #Delete already existing figures
    currentVersion = "4.40"
    availabeUpdateExists = searchForAppUpdates(currentVersion)
    fig = get(groot,'CurrentFigure')
    while not(isempty(fig))
        close(fig)
        fig = get(groot,'CurrentFigure')

    #Read athletes credentials for intervals.icu and settings
    settings = readSettings()

    colors = {  [120, 240, 120] / 255
                [230, 230, 230] / 255
                [255, 165, 0] / 255
                [180, 240, 180] / 255
                [220, 220, 220] / 255
                [255, 120, 120] / 255
                [255, 255, 255] / 255
             }

    numAthletes = size(settings.athletes, 1)
    firstAthlete = 1
    lastAthlete = numAthletes
    if (numAthletes > 5)
        option = displayCoachMenu(numAthletes)
        if (option > 0)
            firstAthlete = 5 * option - 4
            lastAthlete = min([firstAthlete + 4 numAthletes])



    print(['Training Advice created on: ' datestr(datetime('now','TimeZone',settings.timeZone))])
    print(" ")

    for j = firstAthlete:lastAthlete
        username = 'API_KEY'
        password = cell2mat(settings.athletes(j,3))
        ID = cell2mat(settings.athletes(j,2))
        name = cell2mat(settings.athletes(j,1))
    
        options = weboptions('HeaderFields',{'Authorization', ['Basic ' matlab.net.base64encode([username ':' password])]})
        formatOut = 'yyyy-mm-dd'
        endDate = datestr(datetime('now','TimeZone',settings.timeZone), formatOut)
        initDate = datestr(datetime('now','TimeZone',settings.timeZone) - 89, formatOut)
        url = 'https://intervals.icu/api/v1/athlete/' + str(ID) + '/wellness.csv?oldest=' + initDate + '&newest=' + endDate + '&cols=' + settings.FIELD_RHR + ',' + settings.FIELD_rMSSD + ',' + settings.FIELD_SDNN
        resp = webread(url, options)
        
        [numDays, ~] = size(resp)

        RHR = resp(:,settings.FIELD_RHR).(1)

        rMSSD = resp(:,settings.FIELD_rMSSD).(1)
        HRV_rMSSD = 20*log(rMSSD)

        SDNN = resp(:,settings.FIELD_SDNN).(1)
        HRV_SDNN = 20*log(SDNN)

        dates = resp(:,"date").date
        n = min([30 numDays])
        scoreHRV_rMSSD = zeros(n,1)
        scoreHRV_SDNN = zeros(n,1)
        scoreRHR = zeros(n,1)
        for i = 1:n
            last = min([numDays (i + 29)])

            m = mean(HRV_rMSSD(i:last), 'omitnan');
            s = std(HRV_rMSSD(i:last),1, 'omitnan');
            scoreHRV_rMSSD(i) = (HRV_rMSSD(i) - m) / s;

            m = mean(HRV_SDNN(i:last), 'omitnan');
            s = std(HRV_SDNN(i:last),1, 'omitnan');
            scoreHRV_SDNN(i) = (HRV_SDNN(i) - m) / s;

            m = mean(RHR(i:last), 'omitnan');
            s = std(RHR(i:last), 1, 'omitnan');
            scoreRHR(i) = (RHR(i) - m) / s;
        end

        score = cell(numDays,1);
        code = zeros(numDays,1);
        h = figure;
        
        sp1 = subplot('position',[0.05 0.50 0.9 0.45]);
        sp2 = subplot('position',[0.1 0.05 0.3 0.40]);
        sp3 = subplot('position',[0.5 0.05 0.45 0.40]);
        
        subplot(sp1)
       % view(0, 60)

        chartBackground(h, settings);
        angLimit = (1.5*pi/2);

        nTrace = min([5 n]);
        
        xx = (-scoreHRV_rMSSD(1:nTrace)+6).*sin(scoreRHR(1:nTrace)/3*angLimit);
        yy = (-scoreHRV_rMSSD(1:nTrace)+6).*cos(scoreRHR(1:nTrace)/3*angLimit);
        %zz = scoreHRV_SDNN(1:nTrace)+6;
        zz = zeros(size(yy));
        plot3(xx, yy, zz,"k--","LineWidth",1)

        for i = n:-1:2
            ms = 4 + (n/i) / 2;
            ic = 0.5 + (i/n)/2;
            icolor = [ic ic ic];

            xx = (-scoreHRV_rMSSD(i)+6)*sin(scoreRHR(i)/3*angLimit);
            yy = (-scoreHRV_rMSSD(i)+6)*cos(scoreRHR(i)/3*angLimit);
            %zz = scoreHRV_SDNN(i)+6;
            zz = zeros(size(yy));

            plot3(xx,yy, zz,"o","MarkerFaceColor",icolor,"MarkerEdgeColor","k","MarkerSize",ms)
            [s, d, c] = getScore(scoreHRV_rMSSD(i), scoreRHR(i));
            score(i,1) = {s};
            code(i) = c;
        end
        xx = (-scoreHRV_rMSSD(1)+6)*sin(scoreRHR(1)/3*angLimit);
        yy = (-scoreHRV_rMSSD(1)+6)*cos(scoreRHR(1)/3*angLimit);
        %zz = scoreHRV_SDNN(1)+6;
        zz = 0;
        plot3([xx xx],[yy yy],[zz 0], "k-")
        plot3(xx,yy, zz, "o","MarkerFaceColor","b","MarkerEdgeColor","w","MarkerSize",14)
        plot3(xx,yy, zz, "o","MarkerFaceColor","w","MarkerEdgeColor","w","MarkerSize", 10)
        plot3(xx,yy, zz, "*","MarkerFaceColor","b","MarkerEdgeColor","b","MarkerSize", 16)

        [s1, d1, c1] = getScore(scoreHRV_rMSSD(1), scoreRHR(1));
        [s2, d2, c2] = getScore(scoreHRV_rMSSD(2), scoreRHR(2));
        [s3, d3, c3] = getScore(scoreHRV_rMSSD(3), scoreRHR(3));

        if (settings.trainingAdviceMustBeSentToIntervals)    
            sendTrainingAdviceToIntervals(endDate, c1, ID, password);
        end
        
        h.NumberTitle = 'off';
        h.Name = sprintf("%s: advice", name);
%         h.ToolBar = 'none';
%         h.MenuBar = 'none';

        try
            fprintf(strcat(name, " --> ", s1, " ", d1{1}, ". ", d1{2}, "\n\n"))
        catch
        end

        drawReady4(h, s1, d1, cell2mat(colors(c1,1)), settings)
        
        if (availabeUpdateExists)
            text(10,12,sprintf("App UPDATE\nAVAILABLE"),'HorizontalAlignment','right','VerticalAlignment',...
                'top','FontSize',8,'FontWeight','bold','FontName','Arial','Color','b')
        end

        subplot(sp2)
        titleStr = sprintf("Yesterday (%s)", settings.yesterdayActivity);
        [t, s] = title(titleStr);
        t.FontName = 'Arial';
        t.FontSize = 10;

        t.FontWeight = 'normal';
        s.FontName = 'Courier';

        options = weboptions('HeaderFields',{'Authorization', ['Basic ' matlab.net.base64encode([username ':' password])]});

        formatOut = 'yyyy-mm-dd';
        endDate = datestr(datetime('now','TimeZone',settings.timeZone), formatOut);
        initDate = datestr(datetime('now','TimeZone',settings.timeZone) - 1, formatOut);

        url = strcat('https://intervals.icu/api/v1/athlete/', string(ID), '/activities?oldest=', initDate, '&newest=', endDate);
        resp = webread(url, options);

        totalDayLoad = calcTotalDayLoad(resp);
        totalDayDuration = calcTotalDayDuration(resp);
        
        if not(isnumeric(resp))
            iActivity = searchActivity(resp, settings.yesterdayActivity);
            if not(isnumeric(resp(iActivity)))
                if (iscell(resp))
                    act_ID = resp{iActivity}.id;
                    TYPE = resp{iActivity}.type;
                    RPE = resp{iActivity}.icu_rpe;
                    INTENSITY = resp{iActivity}.icu_intensity;
                    DURATION = resp{iActivity}.elapsed_time;
                    LOAD = resp{iActivity}.icu_training_load;
                    FEEL = resp{iActivity}.feel;
                    START_TIME = extractTime(resp{iActivity}.start_date_local);
                else
                    act_ID = resp(iActivity).id;
                    TYPE = resp(iActivity).type;
                    RPE = resp(iActivity).icu_rpe;
                    INTENSITY = resp(iActivity).icu_intensity;
                    DURATION = resp(iActivity).elapsed_time;
                    LOAD = resp(iActivity).icu_training_load;
                    FEEL = resp(iActivity).feel;
                    START_TIME = extractTime(resp(iActivity).start_date_local);
                end
            end
        else
            act_ID = [];
            TYPE = "Resting Day";
            RPE = [];
            INTENSITY = [];
            DURATION = [];
            LOAD = [];
            FEEL = [];
            START_TIME = [];
        end
        
        if not(isempty(act_ID))   
            options = weboptions('HeaderFields',{'Authorization', ['Basic ' matlab.net.base64encode([username ':' password])]});
        
            url = strcat('https://intervals.icu/api/v1/activity/', string(act_ID), '/streams{ext}?types=heartrate');

            resp = webread(url, options);
            heartrate = [];
            if not(isempty(resp))
                heartrate = (resp.data);
            end
            url = strcat('https://intervals.icu/api/v1/activity/', string(act_ID), '/streams{ext}?types=watts');

            resp = webread(url, options);
            power = [];
            if not(isempty(resp))
                power = (resp.data);
            end
            
            subplot(sp2)
            labelFontSize = 10;
            if strcmp(settings.fontSizeForAdvice, 'medium')
                labelFontSize = 8;
            elseif strcmp(settings.fontSizeForAdvice, 'small')
                labelFontSize = 8;
            end

            xlabel('Time (min)', 'FontSize', labelFontSize)
            hold on;
            timeHR = [0:length(heartrate)-1]' / 60;
            timePWR = [0:length(power)-1]' / 60;
            timeEnd = max([length(heartrate)-1 length(power)-1 60])/60;
            axis([0 timeEnd 0 inf]);
            yyaxis(sp2, 'left')
            ylabel('Power (w)', 'Color', [0 0.4470 0.7410], 'FontSize', labelFontSize)
            set(gca,'ycolor',[0 0.4470 0.7410]);        
            s = scatter(timePWR, power, 5, [0 0.4470 0.7410], 'filled');
            alpha(s, 0.2);
            plot(timePWR, movmean(power, 30),'-', 'Color', [0 0.4470 0.7410],'LineWidth', 0.75)
            yyaxis(sp2, 'right')
            ylabel('Heart rate (bpm)','Color',[0.6350 0.0780 0.1840], 'FontSize', labelFontSize)
            set(gca,'ycolor',[0.6350 0.0780 0.1840]);
            plot(timeHR,(heartrate),'Color',[0.6350 0.0780 0.1840])
        end
        subplot(sp3)
       
        axis('off')
        hold on
        axis([0 100 0 100])
        rectangle("position",[0 0 100 100],"EdgeColor","k","FaceColor",[250 250 250]/255)
        cfontName = 'Arial';
        cfontSize = 12;
        vfontName = 'Courier';
        vfontSize = 12;
        if strcmp(settings.fontSizeForAdvice, 'medium')
            cfontSize = 10;
            vfontSize = 10;
        elseif strcmp(settings.fontSizeForAdvice, 'small')
            cfontSize = 8;
            vfontSize = 8;
        end
        xPosLabel = 5;
        xPosVal = 40;
        yPosIni = 95;
        nLines = 7;
        pitch = -8;
        yPos = yPosIni:pitch:yPosIni+nLines*pitch;
        text(xPosLabel, yPos(1),'Type:','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        text(xPosVal, yPos(1),TYPE,'FontSize',vfontSize-2,'FontName',vfontName)
        
        text(xPosLabel, yPos(2),'Time:','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        if isempty(DURATION)
            text(xPosVal, yPos(2),"--",'FontSize',vfontSize,'FontName',vfontName);
        else  
            text(xPosVal, yPos(2),START_TIME,'FontSize',vfontSize,'FontName',vfontName);
        end
        
        text(xPosLabel, yPos(3),'Duration:','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        if isempty(DURATION)
            text(xPosVal, yPos(3),"--",'FontSize',vfontSize,'FontName',vfontName);
        else  
            durationStr = sprintf("%s min (%s)", string(round(DURATION/60)), string(round(totalDayDuration/60)));
            text(xPosVal, yPos(3),durationStr,'FontSize',vfontSize,'FontName',vfontName);
        end

        text(xPosLabel, yPos(4),'Load:','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        if isempty(LOAD)
            text(xPosVal, yPos(4),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(xPosVal, yPos(4),sprintf("%s (%s)", string(LOAD), string(totalDayLoad)),'FontSize',vfontSize,'FontName',vfontName)
        end

        text(xPosLabel, yPos(5),'IF:','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        if isempty(INTENSITY)
            text(xPosVal, yPos(5),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(xPosVal, yPos(5),string(round(INTENSITY)),'FontSize',vfontSize,'FontName',vfontName)
        end

        text(xPosLabel, yPos(6),'RPE:','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        if isempty(RPE)
            text(xPosVal, yPos(6),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(xPosVal, yPos(6),string(RPE),'FontSize',vfontSize,'FontName',vfontName)
        end

        text(xPosLabel, yPos(7),'FEEL:','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        if isempty(FEEL)
            text(xPosVal, yPos(7),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(xPosVal, yPos(7),string(FEEL),'FontSize',vfontSize,'FontName',vfontName)
        end

        colfontSize = 10;

        yPosIni2 = 35;
        nLines = 4;
        pitch2 = pitch;
        yPos2 = yPosIni2:pitch2:yPosIni2+nLines*pitch2;

        text(35, yPos2(1),'Today','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        text(60, yPos2(1),'Yesterday','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        text(xPosLabel, yPos2(2),'rMSSD','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        text(xPosLabel, yPos2(3),'SDNN','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        text(xPosLabel, yPos2(4),'RHR','FontSize',cfontSize,'FontName',cfontName,'FontWeight','bold')
        plot([0 100],[1 1]*mean([yPos(6) yPos2(1)]),'w');

        if isnan(rMSSD(1))
            text(40, yPos2(2),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(40, yPos2(2),string(round(rMSSD(1))),'FontSize',vfontSize,'FontName',vfontName)
        end
        
        if isnan(SDNN(1))
            text(40, yPos2(3),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(40, yPos2(3),string(round(SDNN(1))),'FontSize',vfontSize,'FontName',vfontName)
        end

        if isnan(RHR(1))
            text(40, yPos2(4),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(40, yPos2(4),string(round(RHR(1))),'FontSize',vfontSize,'FontName',vfontName)
        end
        
        if isnan(rMSSD(2))
            text(70, yPos2(2),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(70, yPos2(2),string(round(rMSSD(2))),'FontSize',vfontSize,'FontName',vfontName)
        end

        if isnan(SDNN(2))
            text(70, yPos2(3),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(70, yPos2(3),string(round(SDNN(2))),'FontSize',vfontSize,'FontName',vfontName)
        
        end
        
        if isnan(RHR(2))
            text(70, yPos2(4),"--",'FontSize',vfontSize,'FontName',vfontName)
        else
            text(70, yPos2(4),string(round(RHR(2))),'FontSize',vfontSize,'FontName',vfontName)
        end

        hfigTrends = figure;
%         hfigTrends.ToolBar = 'none';
%         hfigTrends.MenuBar = 'none';
        hfigTrends.NumberTitle = 'off';
        hfigTrends.Name = sprintf("%s: trends", name);

        plotTrends(rMSSD, SDNN, RHR, settings)
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
        detail = [{"Low intensity training"};{}];
        code = 2;
    elseif (scoreRHR <= -2 && scoreHRV >= 0)
        score = "LIT!";
        detail = [{"Keep calm!"};{"Acute fatigue signs"}];
        code = 3;
    elseif (scoreRHR < 1.7 && scoreHRV >= -1)
        score = "Normal";
        detail = [{"Go on!"};{"Train as planned."}];
        code = 4;
    elseif (scoreHRV >= -1)
        score = "LIT";
        detail = [{"Low intensity training"};{}];
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

function chartBackground(h, settings)
    axis('off')
    hold on
    
    drawZone(-3, 3, 3, -3, [220 220 220]/255,-0.02)
    drawZone(1.7, 3, -1, -3, [255 0 0]/255,0)
    drawZone(-2, 1.7, -1, -3, [255 165 0]/255,0)
    drawZone(-3, -2, 3, 0, [255 165 0]/255,0)
    drawZone(-2, 1.7, 3, -1, [200 255 200]/255,-0.01)
    drawZone(-1, 1, 3, 1, [0 255 0]/255,0)
    drawZone(-3, -2, -1, -3, [160 160 160]/255,0)
    drawGrid(settings)
    
end

function drawReady4(h, text1, text2, color, settings)
    p = nsidedpoly(100, 'Center', [0 0], 'Radius', 2);
    fill(p.Vertices(:,1),p.Vertices(:,2), color,'EdgeColor',color)
    alertFontSize = 14;
    adviceFontSize = 12;
    if strcmp(settings.fontSizeForAdvice, 'medium')
        alertFontSize = 12;
        adviceFontSize = 10;
    elseif strcmp(settings.fontSizeForAdvice, 'small')
        alertFontSize = 10;
        adviceFontSize = 8;
    end
    text(0,0,text1,'HorizontalAlignment','center','VerticalAlignment','middle','FontSize',alertFontSize,'FontWeight','bold')
    text(0,-4.5,text2,'HorizontalAlignment','center','VerticalAlignment','middle','FontSize',adviceFontSize,'FontWeight','normal')

end

function drawZone(xL, xR, yB, yU, color,deep)
    angLimit = (1.5*pi/2);

    x1 = [xL:0.1:xR];
    y1 = ones(size(x1))*yB;
    
    y2 = [yB:-0.1:yU];
    x2 = ones(size(y2))*xR;
    
    x3 = [xR:-0.1:xL];
    y3 = ones(size(x3))*yU;
    
    y4 = [yU:0.1:yB];
    x4 = ones(size(y4))*xL;
    
    x = [x1 x2 x3 x4]'/3*angLimit;
    y = -[y1 y2 y3 y4]' + 6;

    
    xx = y.*sin(x);
    yy = y.*cos(x);

    zz = xx * 0 + deep;
    
    fill3(xx, yy, zz, color,'EdgeColor',color)

end

function drawGrid(settings)
   angLimit = (1.5*pi/2);

   gridColor = [100 100 100]/255;
   y = [3.5 -3.2]' + 6;
   yLab1 = y(1) * 1.04;
   yLab2 = y(2) * 0.90;
   labelFontSize = 8;
   if strcmp(settings.fontSizeForAdvice, 'medium')
       labelFontSize = 8;
   elseif strcmp(settings.fontSizeForAdvice, 'small')
        labelFontSize = 7;
   end

   lw = [1.0 0.75 0.75 1.0 0.75 0.75 1.0];
   ls = {'-', '--', '--', '-','--', '--', '-'};
   for i=-3:3 
        x = i * [1 1]'/3*angLimit;
        xx = y.*sin(x);
        yy = y.*cos(x);
        zz = yy * 0 + 0.01;
        plot3(xx, yy, zz, 'color',gridColor, 'LineWidth', lw(i+4), 'LineStyle', ls(i+4))
        
        xxLab = yLab1*sin(x(1));
        yyLab = yLab1*cos(x(1));
        text(xxLab, yyLab, string(i), 'fontname', 'courier', ...
            'FontSize',labelFontSize,'HorizontalAlignment','center');
        xxLab = yLab2*sin(x(1));
        yyLab = yLab2*cos(x(1));
        text(xxLab, yyLab, string(i), 'fontname', 'courier', ...
            'FontSize',labelFontSize,'HorizontalAlignment','center');

   end

   for r=-3:3
       rr = r + 6;
       xx = rr * sin(angLimit*[-1:0.01:1]);
       yy = rr * cos(angLimit*[-1:0.01:1]);
       zz = yy * 0 + 0.01;
       plot3(xx, yy, zz, 'color',gridColor, 'LineWidth', lw(r+4), 'LineStyle', ls(r+4))
   end
end

function hhmm = extractTime(timeStamp)
    pat = 'T' + digitsPattern(2) + ':' + digitsPattern(2);
    hhmmss = extract(timeStamp, pat);
    pat = digitsPattern(2) + ':' + digitsPattern(2);
    hhmm = extract(timeStamp, pat);
end

function iActivity = searchActivity(activities, yesterdayActivity)
    iActivity = 1; %Last or resting day
    switch yesterdayActivity
        case 'Last'
            iActivity = 1;
        case 'Longest'
            maxDuration = 0;
            iActivity = 1;
            for i=1:size(activities,1)
                if (iscell(activities))
                    iDuration = activities{i}.icu_elapsed_time;
                else
                    iDuration = activities(i).icu_elapsed_time;
                end

                if iDuration >= maxDuration
                    maxDuration = iDuration;
                    iActivity = i;
                end
            end
        case 'HighestLoad'
            maxLoad = 0;
            iActivity = 1;
            for i=1:size(activities,1)
                if (iscell(activities))
                    iLoad = activities{i}.icu_training_load;
                else
                    iLoad = activities(i).icu_training_load;
                end
                if iLoad >= maxLoad
                    maxLoad = iLoad;
                    iActivity = i;
                end
            end
        otherwise
            iActivity = 1;
    end
end

function updateIsAvailable = searchForAppUpdates(currentVersion)
    ID = '1FR4DyZkmjVubBHEegcC7COnYoR8RLV8CHpykLGc4DTU';

    sheet_name = 'Version';
    url_name = sprintf('https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=%s', ID, sheet_name);
    updateIsAvailable = false;
    try
        sheet_data = webread(url_name);
        mostRecentVersion = sprintf("%0.2f",sheet_data.Version(1,:)/100);
        configUpdateRequired = sheet_data.ConfigUpdateRequired(1,:);
        updateIsAvailable = not(strcmp(currentVersion, mostRecentVersion));
        if (updateIsAvailable)
            msg = sprintf(  "You are using an outdated version (%s)\n" + ...
                            "Version (%s) is available.\nUse following link" + ...
                            " to update and click on <Add to my files>.",...
                            currentVersion, mostRecentVersion);
            disp(msg) 
            %disp('<a href = "https://drive.matlab.com/sharing/b5ba9fea-3099-40d9-9d74-14cf9cb55911">ImReady4 (update)</a>')
            disp("https://drive.matlab.com/sharing/b5ba9fea-3099-40d9-9d74-14cf9cb55911")
            disp(" ")
        end
        if (configUpdateRequired)
            msg = sprintf(  "Version (%s) requires updated configuration\n" + ...
                            "See config_athletes_template.m in ImReady4\\Template folder and copy new settings to your config_athletes.m script\n",...
                            mostRecentVersion);
            disp(msg)
        end
    catch

    end
end

function totalDayLoad = calcTotalDayLoad(activities)
    totalDayLoad = 0;
    if not(isnumeric(activities))
        for i=1:size(activities,1)
            
            if (iscell(activities))
                iLoad = activities{i}.icu_training_load;
            else
                iLoad = activities(i).icu_training_load;
            end

            if not(isnan(iLoad))
                totalDayLoad = totalDayLoad + iLoad;
            end
        end
    end
end

function totalDayDuration = calcTotalDayDuration(activities)
    totalDayDuration = 0;
    if not(isnumeric(activities))
        for i=1:size(activities,1)
            if (iscell(activities))
                iDuration = activities{i}.elapsed_time;
            else
                iDuration = activities(i).elapsed_time;
            end

            if not(isnan(iDuration))
                totalDayDuration = totalDayDuration + iDuration;
            end
        end
    end
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
    catch

    end
end

function plotTrends(rMSSD, SDNN, RHR,settings)
    labelFontSize = 10;
    if strcmp(settings.fontSizeForAdvice, 'medium')
        labelFontSize = 8;
    elseif strcmp(settings.fontSizeForAdvice, 'small')
        labelFontSize = 8;
    end

    p = subplot(3,1,1);
    ylabel('rMSSD', 'FontSize', labelFontSize)
    xlabel('day', 'FontSize', labelFontSize)
    plotTrendx(p, rMSSD, 30, settings)

    p = subplot(3,1,2);
    ylabel('SDNN', 'FontSize', labelFontSize)
    xlabel('day', 'FontSize', labelFontSize)
    plotTrendx(p, SDNN, 30, settings)

    p = subplot(3,1,3);
    ylabel('rHR', 'FontSize', labelFontSize)
    xlabel('day', 'FontSize', labelFontSize)
    plotTrendx(p, RHR, 30, settings)
end

function plotTrendx(p, yy, nDays, settings)
    labelFontSize = 9;
    if strcmp(settings.fontSizeForAdvice, 'medium')
        labelFontSize = 8;
    elseif strcmp(settings.fontSizeForAdvice, 'small')
        labelFontSize = 8;
    end

    subplot(p);
    p.YGrid = 'on';
    p.YMinorGrid = 'on';
    p.Box = 'on';
    hold on
    y = flip(yy)';
    x = -length(y) + 1:0;
    showValues = settings.showValuesInTrendCharts;
    shortTermDays = settings.daysForShortTermTrend;
    longTermDays = settings.daysForLongTermTrend;
    xStd = settings.multiplier_X_StdDev_ForLongTermTrendRange;

    trend = movmean(y,[longTermDays-1 0],'omitnan');
    std = movstd(y,[longTermDays-1 0],1,'omitnan');
    lowerLimit = trend - xStd * std;
    upperLimit = trend + xStd * std;
    ymin = 10*floor((min(y(end - nDays + 1:end)-2)/10));
    ymin = max(ymin,0);
    ymax = 10*ceil((max(y(end - nDays + 1:end)+1)/10));
    if ymax <= ymin
        ymax = ymin+1;
    end
    if not(isnan(ymax*ymin)) 
        p.YLim = [ymin ymax];
    end

    a = patch([x(end - nDays + 1:end) fliplr(x(end - nDays + 1:end))], [lowerLimit(end - nDays + 1:end) fliplr(upperLimit(end - nDays + 1:end))],...
        'y', 'facealpha',0.5,'edgecolor','y');

    shortTermTrend = movmean(y,[shortTermDays-1 0],'omitnan');

    plot(x(end - nDays + 1:end),shortTermTrend(end - nDays + 1:end),'k--','LineWidth',1)

    b = bar(x(end - nDays + 1:end),y(end - nDays + 1:end));
    b.FaceColor = 'flat';
    b.FaceAlpha = 0.2;
    
    plot(x(end - nDays + 1:end),lowerLimit(end - nDays + 1:end),'y')
    plot(x(end - nDays + 1:end),upperLimit(end - nDays + 1:end),'y')
    y=round(y);
    if (showValues)
        text([-nDays+1:0], y(end - nDays + 1:end)', num2str(y(end - nDays + 1:end)','%d'),...
            'HorizontalAlignment','center','VerticalAlignment','bottom','FontName','courier','FontSize',labelFontSize);
    end
    for i=nDays:-1:1
        if y(end-i+1) > upperLimit(end-i+1) || y(end-i+1) < lowerLimit(end-i+1)
            b.CData(nDays - i + 1,:) = [1 0 0];
        else
            b.CData(nDays - i + 1,:) = [0 1 0];
        end
    end   
end

function option = displayCoachMenu(numAthletes)
    disp("");
    disp("Athletes to be evaluated:")
    disp("   (0) all");
    menuOptions = ceil(numAthletes / 5);
    for i = 1:menuOptions-1
        menuOptionstring = sprintf("   (%d) from %d to %d",i,i*5-4,i*5);
        disp(menuOptionstring);
    end
    menuOptionstring = sprintf("   (%d) from %d to %d",menuOptions,menuOptions*5-4,numAthletes);
    disp(menuOptionstring);

    option = input("\nSelect an option: ");
    if not(isnumeric(option))
        option = 0;
    elseif (option < 0)
        option = 0;
    elseif (option > menuOptions)
        option = 0;
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

    fontSizeForAdvice = 'normal';
    fontSizeForSummaryPanel = 'normal';

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
    settings.fontSizeForAdvice = fontSizeForAdvice;
    settings.fontSizeForSummaryPanel = fontSizeForSummaryPanel;

    cd(oldPath);
end