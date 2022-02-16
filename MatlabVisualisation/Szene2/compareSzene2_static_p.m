%%
clear
load Szene2/30_1_9.mat
winkel1 = 30*pi/180;
offsetX = 1.2;
idx1=1;
idx2=100;
idx3=200;
idx4=400;

txt1 = 't = 0s';
txt2 = 't = 10s';
txt3 = 't = 20s';
txt4 = 't = 40s';

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
xlim([-0.2, offsetX*3+1.2]);
ylim([-0.2,3.5]);

figure(h_fig); cla; hold on;
text(0.5,3.2,txt1,'HorizontalAlignment','center')
text(0.5+offsetX,3.2,txt2,'HorizontalAlignment','center')
text(0.5+offsetX*2,3.2,txt3,'HorizontalAlignment','center')
text(0.5+offsetX*3,3.2,txt4,'HorizontalAlignment','center')
plot([0 0.24+cos(winkel1)*0.34],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',5)
plot([0 1],[3 3],'k-','linewidth',5) 
plot([0 1],[0 0],'k-','linewidth',3) 
plot([0 0],[0 3],'k-','linewidth',3) 
plot([1 1],[0 3],'k-','linewidth',3)
idx=idx1;
plot(pos1x(idx),pos1y(idx),'b.','markersize',30)
plot(pos2x(idx),pos2y(idx),'b.','markersize',30)
plot(pos3x(idx),pos3y(idx),'b.','markersize',30)
plot(pos4x(idx),pos4y(idx),'b.','markersize',30)
plot(pos5x(idx),pos5y(idx),'b.','markersize',30)
plot(pos6x(idx),pos6y(idx),'b.','markersize',30)
plot(pos7x(idx),pos7y(idx),'b.','markersize',30)
plot(pos8x(idx),pos8y(idx),'b.','markersize',30)
plot(pos9x(idx),pos9y(idx),'b.','markersize',30)
plot(pos1xT(idx),pos1yT(idx),'r.','markersize',30)
plot(pos2xT(idx),pos2yT(idx),'r.','markersize',30)
plot(pos3xT(idx),pos3yT(idx),'r.','markersize',30)
plot(pos4xT(idx),pos4yT(idx),'r.','markersize',30)
plot(pos5xT(idx),pos5yT(idx),'r.','markersize',30)
plot(pos6xT(idx),pos6yT(idx),'r.','markersize',30)
plot(pos7xT(idx),pos7yT(idx),'r.','markersize',30)
plot(pos8xT(idx),pos8yT(idx),'r.','markersize',30)
plot(pos9xT(idx),pos9yT(idx),'r.','markersize',30)    


plot([ offsetX  offsetX+0.24+cos(winkel1)*0.34],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',5) 
plot([ offsetX  offsetX+1],[0 0],'k-','linewidth',3) 
plot([ offsetX  offsetX],[0 3],'k-','linewidth',3) 
plot([ offsetX+1  offsetX+1],[0 3],'k-','linewidth',3)
plot([ offsetX  offsetX+0.24+cos(winkel1)*0.34],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',5) 
plot([ offsetX  offsetX+1],[0 0],'k-','linewidth',3) 
plot([ offsetX  offsetX],[0 3],'k-','linewidth',3) 
plot([ offsetX+1  offsetX+1],[0 3],'k-','linewidth',3)
plot([offsetX 1+offsetX],[3 3],'k-','linewidth',5) 
idx=idx2;
plot(pos1x(idx)+ offsetX,pos1y(idx),'b.','markersize',30)
plot(pos2x(idx)+ offsetX,pos2y(idx),'b.','markersize',30)
plot(pos3x(idx)+ offsetX,pos3y(idx),'b.','markersize',30)
plot(pos4x(idx)+ offsetX,pos4y(idx),'b.','markersize',30)
plot(pos1x(idx)+ offsetX,pos1y(idx),'b.','markersize',30)
plot(pos2x(idx)+ offsetX,pos2y(idx),'b.','markersize',30)
plot(pos3x(idx)+ offsetX,pos3y(idx),'b.','markersize',30)
plot(pos4x(idx)+ offsetX,pos4y(idx),'b.','markersize',30)
plot(pos5x(idx)+ offsetX,pos5y(idx),'b.','markersize',30)
plot(pos6x(idx)+ offsetX,pos6y(idx),'b.','markersize',30)
plot(pos7x(idx)+ offsetX,pos7y(idx),'b.','markersize',30)
plot(pos8x(idx)+ offsetX,pos8y(idx),'b.','markersize',30)
plot(pos9x(idx)+ offsetX,pos9y(idx),'b.','markersize',30)
plot(pos1xT(idx)+ offsetX,pos1yT(idx),'r.','markersize',30)
plot(pos2xT(idx)+offsetX,pos2yT(idx),'r.','markersize',30)
plot(pos3xT(idx)+offsetX,pos3yT(idx),'r.','markersize',30)
plot(pos4xT(idx)+offsetX,pos4yT(idx),'r.','markersize',30)
plot(pos5xT(idx)+ offsetX,pos5yT(idx),'r.','markersize',30)
plot(pos6xT(idx)+offsetX,pos6yT(idx),'r.','markersize',30)
plot(pos7xT(idx)+offsetX,pos7yT(idx),'r.','markersize',30)
plot(pos8xT(idx)+offsetX,pos8yT(idx),'r.','markersize',30)
plot(pos9xT(idx)+ offsetX,pos9yT(idx),'r.','markersize',30)

plot([ offsetX*2  offsetX*2+0.24+cos(winkel1)*0.34],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',5) 
plot([ offsetX*2  offsetX*2+1],[0 0],'k-','linewidth',3) 
plot([ offsetX*2  offsetX*2],[0 3],'k-','linewidth',3) 
plot([ offsetX*2+1  offsetX*2+1],[0 3],'k-','linewidth',3)
plot([ offsetX*2  offsetX*2+0.24+cos(winkel1)*0.34],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',5) 
plot([ offsetX*2  offsetX*2+1],[0 0],'k-','linewidth',3) 
plot([ offsetX*2  offsetX*2],[0 3],'k-','linewidth',3) 
plot([ offsetX*2+1  offsetX*2+1],[0 3],'k-','linewidth',3)
plot([offsetX*2 1+offsetX*2],[3 3],'k-','linewidth',5) 
idx=idx3;
plot(pos1x(idx)+ offsetX*2,pos1y(idx),'b.','markersize',30)
plot(pos2x(idx)+ offsetX*2,pos2y(idx),'b.','markersize',30)
plot(pos3x(idx)+ offsetX*2,pos3y(idx),'b.','markersize',30)
plot(pos4x(idx)+ offsetX*2,pos4y(idx),'b.','markersize',30)
plot(pos5x(idx)+ offsetX*2,pos5y(idx),'b.','markersize',30)
plot(pos6x(idx)+ offsetX*2,pos6y(idx),'b.','markersize',30)
plot(pos7x(idx)+ offsetX*2,pos7y(idx),'b.','markersize',30)
plot(pos8x(idx)+ offsetX*2,pos8y(idx),'b.','markersize',30)
plot(pos9x(idx)+ offsetX*2,pos9y(idx),'b.','markersize',30)
plot(pos1xT(idx)+ offsetX*2,pos1yT(idx),'r.','markersize',30)
plot(pos2xT(idx)+ offsetX*2,pos2yT(idx),'r.','markersize',30)
plot(pos3xT(idx)+ offsetX*2,pos3yT(idx),'r.','markersize',30)
plot(pos4xT(idx)+ offsetX*2,pos4yT(idx),'r.','markersize',30)
plot(pos5xT(idx)+ offsetX*2,pos5yT(idx),'r.','markersize',30)
plot(pos6xT(idx)+ offsetX*2,pos6yT(idx),'r.','markersize',30)
plot(pos7xT(idx)+ offsetX*2,pos7yT(idx),'r.','markersize',30)
plot(pos8xT(idx)+ offsetX*2,pos8yT(idx),'r.','markersize',30)
plot(pos9xT(idx)+ offsetX*2,pos9yT(idx),'r.','markersize',30)

plot([offsetX*3  offsetX*3+0.24+cos(winkel1)*0.34],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',5) 
plot([offsetX*3  offsetX*3+1],[0 0],'k-','linewidth',3) 
plot([offsetX*3  offsetX*3],[0 3],'k-','linewidth',3) 
plot([offsetX*3+1  offsetX*3+1],[0 3],'k-','linewidth',3)
plot([offsetX*3  offsetX*3+0.24+cos(winkel1)*0.34],[1.445-sin(winkel1)*0.34 1.445+sin(winkel1)*0.34],'k-','linewidth',5) 
plot([offsetX*3  offsetX*3+1],[0 0],'k-','linewidth',3) 
plot([offsetX*3  offsetX*3],[0 3],'k-','linewidth',3) 
plot([offsetX*3+1  offsetX*3+1],[0 3],'k-','linewidth',3)
plot([offsetX*3 1+offsetX*3],[3 3],'k-','linewidth',5) 
idx=idx4;
plot(pos1x(idx)+ offsetX*3,pos1y(idx),'b.','markersize',30)
plot(pos2x(idx)+ offsetX*3,pos2y(idx),'b.','markersize',30)
plot(pos3x(idx)+ offsetX*3,pos3y(idx),'b.','markersize',30)
plot(pos4x(idx)+ offsetX*3,pos4y(idx),'b.','markersize',30)
plot(pos5x(idx)+ offsetX*3,pos5y(idx),'b.','markersize',30)
plot(pos6x(idx)+ offsetX*3,pos6y(idx),'b.','markersize',30)
plot(pos7x(idx)+ offsetX*3,pos7y(idx),'b.','markersize',30)
plot(pos8x(idx)+ offsetX*3,pos8y(idx),'b.','markersize',30)
plot(pos9x(idx)+ offsetX*3,pos9y(idx),'b.','markersize',30)
plot(pos1xT(idx)+ offsetX*3,pos1yT(idx),'r.','markersize',30)
plot(pos2xT(idx)+ offsetX*3,pos2yT(idx),'r.','markersize',30)
plot(pos3xT(idx)+ offsetX*3,pos3yT(idx),'r.','markersize',30)
plot(pos4xT(idx)+ offsetX*3,pos4yT(idx),'r.','markersize',30)
plot(pos5xT(idx)+ offsetX*3,pos5yT(idx),'r.','markersize',30)
plot(pos6xT(idx)+ offsetX*3,pos6yT(idx),'r.','markersize',30)
plot(pos7xT(idx)+ offsetX*3,pos7yT(idx),'r.','markersize',30)
plot(pos8xT(idx)+ offsetX*3,pos8yT(idx),'r.','markersize',30)
plot(pos9xT(idx)+ offsetX*3,pos9yT(idx),'r.','markersize',30)

