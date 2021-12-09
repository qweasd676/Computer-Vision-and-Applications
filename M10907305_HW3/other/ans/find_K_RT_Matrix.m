function [K,RT_1,RT_2,RT_3] = find_K_RT_Matrix(w1,w2,w3,w4,t1A,t2A,t3A,t4A,t1B,t2B,t3B,t4B,t1C,t2C,t3C,t4C)

    ha = homography(w1,w2,w3,w4,t1A,t2A,t3A,t4A);
    hb = homography(w1,w2,w3,w4,t1B,t2B,t3B,t4B);
    hc = homography(w1,w2,w3,w4,t1C,t2C,t3C,t4C);
    hap = ha';
    hbp = hb';
    hcp = hc';
    A = [(hap(1,1)*hap(2,1)) (hap(1,1)*hap(2,2)+hap(1,2)*hap(2,1)) (hap(1,1)*hap(2,3)+hap(1,3)*hap(2,1)) (hap(1,2)*hap(2,2)) (hap(1,2)*hap(2,3)+hap(1,3)*hap(2,2)) (hap(1,3)*hap(2,3));
         (hap(1,1)^2-hap(2,1)^2) (2*(hap(1,1)*hap(1,2)-hap(2,1)*hap(2,2))) (2*(hap(1,1)*hap(1,3)-hap(2,1)*hap(2,3))) (hap(1,2)^2-hap(2,2)^2) (2*(hap(1,2)*hap(1,3)-hap(2,2)*hap(2,3))) (hap(1,3)^2-hap(2,3)^2);
         (hbp(1,1)*hbp(2,1)) (hbp(1,1)*hbp(2,2)+hbp(1,2)*hbp(2,1)) (hbp(1,1)*hbp(2,3)+hbp(1,3)*hbp(2,1)) (hbp(1,2)*hbp(2,2)) (hbp(1,2)*hbp(2,3)+hbp(1,3)*hbp(2,2)) (hbp(1,3)*hbp(2,3));
         (hbp(1,1)^2-hbp(2,1)^2) (2*(hbp(1,1)*hbp(1,2)-hbp(2,1)*hbp(2,2))) (2*(hbp(1,1)*hbp(1,3)-hbp(2,1)*hbp(2,3))) (hbp(1,2)^2-hbp(2,2)^2) (2*(hbp(1,2)*hbp(1,3)-hbp(2,2)*hbp(2,3))) (hbp(1,3)^2-hbp(2,3)^2);
         (hcp(1,1)*hcp(2,1)) (hcp(1,1)*hcp(2,2)+hcp(1,2)*hcp(2,1)) (hcp(1,1)*hcp(2,3)+hcp(1,3)*hcp(2,1)) (hcp(1,2)*hcp(2,2)) (hcp(1,2)*hcp(2,3)+hcp(1,3)*hcp(2,2)) (hcp(1,3)*hcp(2,3));
         (hcp(1,1)^2-hcp(2,1)^2) (2*(hcp(1,1)*hcp(1,2)-hcp(2,1)*hcp(2,2))) (2*(hcp(1,1)*hcp(1,3)-hcp(2,1)*hcp(2,3))) (hcp(1,2)^2-hcp(2,2)^2) (2*(hcp(1,2)*hcp(1,3)-hcp(2,2)*hcp(2,3))) (hcp(1,3)^2-hcp(2,3)^2); 
         ];
     [~,~,V] = svd(A);
     w = [V(1:3,6)';V(2,6) V(4:5,6)';V(3,6) V(5,6) V(6,6)];
     inw = inv(w);
     inw = inw./inw(3,3);
     c=inw(1,3);
     e=inw(2,3);
     d=sqrt(inw(2,2)-e^2);
     b=(inw(1,2)-c*e)/d;
     a=sqrt(inw(1,1)-b^2-c^2);
     K = [a b c; 0 d e; 0 0 1];
     
     ra = inv(K)*ha;
     ra_1 = ra(:,1);
     ra1_len = sqrt(ra_1(1)^2+ra_1(2)^2+ra_1(3)^2);
     ra_1 = ra_1./ ra1_len;
     ra_2 = ra(:,2);
     ra2_len = sqrt(ra_2(1)^2+ra_2(2)^2+ra_2(3)^2);
     ra_2 = ra_2./ ra2_len;
     ra_3 = cross(ra_1,ra_2);
     ra_2 = cross(ra_3,ra_1);
     t = inv(K)*ha(:,3)./ra1_len;
     RT_1 = [ra_1 ra_2 ra_3 t];
     
     rb = inv(K)*hb;
     rb_1 = rb(:,1);
     rb1_len = sqrt(rb_1(1)^2+rb_1(2)^2+rb_1(3)^2);
     rb_1 = rb_1./ rb1_len;
     rb_2 = rb(:,2);
     rb2_len = (rb_2(1)^2+rb_2(2)^2+rb_2(3)^2)^0.5;
     rb_2 = rb_2./ rb2_len;
     rb_3 = cross(rb_1,rb_2);
     rb_2 = cross(rb_3,rb_1);
     t = inv(K)*hb(:,3)./rb1_len;
     RT_2 = [rb_1 rb_2 rb_3 t];
     
     rc = inv(K)*hc;
     rc_1 = rc(:,1);
     rc1_len = (rc_1(1)^2+rc_1(2)^2+rc_1(3)^2)^0.5;
     rc_1 = rc_1./ rc1_len;
     rc_2 = rc(:,2);
     rb2_len = (rc_2(1)^2+rc_2(2)^2+rc_2(3)^2)^0.5;
     rc_2 = rc_2./ rb2_len;
     rc_3 = cross(rc_1,rc_2);
     rc_2 = cross(rc_3,rc_1);
     t = inv(K)*hc(:,3)./rc1_len;
     RT_3 = [rc_1 rc_2 rc_3 t];
end
