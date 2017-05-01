clear all
clc
close all;

%% parameters
ncho=0.01; %percent of top hashtag in saveHT for getting Amatrix
mlw=5; %max line width
sizpnt=0.2; %size of points
lsize=15;  %output size limit for plots
file='2016-11-08';
%N_h : number of unique hashtag

%% data analysis
%(hashtag,# of tweet)   %(hashtagroup,# of tweet)
load(strcat(file,'.mat'));

%savedata=savedata2;                     %for daytime and night
%clear savedata2;

j=1; %for hashtagroup
k=1; %for hashtag
for i=1:size(savedata,2)
%hashtagnum(time, weekday, fav, re)   %hashtagdate
%time transfer + hashtagnum matrix
%time_unix = str2num(savedata{i}.timestamp_ms); % example time
%time_reference = datenum('1970', 'yyyy'); 
%time_matlab = time_reference + time_unix / 8.64e7;
%time_matlab_string = datestr(time_matlab, 'yyyymmdd HH:MM:SS.FFF');
%time_matlab_string2 = datestr(time_matlab, 'yyyy-mm-dd');
%
%hashtagnum(i,1)=i;
%hashtagnum(i,2)=time_matlab;
%hashtagnum(i,3)=weekday(time_matlab_string2);
%hashtagnum(i,4)=savedata{i}.favorite_count;
%hashtagnum(i,5)=savedata{i}.retweet_count;
%
%hashtag & hashtagroup matrix
if size(savedata{i}.hashtags,2)>1
    hashtagroup{j,1}=savedata{i}.hashtags;
    hashtagroup{j,2}=i;
    for l=1:size(hashtagroup{j},2)
        hashtag(k,1)=cellstr(hashtagroup{j,1}{1,l});
        hashtag(k,2)=cellstr(num2str(i));
        k=k+1;
    end
    j=j+1;
else
    hashtag(k,1)=savedata{i}.hashtags;
    hashtag(k,2)=cellstr(num2str(i));
    k=k+1;
end
end
% sort and count hashtag
%hashtag=sortrows(hashtag);
[uniqueHT, ~, j]=unique(hashtag(:,1));
count = histc(j, 1:numel(uniqueHT));
for i=1:size(count,1)
    saveHT{i,1}=uniqueHT{i};
    saveHT{i,2}=count(i);
end
saveHT=sortrows(saveHT,-2);

%% hashtag group
i=round(size(saveHT,1)*ncho);
Amtr=zeros(i);
for j=1:size(hashtagroup,1)
    j
    m=1;
    l=0;
    for k=1:size(hashtagroup{j,1},2)
    n=find(ismember(saveHT(:,1),hashtagroup{j,1}{k}));
    if n<=i
        l(m)=n;
        m=m+1;        
    end
    end
% write A matrix
    k=size(l,2);
    for m=1:k
    for n=1:k
        if m~=n
        Amtr(l(m),l(n))=Amtr(l(m),l(n))+1;
        end
    end
    end
end
%rule out double mentioned hashtag
for j=1:size(Amtr,1)
    Amtr(j,j)=0;
end
%coweight list
[j,k]=sort(Amtr(:),'descend');
for l=1:1000
    [m,n]=ind2sub([i,i],k(2*l-1));
    conweight{l,1}=saveHT(m,1);
    conweight{l,2}=saveHT(n,1);
    conweight{l,3}=Amtr(m,n);
end

%% distribution of size of hashtags
j=unique(count);
dis = [j histc(count(:),j)];
dis = sortrows(dis,-1);
dis(:,3)=cumsum(dis(:,2)); %CCDF

loglog(dis(:,1),dis(:,2),'b*','MarkerSize',5,'LineWidth',2)
xlabel('word frequency k');
ylabel('Number of group N_k');
title(strcat('Distribution of hashtags N_h=',num2str(size(saveHT,1))))
set(gca,'fontname','Arial','fontsize',12,'fontweight','bold');
set(gcf,'position',[100,100,600,600]);
print(1,'-dbitmap',strcat(file,'dis-fre-hashtag','.jpg'));
%legend('well location','compute domain','building area','location','northeast');
%legend('boxoff');

%CCDF
i=log10(dis(:,1));
j=log10(dis(:,3));
coef=polyfit(i,j,1);
k=polyval(coef,i);
%R^2 error
%yres=j-k;
%SSres=sum(yres.^2);
%SStot=std(j)^2*(size(j,1)-1);
%Rr=1-SSres/SStot
gamma=1-coef(1);
dis(:,4)=10.^(k);
loglog(dis(:,1),dis(:,3),'b*',dis(:,1),dis(:,4),'r-','MarkerSize',5,'LineWidth',2);
i=['log(y)=',num2str(coef(1)),'log(x)+',num2str(coef(2))];
legend('CCDF data',i,'location','northeast');
legend('boxoff');
xlabel('Word frequency k');
ylabel('CCDF of N_k');
title(strcat('CCDF of distribution of hashtags N_h=',num2str(size(saveHT,1)),', gamma=',num2str(gamma)));
set(gca,'fontname','Arial','fontsize',12,'fontweight','bold');
set(gcf,'position',[100,100,600,600]);
print(1,'-dbitmap',strcat(file,'dis-CCDF-hashtag','.jpg'));

%zipf
dis=sortrows(dis,-1);
dis(:,5)=[1:size(dis,1)];   %rank
dis=dis(1:350,:); % opition
i=log10(dis(:,5));
j=log10(dis(:,1));
coef=polyfit(i,j,1);
k=polyval(coef,i);
alpha=-coef(1);
dis(:,6)=10.^(k);
loglog(dis(:,5),dis(:,1),'b*',dis(:,5),dis(:,6),'r-','MarkerSize',5,'LineWidth',2);
i=['log(y)=',num2str(coef(1)),'log(x)+',num2str(coef(2))];
legend('rank data',i,'location','northeast');
legend('boxoff');
xlabel('group rank r');
ylabel('group size');
title(strcat('Zipf of hashtags N_h=',num2str(size(saveHT,1)),', alpha=',num2str(alpha)));
set(gca,'fontname','Arial','fontsize',12,'fontweight','bold');
set(gcf,'position',[100,100,600,600]);
print(1,'-dbitmap',strcat(file,'dis-Zipf-hashtag','.jpg'));

%% A matrix plot
i=round(size(saveHT,1)*ncho);
%j=size(hashtagroup);
gra=graph(Amtr,saveHT(1:i,1));

% weight of connection
j=sort(gra.Edges.Weight,'descend');
k=j(1)/mlw;
l=median(j)/5/k;
colormap hot
plot(gra,'NodeColor','b','EdgeCData',gra.Edges.Weight/k,'LineWidth',gra.Edges.Weight/k);
colorbar
caxis([l mlw+0.1])
m=['Hashtag network : Weightings of connections (N_h=',num2str(size(Amtr,1)),')'];
title(m)
set(gca,'fontname','Arial','fontsize',12,'fontweight','bold');
set(gcf,'position',[100,100,800,800]);
xlim([0 lsize]);
ylim([0 lsize]);
axis off;
print(1,'-dbitmap',strcat(file,'weicon','.jpg'));

%for j=1:size(gra.Edges.Weight,1)
%    j
%    conweight{j,1}=gra.Edges.EndNodes(j,1);
%    conweight{j,2}=gra.Edges.EndNodes(j,2);
%    conweight{j,3}=gra.Edges.Weight(j);
%end
%conweight=sortrows(conweight,-3);

% degree of connection of every hashtag
deg = degree(gra);
for j=1:size(deg,1)
    nodegree{j,1}=saveHT(j,1);
    nodegree{j,2}=deg(j);
end
nodegree=sortrows(nodegree,-2);

colormap hot
j = sizpnt*sqrt(deg-min(deg)+0.2);
k = deg;
plot(gra,'MarkerSize',j,'NodeCData',k,'EdgeAlpha',0.1)
m=['Hashtag network : Degrees of hashtags (N_h=',num2str(size(Amtr,1)),')'];
title(m)
set(gca,'fontname','Arial','fontsize',12,'fontweight','bold');
set(gcf,'position',[100,100,800,800]);
xlim([0 lsize]);
ylim([0 lsize]);
axis off;
colorbar
print(1,'-dbitmap',strcat(file,'deghas','.jpg'));

% output top20 hashtags, connections and hashtag degrees

fileID=fopen(strcat(file,'.txt'),'w');
fprintf(fileID,'%30s %8s %30s %8s %30s %30s %8s \r\n','Top Hashtags','Number','Top Co-hashtags','Number','Best friends 1','2','Number');
for i=1:20
fprintf(fileID,'%30s %8.0f %30s %8.0f %30s %30s %8.0f \r\n',saveHT{i,1},saveHT{i,2},cell2mat(nodegree{i,1}),nodegree{i,2},cell2mat(conweight{i,1}),cell2mat(conweight{i,2}),conweight{i,3});
end
fclose(fileID);

%% save data
filename=['fin-',file,'.mat'];
save(filename,'savedata','hashtagroup','saveHT','dis','Amtr','conweight','nodegree');

%% Node degree distribution
for i=1:size(nodegree,1)
    count2(i)=nodegree{i,2};
end
count2=count2';
% distribution of node degree
j=unique(count2);
dis2 = [j histc(count2(:),j)];
dis2 = sortrows(dis2,-1);
dis2(:,3)=cumsum(dis2(:,2)); %CCDF

dis2=dis2(1:350,:);

loglog(dis2(:,1),dis2(:,2),'b*','MarkerSize',5,'LineWidth',2)
xlabel('Node degree k');
ylabel('Number of group N_k');
title(strcat('Distribution of node degree'))
set(gca,'fontname','Arial','fontsize',12,'fontweight','bold');
set(gcf,'position',[100,100,600,600]);
print(1,'-dbitmap',strcat(file,'dis-fre-nodegree','.jpg'));
%legend('well location','compute domain','building area','location','northeast');
%legend('boxoff');

%CCDF
i=log10(dis2(:,1));
j=log10(dis2(:,3));
coef=polyfit(i,j,1);
k=polyval(coef,i);
%R^2 error
%yres=j-k;
%SSres=sum(yres.^2);
%SStot=std(j)^2*(size(j,1)-1);
%Rr=1-SSres/SStot
gamma=1-coef(1);
dis2(:,4)=10.^(k);
loglog(dis2(:,1),dis2(:,3),'b*',dis2(:,1),dis2(:,4),'r-','MarkerSize',5,'LineWidth',2);
i=['log(y)=',num2str(coef(1)),'log(x)+',num2str(coef(2))];
legend('CCDF data of node degree',i,'location','northeast');
legend('boxoff');
xlabel('Node degree k');
ylabel('CCDF of N_k');
title(strcat('CCDF of distribution of node degree  gamma=',num2str(gamma)));
set(gca,'fontname','Arial','fontsize',12,'fontweight','bold');
set(gcf,'position',[100,100,600,600]);
print(1,'-dbitmap',strcat(file,'dis-CCDF-nodegree','.jpg'));

%zipf
dis2=sortrows(dis2,-1);
dis2(:,5)=[1:size(dis2,1)];   %rank
%dis2=dis2(1:350,:);
i=log10(dis2(:,5));
j=log10(dis2(:,1));
coef=polyfit(i,j,1);
k=polyval(coef,i);
alpha=-coef(1);
dis2(:,6)=10.^(k);
loglog(dis2(:,5),dis2(:,1),'b*',dis2(:,5),dis2(:,6),'r-','MarkerSize',5,'LineWidth',2);
i=['log(y)=',num2str(coef(1)),'log(x)+',num2str(coef(2))];
legend('rank data of node degree',i,'location','northeast');
legend('boxoff');
xlabel('rank r');
ylabel('Node degree k');
title(strcat('Zipf of Node degree k, alpha=',num2str(alpha)));
set(gca,'fontname','Arial','fontsize',12,'fontweight','bold');
set(gcf,'position',[100,100,600,600]);
print(1,'-dbitmap',strcat(file,'dis-Zipf-nodegree','.jpg'));

%%
%'BusyAction', 'ButtonDownFcn',
%'CreateFcn', 'DeleteFcn', 'DisplayName',
%'EdgeAlpha', 'EdgeCData', 'EdgeColor',
%'EdgeLabel', 'EdgeLabelMode',
%'HandleVisibility', 'HitTest',
%'Interruptible', 'LineStyle', 'LineWidth',
%'Marker', 'MarkerSize', 'NodeCData',
%'NodeColor', 'NodeLabel', 'NodeLabelMode',
%'Parent', 'PickableParts', 'Selected',
%'SelectionHighlight', 'ShowArrows', 'Tag',
%'UIContextMenu', 'UserData', 'Visible',
%'XData', 'YData', 'Layout', 'Dimension',
%'Iterations', 'XStart', 'YStart',
%'Direction', 'Sources', 'Sinks',
%'AssignLayers'