clear
load ../../Data/Matlab/Szene1/30_1.mat
winkel = 30*pi/180;

pos1x = double(data(:,1));
pos1y = double(data(:,2));
pos2x = double(data(:,3));
pos2y = double(data(:,4));
pos3x = double(data(:,5));
pos3y = double(data(:,6));
pos4x = double(data(:,7));
pos4y = double(data(:,8));

figure(1)
h_fig = figure(1);
axis equal 
xlim([-0.2,1.2]);
ylim([-0.2,3.2]);

for idx = 1:50:length(pos1x)
    figure(h_fig); cla; hold on;
    plot([0 1],[0 0],'k-','linewidth',2) 
    plot([0 0],[0 3],'k-','linewidth',2) 
    plot([1 1],[0 3],'k-','linewidth',2)
    plot([0.24-cos(winkel)*0.34 0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
    plot(pos1x(idx),pos1y(idx),'r.','markersize',30)
    plot(pos2x(idx),pos2y(idx),'r.','markersize',30)
    plot(pos3x(idx),pos3y(idx),'r.','markersize',30)
    plot(pos4x(idx),pos4y(idx),'r.','markersize',30)
end