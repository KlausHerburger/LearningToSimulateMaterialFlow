%%
clear
load Szene3/2/Gen_60_60_70_70_1_9.mat
winkel1 = 60*pi/180;
winkel2 = -60*pi/180;
winkel3 = 70*pi/180;
winkel4 = -70*pi/180;
offsetX = 1.2;
offsetX2 = 2.7;
offsetY = 6.5;
idx1=1;
idx2=50;
idx3=130;
idx4=179;

txt1 = 't = 0s';
txt2 = 't = 5s';
txt3 = 't = 13s';
txt4 = 't = 18s';

pos1x = double(data_rollout(:,1));
pos1y = double(data_rollout(:,2));
pos2x = double(data_rollout(:,3));
pos2y = double(data_rollout(:,4));
pos3x = double(data_rollout(:,5));
pos3y = double(data_rollout(:,6));
pos4x = double(data_rollout(:,7));
pos4y = double(data_rollout(:,8));
pos5x = double(data_rollout(:,9));
pos5y = double(data_rollout(:,10));
pos6x = double(data_rollout(:,11));
pos6y = double(data_rollout(:,12));
pos7x = double(data_rollout(:,13));
pos7y = double(data_rollout(:,14));
pos8x = double(data_rollout(:,15));
pos8y = double(data_rollout(:,16));
pos9x = double(data_rollout(:,17));
pos9y = double(data_rollout(:,18));

pos1xT = double(true_rollout(:,1));
pos1yT = double(true_rollout(:,2));
pos2xT = double(true_rollout(:,3));
pos2yT = double(true_rollout(:,4));
pos3xT = double(true_rollout(:,5));
pos3yT = double(true_rollout(:,6));
pos4xT = double(true_rollout(:,7));
pos4yT = double(true_rollout(:,8));
pos5xT = double(true_rollout(:,9));
pos5yT = double(true_rollout(:,10));
pos6xT = double(true_rollout(:,11));
pos6yT = double(true_rollout(:,12));
pos7xT = double(true_rollout(:,13));
pos7yT = double(true_rollout(:,14));
pos8xT = double(true_rollout(:,15));
pos8yT = double(true_rollout(:,16));
pos9xT = double(true_rollout(:,17));
pos9yT = double(true_rollout(:,18));


figure('Renderer', 'painters', 'Position', [5 5 800 800])
h_fig = figure(1);
axis equal 
xlim([-0.2, offsetX*2+offsetX2]);
ylim([-0.2,6.2+ offsetY + 0.3]);

