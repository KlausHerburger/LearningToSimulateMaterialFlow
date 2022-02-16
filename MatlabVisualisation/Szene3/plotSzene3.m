clear
load ../../Data/Matlab/Szene3/30_45_1_9.mat
winkel1 = 30*pi/180;
winkel2 = -45*pi/180;

pos1x = double(data(:,1));
pos1y = double(data(:,2));
pos2x = double(data(:,3));
pos2y = double(data(:,4));
pos3x = double(data(:,5));
pos3y = double(data(:,6));
pos4x = double(data(:,7));
pos4y = double(data(:,8));
pos5x = double(data(:,9));
pos5y = double(data(:,10));
pos6x = double(data(:,11));
pos6y = double(data(:,12));
pos7x = double(data(:,13));
pos7y = double(data(:,14));
pos8x = double(data(:,15));
pos8y = double(data(:,16));
pos9x = double(data(:,17));
pos9y = double(data(:,18));

figure(1)
h_fig = figure(1);
axis equal 
xlim([-0.2,1.2]);
ylim([-0.2,6.2]);
for idx = 1:20:length(pos1x)
    figure(h_fig); cla; hold on;
    plot([0.24-cos(winkel1)*0.35 0.24+cos(winkel1)*0.35],[1.47-sin(winkel1)*0.35 1.47+sin(winkel1)*0.35],'k-','linewidth',6)
    plot([0.65-cos(winkel2)*0.5 0.65+cos(winkel2)*0.5],[3-sin(winkel2)*0.5 3+sin(winkel2)*0.5],'k-','linewidth',6)
    plot([0 1],[6 6],'k-','linewidth',6) 
    plot([0 1],[0 0],'k-','linewidth',2) 
    plot([0 0],[0 6],'k-','linewidth',2) 
    plot([1 1],[0 6],'k-','linewidth',2)
    plot(pos1x(idx),pos1y(idx),'r.','markersize',30)
    plot(pos2x(idx),pos2y(idx),'r.','markersize',30)
    plot(pos3x(idx),pos3y(idx),'r.','markersize',30)
    plot(pos4x(idx),pos4y(idx),'r.','markersize',30)
    plot(pos5x(idx),pos5y(idx),'r.','markersize',30)
    plot(pos6x(idx),pos6y(idx),'r.','markersize',30)
    plot(pos7x(idx),pos7y(idx),'r.','markersize',30)
    plot(pos8x(idx),pos8y(idx),'r.','markersize',30)
    plot(pos9x(idx),pos9y(idx),'r.','markersize',30)
end