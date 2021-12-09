function [P] = find_projection_M (X1,X2,X3,X4,X5,X6,uv1,uv2,uv3,uv4,uv5,uv6)

zero=[0,0,0,0]';

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

[~,~,V] = svd(Puvmatrix);
Hab = [V(1:4,12)';V(5:8,12)';V(9:12,12)';];
P = Hab./Hab(3,4);
end
