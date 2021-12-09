from numpy.core.fromnumeric import size
import cv2 
import numpy as np
import argparse
import os 
import sys

class Reconstruct_3D:               #define parameter of the camera.
    def __init__(self):
        self.Left_Camera_K = np.array([[1496.880651,0.000000,605.175810],
                                      [0.000000,1490.679493,338.418796],
                                      [0.000000,0.000000,1.000000]])
        self.Left_Camera_RT= np.array([[1.0,0.0,0.0,0.0],
                                       [0.0,1.0,0.0,0.0],
                                       [0.0,0.0,1.0,0.0]])
        self.Left_Camera_P = self.Left_Camera_K.dot(self.Left_Camera_RT)
        self.Left_Camera_p1 = self.Left_Camera_P[0,:]
        self.Left_Camera_p2 = self.Left_Camera_P[1,:]
        self.Left_Camera_p3 = self.Left_Camera_P[2,:]

        self.Right_Camera_K = np.array([[1484.936861,0.000000,625.964760],
                                       [0.000000,1480.722847,357.750205],
                                       [0.000000,0.000000,1.000000]])
        self.Right_Camera_RT = np.array([[0.893946,0.004543,0.448151,-186.807456],
                                        [0.013206,0.999247,-0.036473,3.343985],
                                        [-0.447979,0.038523,0.893214,45.030463]])
        self.Right_Camera_P = self.Right_Camera_K.dot(self.Right_Camera_RT)                                
        self.Fundamental_Matrix = np.array([[0.000000191234,0.000003409602,-0.001899934537 ],
                                            [0.000003427498,-0.000000298416,-0.023839273818 ],
                                            [-0.000612047140,0.019636148869,1.000000000000 ]])
        self.Right_Camera_p1 = self.Right_Camera_P[0,:]
        self.Right_Camera_p2 = self.Right_Camera_P[1,:]
        self.Right_Camera_p3 = self.Right_Camera_P[2,:]
    

def ARGS():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", '-p', help="Image file's folder path", type=str, required=True)
    # parser.add_argument("--output_folder", "-o", help="Output folder path", type = str, default="./")
    # parser.add_argument("--area", '-a', help="Area limit", type=int, default=2000)
    
    return parser.parse_args()


if __name__=='__main__':
    args = ARGS()
    folder_path = args.path
    files = os.listdir(folder_path)
    stereo = Reconstruct_3D()
    a = np.array([[0,0,0],[0,0,0]])     #Save coordinates of 3D.

    for i in files:
        img = cv2.imread(os.path.join(folder_path , i),0)
        # img_RGB = cv2.imread(os.path.join(folder_path , i))     #draw Feature points in image.
        row,col = img.shape    
        img1 = img[:,0:int(col/2)]      # Split image into left images.
        img2 = img[:,int(col/2):col:]   # Split image into right images.
        img1_point = img1.copy()      
        img2_point = img2.copy()
        
        sorted_img1 = np.argsort(-img1_point,axis=1)     #Pick out the brightestpixel in each row in image1.
        sorted_img2 = np.argsort(-img2_point,axis=1)     #Pick out the brightestpixel in each row in image2.

        x = np.array([sorted_img1[:,0],np.linspace(0,sorted_img1.shape[0]-1,sorted_img1.shape[0],endpoint=True),np.ones(sorted_img1.shape[0])])  #Save coordinates to matrix of x.
        xp = np.array([sorted_img2[:,0],np.linspace(0,sorted_img2.shape[0]-1,sorted_img2.shape[0],endpoint=True),np.ones(sorted_img1.shape[0])]) #Save coordinates to matrix of xp.
        lp =  stereo.Fundamental_Matrix.dot(x)   #define FX = l' , l' = [a b c]T , ax+by+c = 0   
        
        for jj in range(lp.shape[1]):

            if(img1_point[int(x[1,jj]),int(x[0,jj])]> 70):  #Limit the range of light.

                lp_ = np.array([[lp[0,jj]],[lp[1,jj]],[lp[2,jj]]])
                err_values = np.absolute((xp.T).dot(lp_))  #define x'^T.dot(F.dot(X)) = 0 
                err_sort = np.argsort(err_values,axis=0)   #Find the smallest error.

                if err_values[err_sort[0,0],0] <= 0.8  :     # 0.05 Tolerance error      and img2_point[int(xp[1,jj]),int(xp[0,err_sort[0,0]])] > 70 
                             
                    x1  = np.array([int(x[0,jj]),int(x[1,jj]),1]) 
                    xp2 = np.array([ xp[0,err_sort[0,0]] ,xp[1,jj], xp[2,jj] ])

                    A = np.array([x1[0]*stereo.Left_Camera_p3 - stereo.Left_Camera_p1,      #By handout equation of 3D Direct Triangulation method.       
                                    x1[1]*stereo.Left_Camera_p3 - stereo.Left_Camera_p2,
                                    xp2[0]*stereo.Right_Camera_p3 - stereo.Right_Camera_p1,
                                    xp2[1]*stereo.Right_Camera_p3 - stereo.Right_Camera_p2])

                    U,S,V = np.linalg.svd(A, full_matrices=True)    #Use SVD to get matrix of V.
                    X = np.array([V[-1,:]])
                    X = (X/X[0,-1]).T

                    X_check = np.absolute(X)
                    if X_check[2,0]<400:                             #According to the XYZ file, the range of z is within 400.
                        xp_dif = stereo.Right_Camera_P.dot(X)        #Verifying 3D re-projection error.
                        xp_dif = xp_dif/xp_dif[-1]
                    else:
                        continue
                    if np.absolute(xp2[0]- xp_dif[0]) < 50 and  np.absolute(xp2[1]- xp_dif[1]) < 50: #Tolerance error   
                        # cv2.circle(img_RGB,(int(x1[0]),int(x1[1])),1,(255,255,0),0)           #draw Feature points in image.
                        # cv2.circle(img_RGB,(1279+ int(xp2[0]),int(xp2[1])),1,(0,255,0),0)
                        a = np.vstack((a,(X[0:3,0]).T))                                         #3D data stored in the matrix of a.
                else:
                    continue
            else:
                continue
        # cv2.imwrite('./feature/{0}'.format(str(i)),img_RGB)

    #Output matrix a to M10907305.xyz.
    with open('{0}.xyz'.format(str('M10907305')),'w') as f:
        for i in range(2,a.shape[0]):
            f.write(str(a[i,0])+' '+str(a[i,1])+' '+str(a[i,2]))
            f.write('\n')
    f.close()
    print('finish')         



