clear all
clc

tic
%# read the whole file to a temporary cell array
%%fid = fopen('Patient110_D2.txt');
%path(path,'D:\MV\Data Archive\CURE Trials\Patient 9 - M-waves\2014.04.08\2014.04.08')
fid = fopen('D:\MV\Data Archive\CURE RCT\Right\MBV001\2016.07.18\RMs\RM-8.15.56.551.txt');

%% 
% mode =1 for Raw file
% mode =2 for RM/PUMP files
mode = 1 
if mode==1
    tmp = textscan(fid,'%s','Delimiter','');
else
    tmp = textscan(fid,'%s','HeaderLines',17,'Delimiter','');
end
fclose(fid);
Input = tmp{1,1};
%% 
if size(Input,1) >20000 %% For parallel computing

    %% When Parallel local Computing is available
    parfor i = 1:size(Input,1)
        try
            Column= strsplit(Input{i,1}, ',');
            Data(i,:) = str2num([Column{1,1} Column{1,2}]);
        catch
        end
    end
else

    %% Use for shorter data
    for i = 1:size(Input,1)
        try
            Column= strsplit(Input{i,1}, ',');
            Data(i,:) = str2num([Column{1,1} Column{1,2}]);
        catch
        end
    end

end
BreathID = find(Data(:,1)==0);

Breath_No =1;
for n = 2:size(BreathID,1)
    if  BreathID(n-1) == BreathID(n)-1
        BS(Breath_No) = BreathID(n)+1;
        BS = BS(find(BS));
    else
        BE(Breath_No) = BreathID(n)-1;
        BE = BE(find(BE));
    end
    Breath_No = Breath_No +1;
end

%% Non Plausible Pressure and Flow data filtering
Data(find(Data(:,2)==0),:) =NaN;
Data(find(Data(:,2)>65),:) =NaN;
Data(find(Data(:,2)<0),:) =NaN;
Data(find(Data(:,1)>150),:) =NaN;
Data(find(Data(:,1)<-150),:) =NaN;

CURE_BSeparation;

%%CURE_Models;

%%CURE_BPlots;

toc
