#GlowScript 3.1 VPython
from vpython import *
from ..transform_model.transform_base import *

def Simulation(current:Drivepos, change, driver_height):
    thickness = 10 
    side_mirror_2_door = 10
    car_bottom_thickness = 10
    car_ceil_thickness = 10
    shortest_seat_2_padal = current.model.a_d
    lowest_seat_2_car_bottom = current.model.b_d
    right_side_mirror_2_center_of_seat = current.model.d_right
    left_side_mirro_2_center_of_seat = current.model.d_left
    dash_2_car_bottom = current.model.e
    inner_car_height = ( current.model.e + current.model.g )
    
    car_width =  right_side_mirror_2_center_of_seat + left_side_mirro_2_center_of_seat - (2 * side_mirror_2_door)
    car_length = 2 * car_width
    car_seat_size = (car_width / 2)/2
    car_seat_height = thickness
    car_seat_back_thickness = thickness
    car_seat_back_size = car_seat_size
    padal_length = 20
    padal_height = thickness
    padal_width = (car_width / 2)
    dash_length = 2 * padal_length 
    dash_width = (car_width / 2)
    dash_height = thickness
    door_thickness = thickness

    side_mirror_length = 20
    side_mirror_height = 10
    side_mirror_thickness = thickness
    car_bottom_pos_x = 0
    car_bottom_pos_y = 0
    car_bottom_pos_z = 0
    
    car_seat_pos_x = car_bottom_pos_x + ( (car_length / 2) - padal_length - shortest_seat_2_padal - (car_seat_size / 2) ) + current.a_u
    car_seat_pos_y = car_bottom_pos_y + lowest_seat_2_car_bottom + (car_bottom_thickness / 2) - (car_seat_height / 2) + current.b_u
    car_seat_pos_z = car_bottom_pos_z -  ( car_width / 4 )
    car_seat_back_pos_x = car_seat_pos_x - (car_seat_size / 2) + (car_seat_back_thickness / 2)
    car_seat_back_pos_y = car_seat_pos_y + (car_seat_height / 2) + (car_seat_back_size / 2)
    car_seat_back_pos_z = car_seat_pos_z 
    car_ceil_pos_x = car_bottom_pos_x
    car_ceil_pos_y = car_bottom_pos_y +  inner_car_height + (car_bottom_thickness / 2) + (car_ceil_thickness / 2) 
    car_ceil_pos_z = car_bottom_pos_z
    eye_position_x = car_bottom_pos_x + (car_length/2) - padal_length - current.model.c
    eye_position_y = car_seat_pos_y + driver_height
    eye_position_z = car_seat_pos_z 
    padal_postion_x = car_bottom_pos_x + ( (car_length / 2) - (padal_length / 2) )
    padal_postion_y = car_bottom_pos_y +  (padal_height / 2) + (car_bottom_thickness / 2)
    padal_postion_z = car_bottom_pos_z -  ( car_width / 4 )
    dash_position_x = car_bottom_pos_x + ( (car_length / 2) - (dash_length / 2) )
    dash_position_y = car_bottom_pos_y + (car_bottom_thickness / 2) + dash_2_car_bottom + (dash_height / 2)
    dash_position_z = car_bottom_pos_z -  ( car_width / 4 )
    left_door_position_x = car_bottom_pos_x
    left_door_position_y = car_bottom_pos_y + (inner_car_height / 2)
    left_door_position_z = car_bottom_pos_z - ( ( car_width / 2 ) + ( door_thickness / 2 ) )
    right_door_position_x = car_bottom_pos_x
    right_door_position_y = car_bottom_pos_y + (inner_car_height / 2)
    right_door_position_z = car_bottom_pos_z + ( ( car_width / 2 ) + ( door_thickness / 2 ) )
    left_side_mirror_position_x = dash_position_x 
    left_side_mirror_position_y = car_bottom_pos_y + (car_bottom_thickness / 2) + (side_mirror_height / 2) + current.model.f
    left_side_mirror_position_z = dash_position_z - ( (car_width / 4) + door_thickness + side_mirror_2_door + ( side_mirror_thickness / 2 ) )
    right_side_mirror_position_x = dash_position_x
    right_side_mirror_position_y = car_bottom_pos_y + (car_bottom_thickness / 2) + (side_mirror_height / 2) + current.model.f
    right_side_mirror_position_z = dash_position_z + ( 3*(car_width / 4) + door_thickness + side_mirror_2_door + ( side_mirror_thickness / 2 ) )
    
    car_bottom = box(pos = vec(car_bottom_pos_x, car_bottom_pos_y, car_bottom_pos_z), length = car_length, height=car_bottom_thickness, width = car_width )
    car_ceil = box(pos = vec(car_ceil_pos_x, car_ceil_pos_y, car_ceil_pos_z), length = car_length, height = car_ceil_thickness, width = car_width, opacity = 0.5 )
    car_seat = box(pos = vec(car_seat_pos_x, car_seat_pos_y, car_seat_pos_z), length = car_seat_size, height = car_seat_height , width = car_seat_size )
    car_seat_back = box(pos = vec(car_seat_back_pos_x, car_seat_back_pos_y, car_seat_back_pos_z), length = car_seat_back_thickness , height=car_seat_back_size , width= car_seat_back_size)
    eye = box(pos = vec(eye_position_x, eye_position_y, eye_position_z), length = 5, height = 5, width = 5, color = color.red)
    padal = box(pos= vec(padal_postion_x, padal_postion_y, padal_postion_z), length = padal_length, height = padal_height, width = padal_width )
    dash = box(pos= vec(dash_position_x, dash_position_y, dash_position_z), length = dash_length, height = dash_height, width = dash_width  )
    left_door = box(pos = vec(left_door_position_x, left_door_position_y, left_door_position_z), length = car_length, height = inner_car_height ,width = door_thickness, opacity = 0.5)
    right_door = box(pos = vec(right_door_position_x, right_door_position_y, right_door_position_z), length = car_length, height = inner_car_height ,width = door_thickness, opacity = 0.5)
    left_side_mirror = box(pos = vec(left_side_mirror_position_x, left_side_mirror_position_y, left_side_mirror_position_z), length = side_mirror_length, height = side_mirror_height  , width =side_mirror_thickness)
    right_side_mirror = box(pos = vec(right_side_mirror_position_x, right_side_mirror_position_y, right_side_mirror_position_z), length = side_mirror_length, height = side_mirror_height  , width =side_mirror_thickness)
    left_side_mirror.rotate(angle = current.lr_angle_left , axis = vec(0,1,0))
    left_side_mirror.rotate(angle = current.ud_angle , axis = vec(1,0,0))
    right_side_mirror.rotate(angle = current.lr_angle_right, axis = vec(0,1,0))
    right_side_mirror.rotate(angle = current.ud_angle, axis = vec(1,0,0))
    
    v = vec(0,0,0)
    dv = 0.5 # 0.2
    dv2 = 0.05
    dt = 1 # 0.1
    back_and_forth_sum = current.a_u
    up_and_down_sum = current.b_u
    theta1_sum = current.lr_angle_left
    theta2_sum = current.lr_angle_right
    theta3_sum = current.ud_angle
    theta4_sum = current.ud_angle

    ########################    Control Block   ########################
    # while True:
    #     rate(30)
    #     k = keysdown() # a list of keys that are down
    #     #시트
    #     if 'left'  in k:
    #         car_seat.pos.x -= dv
    #         car_seat_back.pos.x -=dv
    #         eye.pos.x -= dv
    #         back_and_forth_sum += dv
    #         print(back_and_forth_sum)
    #     if 'right' in k: 
    #         car_seat.pos.x += dv
    #         car_seat_back.pos.x +=dv
    #         eye.pos.x += dv
    #         back_and_forth_sum  -= dv
    #         print(back_and_forth_sum)
    #     if 'down' in k: 
    #         car_seat.pos.y -= dv
    #         car_seat_back.pos.y -=dv
    #         eye.pos.y -= dv
    #         up_and_down_sum -= dv
    #         print(up_and_down_sum)
    #     if 'up' in k: 
    #         car_seat.pos.y += dv
    #         car_seat_back.pos.y +=dv
    #         eye.pos.y += dv
    #         up_and_down_sum += dv
    #         print(up_and_down_sum)
    #     #사이드미러(좌측)
    #     if 'a' in k : 
    #         left_side_mirror.rotate(angle =  -dv2, axis = vec(0,1,0))
    #         theta1_sum -= dv2
    #         print(theta1_sum)
    #     if 'd' in k :
    #         left_side_mirror.rotate(angle = dv2, axis = vec(0,1,0))
    #         theta1_sum += dv2
    #         print(theta1_sum)
    #     if 's' in k :
    #         left_side_mirror.rotate(angle =  dv2, axis = vec(1,0,0))
    #         theta3_sum += dv2
    #         print(theta3_sum)
    #     if 'w' in k :
    #         left_side_mirror.rotate(angle =  -dv2, axis = vec(1,0,0))
    #         theta3_sum -= dv2
    #         print(theta3_sum)
    #     #사이드미러(우측)
    #     if 'j' in k : 
    #         right_side_mirror.rotate(angle = -dv2, axis = vec(0,1,0))
    #         theta2_sum -= dv2
    #         print(theta2_sum)
    #     if 'l' in k :
    #         right_side_mirror.rotate(angle = dv2, axis = vec(0,1,0))
    #         theta2_sum += dv2
    #         print(theta2_sum)
    #     if 'k' in k : 
    #         right_side_mirror.rotate(angle = -dv2, axis = vec(1,0,0))
    #         theta4_sum -= dv2
    #         print(theta4_sum)
    #     if 'i' in k :
    #         right_side_mirror.rotate(angle = dv2, axis = vec(1,0,0))
    #         theta4_sum += dv2
    #         print(theta4_sum)

Avante = CarModel(34, 30, 74, 55, 125, 77, 77, 38,"Avante")
current_Model_setting = Drivepos(1, 2, 0, 0, 0, Avante)
hip_to_eye = 170*0.44
Simulation(current_Model_setting, 0, hip_to_eye)