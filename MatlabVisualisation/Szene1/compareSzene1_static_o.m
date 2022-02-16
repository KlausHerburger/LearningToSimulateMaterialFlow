%%
clear
load Szene1/5/49_3.mat
winkel = 49*pi/180;
offsetX = 1.2;
offsetX2 = 2.7;
offsetY = 3.5;
idx1=1;
idx2=140;
idx3=180;
idx4=220;

txt1 = 't = 0s';
txt2 = 't = 14s';
txt3 = 't = 18s';
txt4 = 't = 22s';

pos1x = double(data_rollout(:,1));
pos1y = double(data_rollout(:,2));
pos2x = double(data_rollout(:,3));
pos2y = double(data_rollout(:,4));
pos3x = double(data_rollout(:,5));
pos3y = double(data_rollout(:,6));
pos4x = double(data_rollout(:,7));
pos4y = double(data_rollout(:,8));

pos1xT = double(true_rollout(:,1));
pos1yT = double(true_rollout(:,2));
pos2xT = double(true_rollout(:,3));
pos2yT = double(true_rollout(:,4));
pos3xT = double(true_rollout(:,5));
pos3yT = double(true_rollout(:,6));
pos4xT = double(true_rollout(:,7));
pos4yT = double(true_rollout(:,8));


figure('Renderer', 'painters', 'Position', [5 5 800 800])
h_fig = figure(1);
axis equal 
xlim([-0.2, offsetX*2+offsetX2]);
ylim([-0.2,3.2+ offsetY + 0.3]);

figure(h_fig); cla; hold on;
text((1+offsetX)/2,3.2,txt3,'HorizontalAlignment','center')
text((1+offsetX)/2+offsetX2,3.2,txt4,'HorizontalAlignment','center')
text((1+offsetX)/2,3.2+offsetY,txt1,'HorizontalAlignment','center')
text((1+offsetX)/2+offsetX2,3.2+offsetY,txt2,'HorizontalAlignment','center')
plot([0 0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34+offsetY 1.445+sin(winkel)*0.34+offsetY],'k-','linewidth',5) 
plot([0 1],[0+offsetY 0+offsetY],'k-','linewidth',3) 
plot([0 0],[0+offsetY 3+offsetY],'k-','linewidth',3) 
plot([1 1],[0+offsetY 3+offsetY],'k-','linewidth',3)
plot([0+offsetX 0.24+cos(winkel)*0.34+offsetX],[1.445-sin(winkel)*0.34+offsetY 1.445+sin(winkel)*0.34+offsetY],'k-','linewidth',5) 
plot([0+offsetX 1+offsetX],[0+offsetY 0+offsetY],'k-','linewidth',3) 
plot([0+offsetX 0+offsetX],[0+offsetY 3+offsetY],'k-','linewidth',3) 
plot([1+offsetX 1+offsetX],[0+offsetY 3+offsetY],'k-','linewidth',3)
idx=idx1;
plot(pos1x(idx),pos1y(idx)+offsetY,'b.','markersize',22)
plot(pos2x(idx),pos2y(idx)+offsetY,'b.','markersize',22)
plot(pos3x(idx),pos3y(idx)+offsetY,'b.','markersize',22)
plot(pos4x(idx),pos4y(idx)+offsetY,'b.','markersize',22)
plot(pos1xT(idx)+offsetX,pos1yT(idx)+offsetY,'r.','markersize',22)
plot(pos2xT(idx)+offsetX,pos2yT(idx)+offsetY,'r.','markersize',22)
plot(pos3xT(idx)+offsetX,pos3yT(idx)+offsetY,'r.','markersize',22)
plot(pos4xT(idx)+offsetX,pos4yT(idx)+offsetY,'r.','markersize',22)


