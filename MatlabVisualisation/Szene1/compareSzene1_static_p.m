%%
clear
load Szene1/5/37_3.mat
winkel = 37*pi/180;
offsetX = 1.2;
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
xlim([-0.2, offsetX*3+1.2]);
ylim([-0.2,3.2]);

figure(h_fig); cla; hold on;
text(0.5,3.05,txt1,'HorizontalAlignment','center')
text(0.5+offsetX,3.05,txt2,'HorizontalAlignment','center')
text(0.5+offsetX*2,3.05,txt3,'HorizontalAlignment','center')
text(0.5+offsetX*3,3.05,txt4,'HorizontalAlignment','center')
plot([0 0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([0 1],[0 0],'k-','linewidth',3) 
plot([0 0],[0 3],'k-','linewidth',3) 
plot([1 1],[0 3],'k-','linewidth',3)
plot([0 0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([0 1],[0 0],'k-','linewidth',3) 
plot([0 0],[0 3],'k-','linewidth',3) 
plot([1 1],[0 3],'k-','linewidth',3)
idx=idx1;
plot(pos1x(idx),pos1y(idx),'b.','markersize',30)
plot(pos2x(idx),pos2y(idx),'b.','markersize',30)
plot(pos3x(idx),pos3y(idx),'b.','markersize',30)
plot(pos4x(idx),pos4y(idx),'b.','markersize',30)
plot(pos1xT(idx),pos1yT(idx),'r.','markersize',30)
plot(pos2xT(idx),pos2yT(idx),'r.','markersize',30)
plot(pos3xT(idx),pos3yT(idx),'r.','markersize',30)
plot(pos4xT(idx),pos4yT(idx),'r.','markersize',30)


plot([ offsetX  offsetX+0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([ offsetX  offsetX+1],[0 0],'k-','linewidth',3) 
plot([ offsetX  offsetX],[0 3],'k-','linewidth',3) 
plot([ offsetX+1  offsetX+1],[0 3],'k-','linewidth',3)
plot([ offsetX  offsetX+0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([ offsetX  offsetX+1],[0 0],'k-','linewidth',3) 
plot([ offsetX  offsetX],[0 3],'k-','linewidth',3) 
plot([ offsetX+1  offsetX+1],[0 3],'k-','linewidth',3)
idx=idx2;
plot(pos1x(idx)+ offsetX,pos1y(idx),'b.','markersize',30)
plot(pos2x(idx)+ offsetX,pos2y(idx),'b.','markersize',30)
plot(pos3x(idx)+ offsetX,pos3y(idx),'b.','markersize',30)
plot(pos4x(idx)+ offsetX,pos4y(idx),'b.','markersize',30)
plot(pos1xT(idx)+ offsetX,pos1yT(idx),'r.','markersize',30)
plot(pos2xT(idx)+offsetX,pos2yT(idx),'r.','markersize',30)
plot(pos3xT(idx)+offsetX,pos3yT(idx),'r.','markersize',30)
plot(pos4xT(idx)+offsetX,pos4yT(idx),'r.','markersize',30)

plot([ offsetX*2  offsetX*2+0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([ offsetX*2  offsetX*2+1],[0 0],'k-','linewidth',3) 
plot([ offsetX*2  offsetX*2],[0 3],'k-','linewidth',3) 
plot([ offsetX*2+1  offsetX*2+1],[0 3],'k-','linewidth',3)
plot([ offsetX*2  offsetX*2+0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([ offsetX*2  offsetX*2+1],[0 0],'k-','linewidth',3) 
plot([ offsetX*2  offsetX*2],[0 3],'k-','linewidth',3) 
plot([ offsetX*2+1  offsetX*2+1],[0 3],'k-','linewidth',3)
idx=idx3;
plot(pos1x(idx)+ offsetX*2,pos1y(idx),'b.','markersize',30)
plot(pos2x(idx)+ offsetX*2,pos2y(idx),'b.','markersize',30)
plot(pos3x(idx)+ offsetX*2,pos3y(idx),'b.','markersize',30)
plot(pos4x(idx)+ offsetX*2,pos4y(idx),'b.','markersize',30)
plot(pos1xT(idx)+ offsetX*2,pos1yT(idx),'r.','markersize',30)
plot(pos2xT(idx)+ offsetX*2,pos2yT(idx),'r.','markersize',30)
plot(pos3xT(idx)+ offsetX*2,pos3yT(idx),'r.','markersize',30)
plot(pos4xT(idx)+ offsetX*2,pos4yT(idx),'r.','markersize',30)

plot([offsetX*3  offsetX*3+0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([offsetX*3  offsetX*3+1],[0 0],'k-','linewidth',3) 
plot([offsetX*3  offsetX*3],[0 3],'k-','linewidth',3) 
plot([offsetX*3+1  offsetX*3+1],[0 3],'k-','linewidth',3)
plot([offsetX*3  offsetX*3+0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',5) 
plot([offsetX*3  offsetX*3+1],[0 0],'k-','linewidth',3) 
plot([offsetX*3  offsetX*3],[0 3],'k-','linewidth',3) 
plot([offsetX*3+1  offsetX*3+1],[0 3],'k-','linewidth',3)
idx=idx4;
plot(pos1x(idx)+ offsetX*3,pos1y(idx),'b.','markersize',30)
plot(pos2x(idx)+ offsetX*3,pos2y(idx),'b.','markersize',30)
plot(pos3x(idx)+ offsetX*3,pos3y(idx),'b.','markersize',30)
plot(pos4x(idx)+ offsetX*3,pos4y(idx),'b.','markersize',30)
plot(pos1xT(idx)+ offsetX*3,pos1yT(idx),'r.','markersize',30)
plot(pos2xT(idx)+ offsetX*3,pos2yT(idx),'r.','markersize',30)
plot(pos3xT(idx)+ offsetX*3,pos3yT(idx),'r.','markersize',30)
plot(pos4xT(idx)+ offsetX*3,pos4yT(idx),'r.','markersize',30)