figure(h_fig); cla; hold on;
text((1+offsetX)/2,6.2,txt3,'HorizontalAlignment','center')
text((1+offsetX)/2+offsetX2,6.2,txt4,'HorizontalAlignment','center')
text((1+offsetX)/2,6.2+offsetY,txt1,'HorizontalAlignment','center')
text((1+offsetX)/2+offsetX2,6.2+offsetY,txt2,'HorizontalAlignment','center')
plot([0 0.24+cos(winkel1)*0.34],[1.445-sin(winkel1)*0.34+offsetY 1.445+sin(winkel1)*0.34+offsetY],'k-','linewidth',3) 
plot([0.76-cos(winkel2)*0.35 0.76+cos(winkel2)*0.35],[2.5-sin(winkel2)*0.35+offsetY 2.5+sin(winkel2)*0.35+offsetY],'k-','linewidth',3)
plot([0.2-cos(winkel3)*0.5 0.2+cos(winkel3)*0.5],[4-sin(winkel3)*0.5+offsetY 4+sin(winkel3)*0.5+offsetY],'k-','linewidth',3)
plot([0.8-cos(winkel4)*0.5 0.8+cos(winkel4)*0.5],[4-sin(winkel4)*0.5+offsetY 4+sin(winkel4)*0.5+offsetY],'k-','linewidth',3)
plot([0 1],[6+offsetY 6+offsetY],'k-','linewidth',3) 
plot([0 1],[0+offsetY 0+offsetY],'k-','linewidth',2) 
plot([0 0],[0+offsetY 6+offsetY],'k-','linewidth',2) 
plot([1 1],[0+offsetY 6+offsetY],'k-','linewidth',2)
plot([0+offsetX 0.24+cos(winkel1)*0.34+offsetX],[1.445-sin(winkel1)*0.34+offsetY 1.445+sin(winkel1)*0.34+offsetY],'k-','linewidth',3) 
plot([0.76-cos(winkel2)*0.35+offsetX 0.76+cos(winkel2)*0.35+offsetX],[2.5-sin(winkel2)*0.35+offsetY 2.5+sin(winkel2)*0.35+offsetY],'k-','linewidth',3)
plot([0.2-cos(winkel3)*0.5+offsetX 0.2+cos(winkel3)*0.5+offsetX],[4-sin(winkel3)*0.5+offsetY 4+sin(winkel3)*0.5+offsetY],'k-','linewidth',3)
plot([0.8-cos(winkel4)*0.5+offsetX 0.8+cos(winkel4)*0.5+offsetX],[4-sin(winkel4)*0.5+offsetY 4+sin(winkel4)*0.5+offsetY],'k-','linewidth',3)
plot([0+offsetX 1+offsetX],[6+offsetY 6+offsetY],'k-','linewidth',3) 
plot([0+offsetX 1+offsetX],[0+offsetY 0+offsetY],'k-','linewidth',2) 
plot([0+offsetX 0+offsetX],[0+offsetY 6+offsetY],'k-','linewidth',2) 
plot([1+offsetX 1+offsetX],[0+offsetY 6+offsetY],'k-','linewidth',2)
idx=idx1;
plot(pos1x(idx),pos1y(idx)+offsetY,'b.','markersize',12)
plot(pos2x(idx),pos2y(idx)+offsetY,'b.','markersize',12)
plot(pos3x(idx),pos3y(idx)+offsetY,'b.','markersize',12)
plot(pos4x(idx),pos4y(idx)+offsetY,'b.','markersize',12)
plot(pos5x(idx),pos5y(idx)+offsetY,'b.','markersize',12)
plot(pos6x(idx),pos6y(idx)+offsetY,'b.','markersize',12)
plot(pos7x(idx),pos7y(idx)+offsetY,'b.','markersize',12)
plot(pos8x(idx),pos8y(idx)+offsetY,'b.','markersize',12)
plot(pos9x(idx),pos9y(idx)+offsetY,'b.','markersize',12)
plot(pos1xT(idx)+offsetX,pos1yT(idx)+offsetY,'r.','markersize',12)
plot(pos2xT(idx)+offsetX,pos2yT(idx)+offsetY,'r.','markersize',12)
plot(pos3xT(idx)+offsetX,pos3yT(idx)+offsetY,'r.','markersize',12)
plot(pos4xT(idx)+offsetX,pos4yT(idx)+offsetY,'r.','markersize',12)
plot(pos5xT(idx)+offsetX,pos5yT(idx)+offsetY,'r.','markersize',12)
plot(pos6xT(idx)+offsetX,pos6yT(idx)+offsetY,'r.','markersize',12)
plot(pos7xT(idx)+offsetX,pos7yT(idx)+offsetY,'r.','markersize',12)
plot(pos8xT(idx)+offsetX,pos8yT(idx)+offsetY,'r.','markersize',12)
plot(pos9xT(idx)+offsetX,pos9yT(idx)+offsetY,'r.','markersize',12)


