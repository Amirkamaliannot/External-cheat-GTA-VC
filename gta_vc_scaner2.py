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
import struct


pm = pymem.Pymem("gta-vc.exe")

game_module = module_from_name(pm.process_handle, "gta-vc.exe").lpBaseOfDll

img_size = (1024, 1024)
white_img = np.ones((img_size[0], img_size[1], 3), dtype=np.uint8) * 255
center = (img_size[0]//2, img_size[1]//2)


def is_structure(pointer):
    
    try:
        # print(pointer)
        tx = pm.read_float(pointer + 0x34 )
        ty = pm.read_float(pointer + 0x38 )
        tz = pm.read_float(pointer + 0x3c )
        
        # print(tx, ty, tz)
        if( (-2000 < tx <-0.01 or  0.01 < tx < 2000) and (-2000 < ty <-0.01 or  0.01 < ty < 2000) and ( 5 < tz < 100 ) ):
            return True
        else: return False
    except: return False


def show_point_in_map(x, y, size=2, color=(64, 36, 209)):
    global point_list
    if(img_size[0] > abs(x) and img_size[1] > abs(y)):    
        # cv2.rectangle(show , (int(x -size), int(y-size)),(int(x +size), int(y+size)), color, thickness=-1)
        
        point_list.append([x,y])
    else: return False



# def show_structure_points(pointer, x, y):
    
    
#     if(hex(pointer) in address_list): return
#     address_list.append(hex(pointer))

#     try:
#         pointer_value = pm.read_bytes(pointer, 4)
#         pointer_value = int.from_bytes(pointer_value, "little")
#     except:return 0;
    
#     # print(hex(pointer_value))

#     # if(pointer_value and pointer_value < 194670032):
#     #     if(is_structure(pointer_value)):
            
#     #         # print('ok')
#     #         for i in range(50):
#     #             tx = pm.read_float(pointer_value + 0x34+  64* i )
#     #             ty = pm.read_float(pointer_value + 0x38+  64* i  )
#     #             # tz = pm.read_float(pointer_value + 0x3c )
#     #             # print(x, y)
#     #             show_point_in_map(center[0]+(tx-x), center[1]+(ty-y))
            
#     #     else:
#     #         for i in range(0,4):
#     #             show_structure_points(pointer_value + 4*i , x, y)
#     # # except: return
    
#     try:
#         if(pointer_value and pointer_value < 194670032):
#             if(is_structure(pointer_value)):
#                 for i in range(50):
#                     tx = pm.read_float(pointer_value + 0x34+  64* i )
#                     ty = pm.read_float(pointer_value + 0x38+  64* i  )
#                     show_point_in_map(center[0]+(tx-x), center[1]+(ty-y))
                
#             else:
#                 for i in range(0,5):
#                     show_structure_points(pointer_value + 4*i , x, y)
#     except Exception as e:
#         print('Error:', e)

def show_structure_points(pointer, x, y):
    stack = [pointer]
    
    print(hex(pointer))
    while stack:
        current_pointer = stack.pop()
        
        if current_pointer in address_list:
            continue
        address_list.append(current_pointer)
        try:
            pointer_value = pm.read_bytes(current_pointer, 4)
            pointer_value = int.from_bytes(pointer_value, "little")
            if pointer_value in address_list:
                continue
            
        except:
            continue
        if pointer_value and pointer_value < 194670032:
            if is_structure(pointer_value):
                for i in range(50):
                    tx = pm.read_float(pointer_value + 0x34 + 64 * i)
                    ty = pm.read_float(pointer_value + 0x38 + 64 * i)
                    show_point_in_map(center[0] + (tx - x), center[1] + (ty - y))
            else:
                for i in range(4):
                    stack.append(pointer_value + 4 * i)

# for i in range(1):
    
point_list=[]
while(1):
    point_list=[]
    address_list = []
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
                                                       
    for i in range(10):
        show_structure_points(0x8E8DF88  + i*4, x, y)
        # print(point_list)
        
        for i in point_list:
            cv2.rectangle(show, (int(i[0])-2, int(i[1])-2), (int(i[0])+2, int(i[1])+2), (255, 255, 0), thickness=-1)

            
            
            
            
            
            # xbyte_int = int.from_bytes(pm.read_bytes(a_int + 0x50, 1) , "little")
            
    
                
            
                # print(pm.read_float(a_int + 0x34 ))
                
                # byte_value = pm.read_bytes(a_int + 0x50, 1)[0]
                # type_object = byte_value & 0b111
                # status = byte_value >> 3
                # print(type_object)
            
            # if not ( -2000 < pm.read_float(a_int + 0x34 ) <2000):
            #     print ('ok')
            
    # Display the resulting frame
    cv2.imshow('Frame',show )
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    
    









