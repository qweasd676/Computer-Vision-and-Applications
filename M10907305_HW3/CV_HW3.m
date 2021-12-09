clc;clear;
% defind the k(intrinsic parameter) and coordinates of 2D,3D and sabta_claus .
k = [1308.36,0.00,780.00;0.00,1308.36,480.50;0.00,0.00,1.00]
sabta_claus = [-4.5,-2.5,130,1]';
X1 =[0,50,0,1]';
X2 = [-100,50,0,1]';
X3 = [0,50,100,1]';
X4 = [50,-50,50,1]';
X5 = [50,-100,50,1]';
X6 = [50,-100,0,1]';
uv1 = [655,668,1]';
uv2 = [836,305,1]';
uv3 = [296,667,1]';
uv4 = [603,1149,1]';
uv5 = [709,1364,1]';
uv6 = [889,1305,1]';

% Using Gold standard algorithm.
[T_2D T_3D] = Goldstandard(X1,X2,X3,X4,X5,X6,uv1,uv2,uv3,uv4,uv5,uv6);
% % % Update all coordinate of data.
X11 = T_3D*X1;
X21 = T_3D*X2;
X31 = T_3D*X3;
X41 = T_3D*X4;
X51 = T_3D*X5;
X61 = T_3D*X6;
uv11 = T_2D*uv1;
uv21 = T_2D*uv2;
uv31 = T_2D*uv3;
uv41 = T_2D*uv4;
uv51 = T_2D*uv5;
uv61 = T_2D*uv6;

% Find the projection matrix.
P  = Puvmatrix(X11,X21,X31,X41,X51,X61,uv11,uv21,uv31,uv41,uv51,uv61,T_2D,T_3D);
% P  = Puvmatrix(X1,X2,X3,X4,X5,X6,uv1,uv2,uv3,uv4,uv5,uv6);
uv = P*X1;
uv = uv./uv(end)

% calculate the 2D coordiate of sabta claus
sabta_claus_2D = P*sabta_claus;
sabta_claus_2D = sabta_claus_2D./sabta_claus_2D(3)

% Derive RT matrix and calculate distance vector between the target and
% camera.
RT = inv(k)*P;
RT = RT./(sqrt(sum(RT(:,1).^2)))
target = RT*sabta_claus
distance = norm(target)
% vector = RT(:,end)-sabta_claus(1:end-1)
% distance = norm(vector)

function [T_2D T_3D] = Goldstandard(X1,X2,X3,X4,X5,X6,uv1,uv2,uv3,uv4,uv5,uv6)
centroid_x_3D = fix((X1(1)+X2(1)+X3(1)+X4(1)+X5(1)+X6(1))/6); 
centroid_y_3D = fix((X1(2)+X2(2)+X3(2)+X4(2)+X5(2)+X6(2))/6);
centroid_z_3D = fix((X1(3)+X2(3)+X3(3)+X4(3)+X5(3)+X6(3))/6);
centroid_x_2D = fix((uv1(1)+uv2(1)+uv3(1)+uv4(1)+uv5(1)+uv6(1))/6);
centroid_y_2D = fix((uv1(2)+uv2(2)+uv3(2)+uv4(2)+uv5(2)+uv6(2))/6);
centorid_3D = cat(2,centroid_x_3D,centroid_y_3D,centroid_z_3D);
centorid_2D = cat(2,centroid_x_2D,centroid_y_2D);
S_3D = sqrt(2)/(sqrt(sum((centorid_3D-X1(end-1)).^2))+sqrt(sum((centorid_3D-X2(end-1)).^2))+sqrt(sum((centorid_3D-X3(end-1)).^2))+...
sqrt(sum((centorid_3D-X4(end-1)).^2))+sqrt(sum((centorid_3D-X5(end-1)).^2))+sqrt(sum((centorid_3D-X6(end-1)).^2))/6);
S_2D = sqrt(2)/(sqrt(sum((centorid_2D-uv1(end-1)).^2))+sqrt(sum((centorid_2D-uv2(end-1)).^2))+sqrt(sum((centorid_2D-uv3(end-1)).^2))+...
sqrt(sum((centorid_2D-uv4(end-1)).^2))+sqrt(sum((centorid_2D-uv5(end-1)).^2))+sqrt(sum((centorid_2D-uv6(end-1)).^2))/6);
T_3D =  [S_3D 0 0 -S_3D*centroid_x_3D ; 0 S_3D 0 -S_3D*centroid_y_3D; 0 0 S_3D -S_3D*centroid_z_3D; 0 0 0 1]
T_2D =  [S_2D 0 -S_2D*centroid_x_2D ; 0 S_2D -S_2D*centroid_y_2D; 0 0 1]
end

function [P] = Puvmatrix(X1,X2,X3,X4,X5,X6,uv1,uv2,uv3,uv4,uv5,uv6,T_2D,T_3D)
% function [P] = Puvmatrix(X1,X2,X3,X4,X5,X6,uv1,uv2,uv3,uv4,uv5,uv6)
zero = [0 0 0 0]';
Puvmatrix=[  X1'    zero' -uv1(1).*X1';
   zero'  X1'   -uv1(2).*X1';
   X2'    zero' -uv2(1).*X2';
   zero'  X2'   -uv2(2).*X2';
   X3'    zero' -uv3(1).*X3';
   zero'  X3'   -uv3(2).*X3';
   X4'    zero' -uv4(1).*X4';
   zero'  X4'   -uv4(2).*X4';
   X5'    zero' -uv5(1).*X5';
   zero'  X5'   -uv5(2).*X5';
   X6'    zero' -uv6(1).*X6';
   zero'  X6'   -uv6(2).*X6';];
[U,S,V] = svd(Puvmatrix);
P = [V(1:4,12)';V(5:8,12)';V(9:12,12)'];
P = inv(T_2D)*P*T_3D;
P = P./P(end)
end