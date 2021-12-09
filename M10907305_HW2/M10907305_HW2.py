import cv2 
import numpy as np


class homography:

    def __init__(self,img_src):
        self.img_src = img_src

    def Perspective(self,img_srcPoint,img_dstPoint):
        mask = np.zeros(self.img_src.shape, np.uint8)
        mask = cv2.polylines(mask,[img_srcPoint],True, (255,255,255),1,cv2.LINE_AA )
        mask2 = cv2.fillPoly(mask.copy(), [img_srcPoint], (255, 255, 255),cv2.LINE_AA)
        ROI = cv2.bitwise_and(mask2, self.img_src.copy())
        M ,H = cv2.findHomography(img_srcPoint,img_dstPoint, cv2.RANSAC,5.0)
        Perspective_img = cv2.warpPerspective(ROI,M,(ROI.shape[1],ROI.shape[0]), borderMode=cv2.BORDER_CONSTANT, flags=cv2.INTER_LINEAR )
        img_fixed = cv2.cvtColor(Perspective_img.copy(),cv2.COLOR_BGR2GRAY)
        ret , img_binary= cv2.threshold(img_fixed,1,255,cv2.THRESH_BINARY)
        mask[:,:,0] = img_binary        #Convert to RGB image
        mask[:,:,1] = img_binary
        mask[:,:,2] = img_binary
        # print(mask2.shape,mask.shape)
        # cv2.imshow('mask',mask)
        # cv2.imshow('mask2',mask2)
        # cv2.imshow('img',Perspective_img)
        # cv2.waitKey(0)
        return ~mask,Perspective_img
    def combine_img(self,ROI1,ROI2,Perspective_img1,Perspective_img2):
        ROI = cv2.bitwise_and(ROI1&ROI2, self.img_src.copy())
        swap_ArtGallery = ROI + Perspective_img1 + Perspective_img2
        # cv2.imshow('ROI1',ROI)
        # cv2.imshow('ROI2',swap_ArtGallery)
        # cv2.waitKey(0)
        cv2.imwrite('M10907305.jpg',swap_ArtGallery)
        
if __name__=='__main__':
    img_srcPoint = np.array([[40,103],[43,446],[341,426],[340,123]])            #define image_1 point
    img_dstPoint = np.array([[684,119],[681,452],[959,516],[956,72]])           #define image_2 point
    img_src = cv2.imread("ArtGallery.jpg")                                      #read ArtGallery.jpg
    img_src_homography = img_src.copy()
    homography_ = homography(img_src_homography)
    ROI1 , Perspective_img1 = homography_.Perspective(img_srcPoint,img_dstPoint) #get homography and Perspective  by image1   
    ROI2 , Perspective_img2 = homography_.Perspective(img_dstPoint,img_srcPoint) #get homography and Perspective  by image2
    homography_.combine_img(ROI1,ROI2,Perspective_img1,Perspective_img2)         #combine image1 and image2
    
    # cv2.destroyAllWindows()