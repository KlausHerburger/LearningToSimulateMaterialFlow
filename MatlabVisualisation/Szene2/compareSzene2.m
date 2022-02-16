%%
clear
load Szene2/30_1_9.mat
winkel1 = 45*pi/180;
offset = 0;

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

figure(1)
h_fig = figure(1);
axis equal 
xlim([-0.2,1.2 + offset]);
ylim([-0.2,3.2]);

for idx = 1:5:length(pos1x)
    figure(h_fig); cla; hold on;
    plot([0.24-cos(winkel1)*0.35 0.24+cos(winkel1)*0.35],[1.47-sin(winkel1)*0.35 1.47+sin(winkel1)*0.35],'k-','linewidth',6)
    plot([0 1],[3 3],'k-','linewidth',6)  
    plot([0 1],[0 0],'k-','linewidth',2) 
    plot([offset 1+offset],[0 0],'k-','linewidth',2) 
    plot([0 0],[0 3],'k-','linewidth',2) 
    plot([1 1],[0 3],'k-','linewidth',2)
    plot([offset offset],[0 3],'k-','linewidth',2) 
    plot([1+offset 1+offset],[0 3],'k-','linewidth',2)
    plot([0.24-cos(winkel1)*0.35+offset 0.24+cos(winkel1)*0.35+offset],[1.47-sin(winkel1)*0.35 1.47+sin(winkel1)*0.35],'k-','linewidth',6)
    plot([0+offset 1+offset],[3 3],'k-','linewidth',6) 
    plot(pos1x(idx)+offset,pos1y(idx),'b.','markersize',30)
    plot(pos2x(idx)+offset,pos2y(idx),'b.','markersize',30)
    plot(pos3x(idx)+offset,pos3y(idx),'b.','markersize',30)
    plot(pos4x(idx)+offset,pos4y(idx),'b.','markersize',30)
    plot(pos5x(idx)+offset,pos5y(idx),'b.','markersize',30)
    plot(pos6x(idx)+offset,pos6y(idx),'b.','markersize',30)
    plot(pos7x(idx)+offset,pos7y(idx),'b.','markersize',30)
    plot(pos8x(idx)+offset,pos8y(idx),'b.','markersize',30)
    plot(pos9x(idx)+offset,pos9y(idx),'b.','markersize',30)
    plot(pos1xT(idx),pos1yT(idx),'r.','markersize',30)
    plot(pos2xT(idx),pos2yT(idx),'r.','markersize',30)
    plot(pos3xT(idx),pos3yT(idx),'r.','markersize',30)
    plot(pos4xT(idx),pos4yT(idx),'r.','markersize',30)
    plot(pos5xT(idx),pos5yT(idx),'r.','markersize',30)
    plot(pos6xT(idx),pos6yT(idx),'r.','markersize',30)
    plot(pos7xT(idx),pos7yT(idx),'r.','markersize',30)
    plot(pos8xT(idx),pos8yT(idx),'r.','markersize',30)
    plot(pos9xT(idx),pos9yT(idx),'r.','markersize',30)    
    %pause(0.01)
%
end