plot([0+offsetX2 0.24+cos(winkel1)*0.34+offsetX2],[1.445-sin(winkel1)*0.34+offsetY 1.445+sin(winkel1)*0.34+offsetY],'k-','linewidth',3) 
plot([0.76-cos(winkel2)*0.35+offsetX2 0.76+cos(winkel2)*0.35+offsetX2],[2.5-sin(winkel2)*0.35+offsetY 2.5+sin(winkel2)*0.35+offsetY],'k-','linewidth',3)
plot([0.2-cos(winkel3)*0.5+offsetX2 0.2+cos(winkel3)*0.5+offsetX2],[4-sin(winkel3)*0.5+offsetY 4+sin(winkel3)*0.5+offsetY],'k-','linewidth',3)
plot([0.8-cos(winkel4)*0.5+offsetX2 0.8+cos(winkel4)*0.5+offsetX2],[4-sin(winkel4)*0.5+offsetY 4+sin(winkel4)*0.5+offsetY],'k-','linewidth',3)
plot([0+offsetX2 1+offsetX2],[6+offsetY 6+offsetY],'k-','linewidth',3) 
plot([0+offsetX2 1+offsetX2],[0+offsetY 0+offsetY],'k-','linewidth',2) 
plot([0+offsetX2 0+offsetX2],[0+offsetY 6+offsetY],'k-','linewidth',2) 
plot([1+offsetX2 1+offsetX2],[0+offsetY 6+offsetY],'k-','linewidth',2)
plot([0+offsetX+offsetX2 0.24+cos(winkel1)*0.34+offsetX+offsetX2],[1.445-sin(winkel1)*0.34+offsetY 1.445+sin(winkel1)*0.34+offsetY],'k-','linewidth',3) 
plot([0+offsetX+offsetX2 1+offsetX+offsetX2],[0+offsetY 0+offsetY],'k-','linewidth',2) 
plot([0+offsetX+offsetX2 0+offsetX+offsetX2],[0+offsetY 6+offsetY],'k-','linewidth',2) 
plot([1+offsetX+offsetX2 1+offsetX+offsetX2],[0+offsetY 6+offsetY],'k-','linewidth',2)
plot([0+offsetX+offsetX2 0.24+cos(winkel1)*0.34+offsetX+offsetX2],[1.445-sin(winkel1)*0.34+offsetY 1.445+sin(winkel1)*0.34+offsetY],'k-','linewidth',3) 
plot([0.76-cos(winkel2)*0.35+offsetX+offsetX2 0.76+cos(winkel2)*0.35+offsetX+offsetX2],[2.5-sin(winkel2)*0.35+offsetY 2.5+sin(winkel2)*0.35+offsetY],'k-','linewidth',3)
plot([0.2-cos(winkel3)*0.5+offsetX+offsetX2 0.2+cos(winkel3)*0.5+offsetX+offsetX2],[4-sin(winkel3)*0.5+offsetY 4+sin(winkel3)*0.5+offsetY],'k-','linewidth',3)
plot([0.8-cos(winkel4)*0.5+offsetX+offsetX2 0.8+cos(winkel4)*0.5+offsetX+offsetX2],[4-sin(winkel4)*0.5+offsetY 4+sin(winkel4)*0.5+offsetY],'k-','linewidth',3)
plot([0+offsetX2+offsetX 1+offsetX2+offsetX],[6+offsetY 6+offsetY],'k-','linewidth',3) 
idx=idx2;
plot(pos1x(idx)+offsetX2,pos1y(idx)+offsetY,'b.','markersize',12)
plot(pos2x(idx)+offsetX2,pos2y(idx)+offsetY,'b.','markersize',12)
plot(pos3x(idx)+offsetX2,pos3y(idx)+offsetY,'b.','markersize',12)
plot(pos4x(idx)+offsetX2,pos4y(idx)+offsetY,'b.','markersize',12)
plot(pos5x(idx)+offsetX2,pos5y(idx)+offsetY,'b.','markersize',12)
plot(pos6x(idx)+offsetX2,pos6y(idx)+offsetY,'b.','markersize',12)
plot(pos7x(idx)+offsetX2,pos7y(idx)+offsetY,'b.','markersize',12)
plot(pos8x(idx)+offsetX2,pos8y(idx)+offsetY,'b.','markersize',12)
plot(pos9x(idx)+offsetX2,pos9y(idx)+offsetY,'b.','markersize',12)
plot(pos1xT(idx)+offsetX2+offsetX,pos1yT(idx)+offsetY,'r.','markersize',12)
plot(pos2xT(idx)+offsetX2+offsetX,pos2yT(idx)+offsetY,'r.','markersize',12)
plot(pos3xT(idx)+offsetX2+offsetX,pos3yT(idx)+offsetY,'r.','markersize',12)
plot(pos4xT(idx)+offsetX2+offsetX,pos4yT(idx)+offsetY,'r.','markersize',12)
plot(pos5xT(idx)+offsetX2+offsetX,pos5yT(idx)+offsetY,'r.','markersize',12)
plot(pos6xT(idx)+offsetX2+offsetX,pos6yT(idx)+offsetY,'r.','markersize',12)
plot(pos7xT(idx)+offsetX2+offsetX,pos7yT(idx)+offsetY,'r.','markersize',12)
plot(pos8xT(idx)+offsetX2+offsetX,pos8yT(idx)+offsetY,'r.','markersize',12)
plot(pos9xT(idx)+offsetX2+offsetX,pos9yT(idx)+offsetY,'r.','markersize',12)