plot([0+offsetX2 0.24+cos(winkel)*0.34+offsetX2],[1.445-sin(winkel)*0.34+offsetY 1.445+sin(winkel)*0.34+offsetY],'k-','linewidth',5) 
plot([0+offsetX2 1+offsetX2],[0+offsetY 0+offsetY],'k-','linewidth',3) 
plot([0+offsetX2 0+offsetX2],[0+offsetY 3+offsetY],'k-','linewidth',3) 
plot([1+offsetX2 1+offsetX2],[0+offsetY 3+offsetY],'k-','linewidth',3)
plot([0+offsetX+offsetX2 0.24+cos(winkel)*0.34+offsetX+offsetX2],[1.445-sin(winkel)*0.34+offsetY 1.445+sin(winkel)*0.34+offsetY],'k-','linewidth',5) 
plot([0+offsetX+offsetX2 1+offsetX+offsetX2],[0+offsetY 0+offsetY],'k-','linewidth',3) 
plot([0+offsetX+offsetX2 0+offsetX+offsetX2],[0+offsetY 3+offsetY],'k-','linewidth',3) 
plot([1+offsetX+offsetX2 1+offsetX+offsetX2],[0+offsetY 3+offsetY],'k-','linewidth',3)
idx=idx2;
plot(pos1x(idx)+offsetX2,pos1y(idx)+offsetY,'b.','markersize',22)
plot(pos2x(idx)+offsetX2,pos2y(idx)+offsetY,'b.','markersize',22)
plot(pos3x(idx)+offsetX2,pos3y(idx)+offsetY,'b.','markersize',22)
plot(pos4x(idx)+offsetX2,pos4y(idx)+offsetY,'b.','markersize',22)
plot(pos1xT(idx)+offsetX2+offsetX,pos1yT(idx)+offsetY,'r.','markersize',22)
plot(pos2xT(idx)+offsetX2+offsetX,pos2yT(idx)+offsetY,'r.','markersize',22)
plot(pos3xT(idx)+offsetX2+offsetX,pos3yT(idx)+offsetY,'r.','markersize',22)
plot(pos4xT(idx)+offsetX2+offsetX,pos4yT(idx)+offsetY,'r.','markersize',22)

plot([0 0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([0 1],[0 0],'k-','linewidth',3) 
plot([0 0],[0 3],'k-','linewidth',3) 
plot([1 1],[0 3],'k-','linewidth',3)
plot([0+offsetX 0.24+cos(winkel)*0.34+offsetX],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([0+offsetX 1+offsetX],[0 0],'k-','linewidth',3) 
plot([0+offsetX 0+offsetX],[0 3],'k-','linewidth',3) 
plot([1+offsetX 1+offsetX],[0 3],'k-','linewidth',3)
idx=idx3;
plot(pos1x(idx),pos1y(idx),'b.','markersize',22)
plot(pos2x(idx),pos2y(idx),'b.','markersize',22)
plot(pos3x(idx),pos3y(idx),'b.','markersize',22)
plot(pos4x(idx),pos4y(idx),'b.','markersize',22)
plot(pos1xT(idx)+offsetX,pos1yT(idx),'r.','markersize',22)
plot(pos2xT(idx)+offsetX,pos2yT(idx),'r.','markersize',22)
plot(pos3xT(idx)+offsetX,pos3yT(idx),'r.','markersize',22)
plot(pos4xT(idx)+offsetX,pos4yT(idx),'r.','markersize',22)


plot([0+offsetX2 0.24+cos(winkel)*0.34+offsetX2],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([0+offsetX2 1+offsetX2],[0 0],'k-','linewidth',3) 
plot([0+offsetX2 0+offsetX2],[0 3],'k-','linewidth',3) 
plot([1+offsetX2 1+offsetX2],[0 3],'k-','linewidth',3)
plot([0+offsetX+offsetX2 0.24+cos(winkel)*0.34+offsetX+offsetX2],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([0+offsetX+offsetX2 1+offsetX+offsetX2],[0 0],'k-','linewidth',3) 
plot([0+offsetX+offsetX2 0+offsetX+offsetX2],[0 3],'k-','linewidth',3) 
plot([1+offsetX+offsetX2 1+offsetX+offsetX2],[0 3],'k-','linewidth',3)
idx=idx4;
plot(pos1x(idx)+offsetX2,pos1y(idx),'b.','markersize',22)
plot(pos2x(idx)+offsetX2,pos2y(idx),'b.','markersize',22)
plot(pos3x(idx)+offsetX2,pos3y(idx),'b.','markersize',22)
plot(pos4x(idx)+offsetX2,pos4y(idx),'b.','markersize',22)
plot(pos1xT(idx)+offsetX2+offsetX,pos1yT(idx),'r.','markersize',22)
plot(pos2xT(idx)+offsetX2+offsetX,pos2yT(idx),'r.','markersize',22)
plot(pos3xT(idx)+offsetX2+offsetX,pos3yT(idx),'r.','markersize',22)
plot(pos4xT(idx)+offsetX2+offsetX,pos4yT(idx),'r.','markersize',22)
