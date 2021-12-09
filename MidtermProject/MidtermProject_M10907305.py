from numpy.core.fromnumeric import size
import cv2
import numpy as np
import os

class Panorama_Stitching :
    def __init__(self,img1,img2,img3,img4):
        self.sift = cv2.xfeatures2d.SIFT_create()
    def sift_(self,img1,img2,img3,img4):
        self.kp1,self.des1 = self.sift.detectAndCompute(img1,None)
        self.kp2,self.des2 = self.sift.detectAndCompute(img2,None)
        self.kp3,self.des3 = self.sift.detectAndCompute(img3,None)
        self.kp4,self.des4 = self.sift.detectAndCompute(img4,None)

    def drawimage(self,img_right,img_left,kp1,des1,kp2,des2,values):
        self.matches = cv2.BFMatcher().knnMatch(des1,des2, k=2)
        self.good = [m for m, n in self.matches if m.distance < 0.25*n.distance]
        if(len(self.good) > 4):
            #Analyze descriptors into general coordinates.
            self.src_pts = np.float32([ kp1[m.queryIdx].pt for m in self.good ]).reshape(-1,1,2)
            self.dst_pts = np.float32([ kp2[m.trainIdx].pt for m in self.good ]).reshape(-1,1,2)
            #use Homography to find the H matrix.
            self.H, self.mask = cv2.findHomography(self.src_pts, self.dst_pts, cv2.RANSAC,5.0)
            #Draw corresponding MARKs on images.
            matchesMask = self.mask.ravel().tolist()
            draw_params = dict(matchColor = (255,0,0), # draw matches in green color
                singlePointColor = None,
                matchesMask = matchesMask, # draw only inliers
                flags = 2)
            img_match = cv2.drawMatches(img_right.copy(),kp1,img_left.copy(),kp2,self.good,None,**draw_params)
            cv2.imwrite("./result/drawMatches{0}.jpg".format(str(values)),img_match)
            print('\n{0}:image_left\n'.format(str(values)),self.dst_pts)
            print('\n{0}:image_right\n'.format(str(values)),self.src_pts)

    def sift_function(self,img_right,img_left,kp1,des1,kp2,des2,values):

        # use sift to find the descriptors of the two photos.
        self.matches = cv2.BFMatcher().knnMatch(des1,des2,k=2)
        self.good = [m for m, n in self.matches if m.distance < 0.25*n.distance]
        if(len(self.good) > 4):
            #Analyze descriptors into general coordinates.
            self.src_pts = np.float32([kp1[m.queryIdx].pt for m in self.good ]).reshape(-1,1,2)
            self.dst_pts = np.float32([kp2[m.trainIdx].pt for m in self.good ]).reshape(-1,1,2)
        
            if values >=1:
                self.conver_dst_pts = np.pad(self.dst_pts,((0,0),(0,0),(0,1)),'constant',constant_values = 1)
                self.data_dst_pts = []
                for i in range(0,self.dst_pts.shape[0]):
                    # print(self.conver_dst_pts[i,0,:])
                    a = self.conver_dst_pts[i,0,:].reshape(self.conver_dst_pts[i,0,:].shape[0],1)
                    a1 = self.H.dot(a)
                    a2 = a1/a1[2]
                    self.dst_pts[i,:,0] = a2[0]
                    self.dst_pts[i,:,1] = a2[1]
                    # print(a2)
            # print('\n{0}:image_left\n'.format(str(values)),self.dst_pts)
            # print('\n{0}:image_right\n'.format(str(values)),self.src_pts)

            #use Homography to find the H matrix.
            self.H, self.mask = cv2.findHomography(self.src_pts, self.dst_pts, cv2.RANSAC,5.0)
            # print('\n',self.H)
            self.Perspective_img1 = cv2.warpPerspective(img_right,self.H,(img_right.shape[1]+img_left.shape[1],img_right.shape[0]))
            # cv2.imshow('img{0}'.format(str(values)),self.Perspective_img1)
            
            #prcessing overlapping problem.
            img_ = cv2.copyMakeBorder(img_left.copy(),0,0,0,int(self.Perspective_img1.shape[1]-img_left.shape[1]),cv2.BORDER_CONSTANT)
            self.result = cv2.subtract(self.Perspective_img1,img_)
            self.result = cv2.add(self.result,img_)     
            # cv2.imshow('img',self.result)       
            # cv2.waitKey(0)
            # cv2.imwrite("./result/drawMatches{0}.jpg".format(str(values)),img_match)
            cv2.imwrite("./result/stitching{0}1.jpg".format(str(values)),self.result)
            # return 0
            return self.result
        else:
            return 0
if __name__=='__main__':
    #read image and resize image. 
    img1 = cv2.imread('004.JPG')
    img2 = cv2.imread('003.JPG') 
    img3 = cv2.imread('002.JPG')
    img4 = cv2.imread('001.JPG')

    #reduce computing time, but many messages will disappear.
    # img1 = cv2.resize(img1,(375,500),interpolation=cv2.INTER_AREA)
    # img2 = cv2.resize(img2,(375,500),interpolation=cv2.INTER_AREA)
    # img3 = cv2.resize(img3,(375,500),interpolation=cv2.INTER_AREA)
    # img4 = cv2.resize(img4,(375,500),interpolation=cv2.INTER_AREA)

    # Add image black border.
    img1 = cv2.copyMakeBorder(img1,int(img1.shape[0]/2),int(img1.shape[0]/2),0,0,cv2.BORDER_CONSTANT)
    img2 = cv2.copyMakeBorder(img2,int(img2.shape[0]/2),int(img2.shape[0]/2),0,0,cv2.BORDER_CONSTANT)
    img3 = cv2.copyMakeBorder(img3,int(img3.shape[0]/2),int(img3.shape[0]/2),0,0,cv2.BORDER_CONSTANT)
    img4 = cv2.copyMakeBorder(img4,int(img4.shape[0]/2),int(img4.shape[0]/2),0,0,cv2.BORDER_CONSTANT)
    
    #Stitching processing
    Stitching = Panorama_Stitching(img1,img2,img3,img4)
    Stitching.sift_(img1,img2,img3,img4)

    #draw image
    Stitching.drawimage(img1,img2,Stitching.kp1,Stitching.des1,Stitching.kp2,Stitching.des2,1)
    Stitching.drawimage(img2,img3,Stitching.kp2,Stitching.des2,Stitching.kp3,Stitching.des3,2)
    Stitching.drawimage(img3,img4,Stitching.kp3,Stitching.des3,Stitching.kp4,Stitching.des4,3)

    # Stitching image
    img_stitching1 = Stitching.sift_function(img2,img1,Stitching.kp2,Stitching.des2,Stitching.kp1,Stitching.des1,0)
    img_stitching2 = Stitching.sift_function(img3,img_stitching1,Stitching.kp3,Stitching.des3,Stitching.kp2,Stitching.des2,1)
    img_stitching3 = Stitching.sift_function(img4,img_stitching2,Stitching.kp4,Stitching.des4,Stitching.kp3,Stitching.des3,2)

    cv2.imshow('img',img_stitching3)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