plot([0 0.24+cos(winkel1)*0.34],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',3) 
plot([0.76-cos(winkel2)*0.35 0.76+cos(winkel2)*0.35],[2.5-sin(winkel2)*0.35 2.5+sin(winkel2)*0.35],'k-','linewidth',3)
plot([0.2-cos(winkel3)*0.5 0.2+cos(winkel3)*0.5],[4-sin(winkel3)*0.5 4+sin(winkel3)*0.5],'k-','linewidth',3)
plot([0.8-cos(winkel4)*0.5 0.8+cos(winkel4)*0.5],[4-sin(winkel4)*0.5 4+sin(winkel4)*0.5],'k-','linewidth',3)
plot([0 1],[6 6],'k-','linewidth',3) 
plot([0 1],[0 0],'k-','linewidth',2) 
plot([0 0],[0 6],'k-','linewidth',2) 
plot([1 1],[0 6],'k-','linewidth',2)
plot([0+offsetX 0.24+cos(winkel1)*0.34+offsetX],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',3) 
plot([0.76-cos(winkel2)*0.35+offsetX 0.76+cos(winkel2)*0.35+offsetX],[2.5-sin(winkel2)*0.35 2.5+sin(winkel2)*0.35],'k-','linewidth',3)
plot([0.2-cos(winkel3)*0.5+offsetX 0.2+cos(winkel3)*0.5+offsetX],[4-sin(winkel3)*0.5 4+sin(winkel3)*0.5],'k-','linewidth',3)
plot([0.8-cos(winkel4)*0.5+offsetX 0.8+cos(winkel4)*0.5+offsetX],[4-sin(winkel4)*0.5 4+sin(winkel4)*0.5],'k-','linewidth',3)
plot([0+offsetX 1+offsetX],[6 6],'k-','linewidth',3) 
plot([0+offsetX 1+offsetX],[0 0],'k-','linewidth',2) 
plot([0+offsetX 0+offsetX],[0 6],'k-','linewidth',2) 
plot([1+offsetX 1+offsetX],[0 6],'k-','linewidth',2)
idx=idx3;
plot(pos1x(idx),pos1y(idx),'b.','markersize',12)
plot(pos2x(idx),pos2y(idx),'b.','markersize',12)
plot(pos3x(idx),pos3y(idx),'b.','markersize',12)
plot(pos4x(idx),pos4y(idx),'b.','markersize',12)
plot(pos5x(idx),pos5y(idx),'b.','markersize',12)
plot(pos6x(idx),pos6y(idx),'b.','markersize',12)
plot(pos7x(idx),pos7y(idx),'b.','markersize',12)
plot(pos8x(idx),pos8y(idx),'b.','markersize',12)
plot(pos9x(idx),pos9y(idx),'b.','markersize',12)
plot(pos1xT(idx)+offsetX,pos1yT(idx),'r.','markersize',12)
plot(pos2xT(idx)+offsetX,pos2yT(idx),'r.','markersize',12)
plot(pos3xT(idx)+offsetX,pos3yT(idx),'r.','markersize',12)
plot(pos4xT(idx)+offsetX,pos4yT(idx),'r.','markersize',12)
plot(pos5xT(idx)+offsetX,pos5yT(idx),'r.','markersize',12)
plot(pos6xT(idx)+offsetX,pos6yT(idx),'r.','markersize',12)
plot(pos7xT(idx)+offsetX,pos7yT(idx),'r.','markersize',12)
plot(pos8xT(idx)+offsetX,pos8yT(idx),'r.','markersize',12)
plot(pos9xT(idx)+offsetX,pos9yT(idx),'r.','markersize',12)


plot([0+offsetX2 0.24+cos(winkel1)*0.34+offsetX2],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',3) 
plot([0.76-cos(winkel2)*0.35+offsetX2 0.76+cos(winkel2)*0.35+offsetX2],[2.5-sin(winkel2)*0.35 2.5+sin(winkel2)*0.35],'k-','linewidth',3)
plot([0.2-cos(winkel3)*0.5+offsetX2 0.2+cos(winkel3)*0.5+offsetX2],[4-sin(winkel3)*0.5 4+sin(winkel3)*0.5],'k-','linewidth',3)
plot([0.8-cos(winkel4)*0.5+offsetX2 0.8+cos(winkel4)*0.5+offsetX2],[4-sin(winkel4)*0.5 4+sin(winkel4)*0.5],'k-','linewidth',3)
plot([0+offsetX2 1+offsetX2],[6 6],'k-','linewidth',3) 
plot([0+offsetX2 1+offsetX2],[0 0],'k-','linewidth',2) 
plot([0+offsetX2 0+offsetX2],[0 6],'k-','linewidth',2) 
plot([1+offsetX2 1+offsetX2],[0 6],'k-','linewidth',2)
plot([0+offsetX+offsetX2 0.24+cos(winkel1)*0.34+offsetX+offsetX2],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',3) 
plot([0.76-cos(winkel2)*0.35+offsetX+offsetX2 0.76+cos(winkel2)*0.35+offsetX+offsetX2],[2.5-sin(winkel2)*0.35 2.5+sin(winkel2)*0.35],'k-','linewidth',3)
plot([0.2-cos(winkel3)*0.5+offsetX+offsetX2 0.2+cos(winkel3)*0.5+offsetX+offsetX2],[4-sin(winkel3)*0.5 4+sin(winkel3)*0.5],'k-','linewidth',3)
plot([0.8-cos(winkel4)*0.5+offsetX+offsetX2 0.8+cos(winkel4)*0.5+offsetX+offsetX2],[4-sin(winkel4)*0.5 4+sin(winkel4)*0.5],'k-','linewidth',3)
plot([0+offsetX+offsetX2 1+offsetX+offsetX2],[6 6],'k-','linewidth',3) 
plot([0+offsetX+offsetX2 1+offsetX+offsetX2],[0 0],'k-','linewidth',2) 
plot([0+offsetX+offsetX2 0+offsetX+offsetX2],[0 6],'k-','linewidth',2) 
plot([1+offsetX+offsetX2 1+offsetX+offsetX2],[0 6],'k-','linewidth',2)
idx=idx4;
plot(pos1x(idx)+offsetX2,pos1y(idx),'b.','markersize',12)
plot(pos2x(idx)+offsetX2,pos2y(idx),'b.','markersize',12)
plot(pos3x(idx)+offsetX2,pos3y(idx),'b.','markersize',12)
plot(pos4x(idx)+offsetX2,pos4y(idx),'b.','markersize',12)
plot(pos5x(idx)+offsetX2,pos5y(idx),'b.','markersize',12)
plot(pos6x(idx)+offsetX2,pos6y(idx),'b.','markersize',12)
plot(pos7x(idx)+offsetX2,pos7y(idx),'b.','markersize',12)
plot(pos8x(idx)+offsetX2,pos8y(idx),'b.','markersize',12)
plot(pos9x(idx)+offsetX2,pos9y(idx),'b.','markersize',12)
plot(pos1xT(idx)+offsetX2+offsetX,pos1yT(idx),'r.','markersize',12)
plot(pos2xT(idx)+offsetX2+offsetX,pos2yT(idx),'r.','markersize',12)
plot(pos3xT(idx)+offsetX2+offsetX,pos3yT(idx),'r.','markersize',12)
plot(pos4xT(idx)+offsetX2+offsetX,pos4yT(idx),'r.','markersize',12)
plot(pos5xT(idx)+offsetX2+offsetX,pos5yT(idx),'r.','markersize',12)
plot(pos6xT(idx)+offsetX2+offsetX,pos6yT(idx),'r.','markersize',12)
plot(pos7xT(idx)+offsetX2+offsetX,pos7yT(idx),'r.','markersize',12)
plot(pos8xT(idx)+offsetX2+offsetX,pos8yT(idx),'r.','markersize',12)
plot(pos9xT(idx)+offsetX2+offsetX,pos9yT(idx),'r.','markersize',12)
