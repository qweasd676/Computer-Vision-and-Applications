from os.path import splitext
from numpy.core.numeric import ones
import cv2
import os , sys
import numpy as np
import time




class voxel_parameter:
    Instrisic_Parameter = np.array([[722.481995 ,0 ,399.000000],
                            [0.000000,722.481934, 311.000000],
                            [0.000000, 0.000000, 1.000000]])
    def __init__(self,image_name):
        if(image_name == '01.bmp'):
            self.Exstrisic_Parameter = np.array([[0.508468, 0.860935, -0.015857, 3.932282],
                                        [-0.101237, 0.041482, -0.994003 ,21.303495],
                                        [-0.855111, 0.507022, 0.108232, 88.085114]])

        elif(image_name == '02.bmp'):
            self.Exstrisic_Parameter = np.array([[0.054555, 0.997525 ,0.044349 ,-0.396882],
                                        [-0.129876, 0.051127, -0.990217, 21.030863],
                                        [-0.990031, 0.048262, 0.132325, 86.551529]])

        elif(image_name == '03.bmp'):
            self.Exstrisic_Parameter = np.array([[-0.483178, 0.864219, 0.140232 ,-6.133193],
                                        [-0.118992,0.093863, -0.988454, 21.073915],
                                        [-0.867401, -0.494281, 0.057464, 88.905014]])
        elif(image_name == '04.bmp'):
            self.Exstrisic_Parameter = np.array([[-0.826707, 0.562054 ,0.025509 ,-3.706015],
                                        [-0.015798 ,0.022133, -0.999636 ,22.618803],
                                        [-0.562411, -0.826804 ,-0.009437, 89.343170]])
        elif(image_name == '05.bmp'):
            self.Exstrisic_Parameter = np.array([[-0.920328 ,-0.386141, 0.062375, 0.837949],
                                        [-0.102550, 0.084312, -0.991155, 20.728113],
                                        [0.377463, -0.918577 ,-0.117211, 93.253716]])
        elif(image_name == '06.bmp'):
            self.Exstrisic_Parameter = np.array([[-0.315707, -0.948836 ,-0.006217 ,2.520231],
                                        [-0.091609 ,0.037001 ,-0.995114,20.983803],
                                        [0.944422, -0.313592, -0.098622 ,93.845718]])
        elif(image_name == '07.bmp'):
            self.Exstrisic_Parameter = np.array([[0.547250 ,-0.836131, -0.037448 ,-5.300584],
                                        [-0.082565 ,-0.009407 ,-0.996548, 21.209290],
                                        [0.832886 ,0.548449 ,-0.074202, 91.918419]])
        elif(image_name == '08.bmp'):
            self.Exstrisic_Parameter = np.array([[0.998758, -0.047722 ,-0.014321 ,7.249783],
                                        [-0.026645 ,-0.268707 ,-0.962861, 16.707335],
                                        [0.042101 ,0.962035 ,-0.269661 ,101.258018]])
        elif(image_name == '09.bmp'):
            self.Exstrisic_Parameter = np.array([[0.515633 ,0.856808 ,0.001705, 1.082603],
                                        [0.856751 ,-0.515573, -0.013213, 4.623665],
                                        [-0.010425 ,0.008264, -0.999911, 114.083206]])
        elif(image_name == '10.bmp'):
            self.Exstrisic_Parameter = np.array([[-0.164361, 0.974144 ,-0.155012, 2.258266],
                                        [-0.915024 ,-0.209267 ,-0.344892, 8.572358],
                                        [-0.368429, 0.085148, 0.925748, 76.273094]])
        elif(image_name == '11.bmp'):
            self.Exstrisic_Parameter = np.array([[-0.053241 ,0.998369, 0.020604 ,1.405633],
                                        [-0.737301 ,-0.053217, 0.673473 ,-20.414452],
                                        [0.673454 ,0.020664, 0.738940, 80.795265]])

 

if __name__=='__main__':
    object_3D = np.ones([101,101,101])
    img_position = input('enter picture postion:')
    files = os.listdir(img_position)
    for img in files:
        root, extension = os.path.splitext(img)
        print(img)
        if(extension == '.bmp'):
            img_name = cv2.imread(os.path.join(img_position , img),0)
            row,col = img_name.shape
            voxel_3D = voxel_parameter(img)
            start_time = time.time()
            for i in range(0,101,1):
                for j in range(-50,51,1):
                    for k in range(-50,51,1):    
                        if(object_3D[j+50,k+50,i] == 1 ):
                            two_dim = np.dot(np.dot(voxel_3D.Instrisic_Parameter,voxel_3D.Exstrisic_Parameter),np.array([[k],[j],[i],[1]]))

                            two_dim =np.round(two_dim/two_dim[2])
                            two_dim = two_dim.astype(int)

                            if( (two_dim[0] > col) or (two_dim[0] < 0) or (two_dim[1] > row) or (two_dim[1] < 0) ):
                                object_3D[j+50,k+50,i] = 0
                            else:
                                if(img_name[two_dim[1]-1,two_dim[0]-1]  == 0):
                                    object_3D[j+50,k+50,i] = 0
            end_time = time.time()
            print(( end_time - start_time))

    print(object_3D.shape)    
    with open('{0}.xyz'.format(str(img_position)),'w') as f:
        for i in range(0,101,1):
            for j in range(0,101,1):
                for k in range(0,101,1):
                    if(object_3D[j,k,i] == 1):
                        f.write(str(k-50)+' '+str(j-50)+' '+str(i))
                        f.write('\n')
    f.close()
    

                    
                    

