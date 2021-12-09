function [result] = homography(pA1,pA2,pA3,pA4,pB1,pB2,pB3,pB4)

%-------------------------選取採樣點-----------------------------

Aab=[0 0 0 -pB1(3)*pA1' pB1(2)*pA1';
     pB1(3)*pA1' 0 0 0 -pB1(1)*pA1';
     0 0 0 -pB2(3)*pA2' pB2(2)*pA2'; 
     pB2(3)*pA2' 0 0 0 -pB2(1)*pA2';
     0 0 0 -pB3(3)*pA3' pB3(2)*pA3'; 
     pB3(3)*pA3' 0 0 0 -pB3(1)*pA3';
     0 0 0 -pB4(3)*pA4' pB4(2)*pA4'; 
     pB4(3)*pA4' 0 0 0 -pB4(1)*pA4';];
 
[~,~,V] = svd(Aab);
Hab = [V(1:3,9)';V(4:6,9)';V(7:9,9)';];
result = Hab./Hab(3,3);
end