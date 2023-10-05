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


img_size = (1024, 1024)
white_img = np.ones((img_size[0], img_size[1], 3), dtype=np.uint8) * 255
center = (img_size[0]//2, img_size[1]//2)

while(True):

    show =  white_img.copy()
    
    #draw center rectangle 
    cv2.rectangle(show, (center[0]-6, center[1]-6), (center[0]+6, center[1]+6), (0, 255, 0), thickness=-1)
    
    #get player positions
    y, x = pm.read_float( game_module + 0x3E4934), pm.read_float( game_module + 0x3E4930)
    angle = math.atan2(pm.read_float( game_module + 0x3E4978), pm.read_float( game_module + 0x3E497C))
    angle_degrees = math.degrees(angle)

    #draw angle triangle
    side_length = 10
    pt1 = (center[0], center[1] + int(side_length//1.2))
    pt2 = (center[0] - side_length//2, center[1] - side_length//2)
    pt3 = (center[0] + side_length//2, center[1] - side_length//2)
    cv2.drawContours(show, [np.array([pt3, pt2, pt1])], 0, (0, 0, 0), thickness=-1)
    
    #rorate triangle
    M = cv2.getRotationMatrix2D(center, angle_degrees, 1.0)
    rotated_triangle = cv2.warpAffine(show, M, img_size)
    
    #replace center of show with rotated_triangle
    show[center[0]-25:center[0]+25,
         center[1]-25:center[1]+25] = rotated_triangle[center[0]-25:center[0]+25,
                                                       center[1]-25:center[1]+25]  
    
    #loop over objects(cars and people)
    for i in range(350):
        
        a = pm.read_bytes(game_module + 0x38FA14 + (i-10)*0x28, 4)
        try:
            byte_value = pm.read_bytes(int.from_bytes(a[::-1], "big") + 0x50, 1)[0] 
            type_object = byte_value & 0b111
            status = byte_value >> 3
            
            print(status)
            
            tx = pm.read_float(int.from_bytes(a[::-1], "big") + 0x34 )
            ty = pm.read_float(int.from_bytes(a[::-1], "big") + 0x38 )
            hp = pm.read_float(int.from_bytes(a[::-1], "big") + 0x354 )
            
            
            
            if(int_value == 2):
                cv2.rectangle(show , (int(center[0] -5+(tx-x)*2), int(center[1] -5 +(ty-y)*2)),
                                      (int(center[0] +5+(tx-x)*2), int(center[1] +5 +(ty-y)*2)),
                                      (255, 0, 255), thickness=-1)
            if(int_value == 4):
                cv2.rectangle(show , (int(center[0] -5+(tx-x)*2), int(center[1] -5 +(ty-y)*2)),
                                      (int(center[0] +5+(tx-x)*2), int(center[1] +5 +(ty-y)*2)),
                                      (168, 50, 166), thickness=-1)
            if(int_value == 5):
                cv2.rectangle(show , (int(center[0] -5+(tx-x)*2), int(center[1] -5 +(ty-y)*2)),
                                      (int(center[0] +5+(tx-x)*2), int(center[1] +5 +(ty-y)*2)),
                                      (64, 36, 209), thickness=-1)
            if(int_value == 10):
                cv2.rectangle(show , (int(center[0] -7+(tx-x)*2), int(center[1] -7 +(ty-y)*2)),
                                      (int(center[0] +7+(tx-x)*2), int(center[1] +7 +(ty-y)*2)),
                                      (82, 168, 50), thickness=-1)
            if(int_value == 11):
                cv2.rectangle(show , (int(center[0] -7+(tx-x)*2), int(center[1] -7 +(ty-y)*2)),
                                      (int(center[0] +7+(tx-x)*2), int(center[1] +7 +(ty-y)*2)),
                                      (52, 134, 235), thickness=-1)
                    
                
                
            
            if (ty-y) and (tx-x) and (tx-x)*2<center[0] and (ty-y)*2<center[1]:
                
                #people hp is 100 and car is near 0 in normal
                if(hp > 10):
                    #people
                    cv2.rectangle(show , (int(center[0] -2+(tx-x)*2), int(center[1] -2 +(ty-y)*2)),
                                         (int(center[0] +2+(tx-x)*2), int(center[1] +2 +(ty-y)*2)),
                                         (0, 0, 255), thickness=-1)
                else:
                    #car
                    cv2.rectangle(show , (int(center[0] -4+(tx-x)*2), int(center[1] -4+(ty-y)*2)),
                                         (int(center[0] +4+(tx-x)*2), int(center[1] +4+(ty-y)*2)), 
                                         (0, 255, 255), thickness=-1)
        except:
            pass
    
    # Display the resulting frame
    cv2.imshow('Frame',show )
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
 









