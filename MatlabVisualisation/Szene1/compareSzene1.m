%%
clear
load Szene1/5/20_3.mat
winkel = 20*pi/180;
offset = 0;

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


figure(1)
h_fig = figure(1);
axis equal 
xlim([-0.2,1.2+offset]);
ylim([-0.2,3.2]);

for idx = 1:10:length(pos1xT)
    figure(h_fig); cla; hold on;
    plot([0 0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',3) 
    plot([offset offset+0.24+cos(winkel)*0.34],[1.445-sin(winkel)*0.34 1.445+sin(winkel)*0.34],'k-','linewidth',3) 
    plot([0 1],[0 0],'k-','linewidth',2) 
    plot([offset 1+offset],[0 0],'k-','linewidth',2) 
    plot([0 0],[0 3],'k-','linewidth',2) 
    plot([1 1],[0 3],'k-','linewidth',2)
    plot([offset offset],[0 3],'k-','linewidth',2) 
    plot([1+offset 1+offset],[0 3],'k-','linewidth',2)
    plot(pos1x(idx),pos1y(idx),'b.','markersize',30)
    plot(pos2x(idx),pos2y(idx),'b.','markersize',30)
    plot(pos3x(idx),pos3y(idx),'b.','markersize',30)
    plot(pos4x(idx),pos4y(idx),'b.','markersize',30)
    plot(pos1xT(idx)+offset,pos1yT(idx),'r.','markersize',30)
    plot(pos2xT(idx)+offset,pos2yT(idx),'r.','markersize',30)
    plot(pos3xT(idx)+offset,pos3yT(idx),'r.','markersize',30)
    plot(pos4xT(idx)+offset,pos4yT(idx),'r.','markersize',30)
    pause(0.05)
%
end