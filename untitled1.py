# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 19:27:25 2023

@author: Amir
"""

from pymem import  *
from pymem.process import  *
import cv2
import numpy as np
import math


pm = pymem.Pymem("gta-vc.exe")

game_module = module_from_name(pm.process_handle, "gta-vc.exe").lpBaseOfDll


for i in range(300):
    a = pm.read_bytes(game_module + 0x38F834 + (i-30)*0x28, 4)
    
    
    try:
        b = pm.read_float(int.from_bytes(a[::-1], "big") + 0x34 )
        b = pm.read_float(int.from_bytes(a[::-1], "big") + 0x38 )
        # b = pm.read_float(int.from_bytes(a[::-1], "big") + 0x3c )
        
        print(b)
        
        # pm.write_float(int.from_bytes(a[::-1], "big") + 0x34 , 30.0)
        # pm.write_float(int.from_bytes(a[::-1], "big") + 0x38 , 30.0)
        # pm.write_float(int.from_bytes(a[::-1], "big") + 0x3c , 30.0)
        
    except:
        pass
    
    # print(a)
    # print(int.from_bytes(a[::-1], "big"))
    # print(a[::-1].hex())
    
# img_1 = np.zeros([1024,1024,1],dtype=np.uint8)

img_size = (1024, 1024)
white_img = np.ones((img_size[0], img_size[1], 3), dtype=np.uint8) * 255

while(True):

    show =  white_img.copy()
    
    cv2.rectangle(show, (img_size[0]//2 -6, img_size[1]//2 -6), (img_size[0]//2 +6, img_size[1]//2 +6), (0, 255, 0), thickness=-1)
    y, x = pm.read_float( game_module + 0x3E4934), pm.read_float( game_module + 0x3E4930)
    angle = math.atan2(pm.read_float( game_module + 0x3E4978), pm.read_float( game_module + 0x3E497C))
    angle_degrees = math.degrees(angle)


    center = (img_size[0]//2, img_size[1]//2)
    side_length = 10
    pt1 = (center[0], center[1] + int(side_length//1.2))
    pt2 = (center[0] - side_length//2, center[1] - side_length//2)
    pt3 = (center[0] + side_length//2, center[1] - side_length//2)
    cv2.drawContours(show, [np.array([pt3, pt2, pt1])], 0, (0, 0, 0), thickness=-1)
    M = cv2.getRotationMatrix2D(center, angle_degrees, 1.0)
    rotated_triangle = cv2.warpAffine(show, M, img_size)
    
    show[img_size[0]//2 -25:img_size[0]//2+25,
         img_size[1]//2 -25:img_size[1]//2+25] = rotated_triangle[img_size[0]//2-25:img_size[0]//2+25,
                                                                  img_size[1]//2-25:img_size[1]//2+25]  
    
    for i in range(350):
        a = pm.read_bytes(game_module + 0x38FA14 + (i-10)*0x28, 4)
        try:
            tx = pm.read_float(int.from_bytes(a[::-1], "big") + 0x34 )
            ty = pm.read_float(int.from_bytes(a[::-1], "big") + 0x38 )
            hp = pm.read_float(int.from_bytes(a[::-1], "big") + 0x354 )
            if (ty-y) and (tx-x) and (tx-x)*2<img_size[0] and (ty-y)*2<img_size[1]:
                
                if(hp > 10):
                    #people
                    cv2.rectangle(show , (int(img_size[0]//2 -2+(tx-x)*2), int(img_size[1]//2 -2 +(ty-y)*2)),
                                         (int(img_size[0]//2 +2+(tx-x)*2), int(img_size[1]//2 +2 +(ty-y)*2)),
                                         (0, 0, 255), thickness=-1)
                else:
                    #car
                    cv2.rectangle(show , (int(img_size[0]//2 -4+(tx-x)*2), int(img_size[1]//2 -4+(ty-y)*2)),
                                         (int(img_size[0]//2 +4+(tx-x)*2), int(img_size[1]//2 +4+(ty-y)*2)), 
                                         (0, 255, 255), thickness=-1)
        except:
            pass
    

    
    # Display the resulting frame
    cv2.imshow('Frame',show )
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
 









