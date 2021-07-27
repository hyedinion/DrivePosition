#!/usr/bin/env python
# coding: utf-8

# In[1]:


#dictionary
class CarModel:    
    def __init__(self,a_d,b_d,c,d_left,d_right,e,f,g,name):
        self.a_d = a_d #페달 ~ 시트를 맨앞으로 당겼을때의 거리
        self.b_d = b_d #차량내부 바닥 ~ 시트를 맨아래로 내렸을때의 거리
        self.c = c #사이드미러 중앙 ~ 시트를 맨앞으로 당겼을때 눈위치(사람머리두께를 약 17 ~ 18cm 라고 가정, 차량 옆면과 수평이 되는 거리측정.)
        self.d_left = d_left #좌측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
        self.d_right = d_right #우측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
        self.e = e #차량내부 바닥 ~ 대시보드
        self.f = f #차량내부 바닥 ~ 사이드미러 중앙까지의 높이
        self.g = g #대시 ~ 천장
        self.name = name
        
class Drivepos:
    def __init__(self, a_u, b_u, lr_angle_left, lr_angle_right, ud_angle, model:CarModel):
        self.a_u = a_u                          #사용자가 이동시킨 x값
        self.b_u = b_u                          #사용자가 이동시킨 y값
        self.lr_angle_left = lr_angle_left      #사용자가 설정시킨 좌우 사이드미러 angle (차량 옆면 기준)
        self.lr_angle_right = lr_angle_right    #사용자가 설정시킨 좌우 사이드미러 angle (차량 옆면 기준)
        self.ud_angle = ud_angle                #사용자가 설정시킨 상하 사이드미러 angle (미러의 기울기)
        self.model:CarModel = model             #CarModel 객체
    
    def __iter__(self):
        for key in self.__dict__:
             yield (key, self.__dict__[key]) if key != 'model' else (key, self.__dict__[key].__dict__)
                
class PersonalConst:
    def __init__(self, hip_to_eye, default_side):
        self.hip_to_eye = hip_to_eye        #엉덩이 ~ 눈
        self.default_side = default_side    #사용자 설정 사이드미러 각 활용 여부

    
#자동차 상수값
Morning = CarModel(34, 30, 63.5, 50.5, 103.5, 77, 77, 35, "Morning") # 가상의 값 (6, 7 ,8)
Avante = CarModel(34, 30, 74, 55, 125, 77, 77, 38,"Avante") # 가상의 값 (2, 8)
Genesis_G70 = CarModel(34, 29, 51, 57, 134, 77, 80, 40, "Genesis_G70") # 현재 제네시스만 정확.


##move_change test
current_Model = Morning #현재 타고있는 차량
User = PersonalConst(100,1) #현재 user의 정보
setting_Model= Drivepos(4, 5, 50, 48, 35, Morning) #현재 user의 driveposition setting값
#차마다 driveposition저장
car_Model_setting = {"Morning":Drivepos(0, 0, 0, 0, 0, current_Model),"Avante":Drivepos(0, 0, 0, 0, 0, current_Model),"Genesis_G70":Drivepos(0, 0, 0, 0, 0, current_Model)}
current_Model_setting = car_Model_setting[current_Model.name]# 현재 타고있는 차량의 driveposition
ver = 2
car_setting_complete = 0

print(current_Model_setting.model)


# In[2]:


import math
def transformModel(setting:Drivepos, target:CarModel, personal:PersonalConst, ver) -> Drivepos:
    #####좌석시트
    A = setting.a_u + setting.model.a_d     #사용자가 편안하다고 느끼는 공간
    delta_a = A - target.a_d                #바뀐차량에서 사용자가 움직여야하는 x값

    #ver 1 : 바닥에서 편안한 공간을 확보한 값을 이용하여 시트조정
    B = setting.b_u + setting.model.b_d
    delta_b = B - target.b_d
    #ver 2 : 대시보드에서 시선이 올라오는 고정값으로 시트조정
    if ver == 2:
        B = - setting.b_u - setting.model.b_d + setting.model.e
        delta_b = - B - target.b_d + target.e
    #ver 3: 대시보드에 사용자 시선이 위치하는 지점의 비율을 고려하여 시트조정.
    elif ver == 3 :
        B = ( personal.hip_to_eye + setting.b_u + setting.model.b_d - setting.model.e ) / setting.model.g
        delta_b = B * target.g - personal.hip_to_eye - target.b_d + target.e

    #####사이드미러
    setting_C = setting.a_u + setting.model.c   # 사이드미러 중앙 ~ 시트설정후 사용자의 눈위치 (차량 옆면과 수평이 되는 거리)
    target_C = delta_a + target.c
    setting_D_left = setting.model.d_left       # 좌측 사이드미러 중앙 ~ 차량시트 중앙까지의 거리
    target_D_left = target.d_left
    setting_D_right = setting.model.d_right     # 우측 사이드미러 중앙 ~ 차량시트 중앙까지의 거리
    target_D_right = target.d_right
    setting_E = setting.b_u + setting.model.b_d + personal.hip_to_eye - setting.model.f  # 사이드미러 중앙 ~ 사용자의 눈높이 // (바닥 ~ 조정된시트의 높이) + (사람의 엉덩이 ~ 눈위치) - (바닥 ~ 미러)
    target_E = delta_b + target.b_d + personal.hip_to_eye - target.f
    
    #사이드미러 각 표준값으로 세팅 (시야가 차체 방향과 나란하게 나감.)
    p_left = 90     # 좌측사이드 좌우 시야각의 각도 (사이드미러에서 바라봤을때의 좌우시야 각) // 사용자 취향반영 (바깥쪽(>90), 중간(90), 안쪽(<90)..)
    p_right = 90    # 우측사이드 좌우 시야각의 각도 (사이드미러에서 바라봤을때의 좌우시야 각) // 사용자 취향반영 (바깥쪽(>90), 중간(90), 안쪽(<90)..)
    q = 90          # 양측사이드 상하 시야각의 각도 (사이드미러에서 바라봤을때의 상하시야 각) // 사용자 취향반영 (위(>90), 중간(90), 아래(<90)..)
    
    #사이드미러 각 사용자 취향고려
    if not personal.default_side:
        p_left = 2*setting.lr_angle_left - math.degrees(math.atan2(setting_C, setting_D_left))
        p_right = 2*setting.lr_angle_right - math.degrees(math.atan2(setting_C, setting_D_right))
        q = 2*setting.ud_angle + math.degrees(math.atan2(setting_C, setting_E))
    
    delta_lr_angle_left = (p_left + math.degrees(math.atan2(target_C, target_D_left)))/2    #사용자가 움직여야하는 사이드미러 좌우각도
    delta_lr_angle_right = (p_right + math.degrees(math.atan2(target_C, target_D_right)))/2 #사용자가 움직여야하는 사이드미러 좌우각도
    delta_ud_angle = (q - math.degrees(math.atan2(target_C, target_E)))/2                   #사용자가 움직여야하는 사이드미러 상하각도
    
    return Drivepos(delta_a, delta_b, delta_lr_angle_left, delta_lr_angle_right, delta_ud_angle, target)


def getToMove(setting:Drivepos, current:Drivepos) -> Drivepos:
    return Drivepos(setting.a_u - current.a_u, setting.b_u - current.b_u, setting.lr_angle_left - current.lr_angle_left, setting.lr_angle_right - current.lr_angle_left , setting.ud_angle - current.ud_angle, setting.model)

def move_change(setting_Model:Drivepos,current_Model_setting:Drivepos,User:PersonalConst,ver):
    #차종별 상수 세팅
    global Morning
    global Avante
    global Genesis_G70

    get_transformed_setting = transformModel(setting_Model, current_Model_setting.model, User, ver)

    #얼마나 움직여야 하는지 출력
    toMove = getToMove(get_transformed_setting, current_Model_setting)
    
    return toMove


# In[3]:


import socketio
import eventlet
import json as js
import threading
#create a Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)
        

@sio.event
def connect(sid, environ):
	print('connect ', sid)

@sio.event
def disconnect(sid):
	print('disconnect ', sid)


#안드로이드 connect요청
@sio.on('connect_first')
def test(sid,json):
    global car_setting_complete
    global current_Model
    if car_setting_complete==1:
        json_data = js.dumps(current_Model.__dict__)
        sio.emit('connect_response',json_data)
    
    

#안드로이드 personalConst
@sio.on('personal_request')
def test(sid,json):
    global User
    #String 받아옴 "height default_side"
    print(json)
    person = json.split()
    height =float(person[0])
    default_side = int(person[1])
    hip_to_eye = height * 0.438 + 5.0973 # 키와 엉덩이에서 눈높이까지의 길이에 대한 연관관계
    
    User = PersonalConst(hip_to_eye,default_side)
    
import copy
#안드로이드 save요청
@sio.on('save_request')
def test(sid,json):
    global current_Model_setting
    print(json)
    car = current_Model_setting.model.__dict__
    cm = copy.deepcopy(current_Model_setting)
    cm.model = car
    json_data = js.dumps(cm.__dict__)
    print(json_data)
    sio.emit('save_send',json_data)

#안드로이드 apply요청
@sio.on('apply')
def test(sid,json):
    global current_Model_setting
    #string 받아옴
    user_setting = eval(json)
    #CarModel 객체로 변환
    car = user_setting['model']
    carList = list(car.values())
    carmodel = CarModel(carList[0],carList[1],carList[2],carList[3],carList[4],carList[5],carList[6],carList[7],carList[8])
    #Drivepos 객체로 변환
    settingList = list(user_setting.values())
    current_Model_setting = Drivepos(settingList[0],settingList[1],settingList[2],settingList[3],settingList[4],carmodel)
    #여기서 vpython에 움직이기 요청
    print(json)
    
    
def start_server():
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0',5000)),app)
    
server_thread = threading.Thread(target=start_server)
server_thread.start()


# In[4]:


def carmodel_setting():
    global Morning
    global Avante
    global Genesis_G70
    global current_Model
    global car_setting_complete
    global current_Model_setting
    
    carnum = int(input("차량 종류를 입력하세요 (1: Morning, 2: avante, 3: genesis)"))
    if carnum==1:
        current_Model = Morning
    elif carnum==2:
        current_Model = Avante
    else:
        current_Model = Genesis_G70
    
    current_Model_setting = car_Model_setting[current_Model.name]
        
        
    car_setting_complete = 1
    
    print(current_Model.name)
    

class chachacha:
    def __init__(self, niked, pos_x, pos_y, pos_z, driver_height):
        thickness = 10 
        side_mirror_2_door = 10
        car_bottom_thickness = 10
        car_ceil_thickness = 10
        shortest_seat_2_padal = niked.model.a_d
        lowest_seat_2_car_bottom = niked.model.b_d
        right_side_mirror_2_center_of_seat = niked.model.d_right
        left_side_mirro_2_center_of_seat = niked.model.d_left
        dash_2_car_bottom = niked.model.e
        inner_car_height = ( niked.model.e + niked.model.g )
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
        car_bottom_pos_x = pos_x
        car_bottom_pos_y = pos_y
        car_bottom_pos_z = pos_z 
        
        car_seat_pos_x = car_bottom_pos_x + ( (car_length / 2) - padal_length - shortest_seat_2_padal - (car_seat_size / 2) ) + niked.a_u
     
        car_seat_pos_y = car_bottom_pos_y + lowest_seat_2_car_bottom + (car_bottom_thickness / 2) - (car_seat_height / 2) + niked.b_u
    
        car_seat_pos_z = car_bottom_pos_z -  ( car_width / 4 )
    
        car_seat_back_pos_x = car_seat_pos_x - (car_seat_size / 2) + (car_seat_back_thickness / 2)
    
        car_seat_back_pos_y = car_seat_pos_y + (car_seat_height / 2) + (car_seat_back_size / 2)
    
        car_seat_back_pos_z = car_seat_pos_z 
    
        car_ceil_pos_x = car_bottom_pos_x
    
        car_ceil_pos_y = car_bottom_pos_y +  inner_car_height + (car_bottom_thickness / 2) + (car_ceil_thickness / 2) 
    
        car_ceil_pos_z = car_bottom_pos_z
         
        eye_position_x = car_bottom_pos_x + (car_length/2) - padal_length - niked.model.c
    
        eye_position_y = car_seat_pos_y + (driver_height * 0.44)
    
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
    
        left_side_mirror_position_y = car_bottom_pos_y + (car_bottom_thickness / 2) + (side_mirror_height / 2) + niked.model.f
    
        left_side_mirror_position_z = dash_position_z - ( (car_width / 4) + door_thickness + side_mirror_2_door + ( side_mirror_thickness / 2 ) )
    
        right_side_mirror_position_x = dash_position_x
    
        right_side_mirror_position_y = car_bottom_pos_y + (car_bottom_thickness / 2) + (side_mirror_height / 2) + niked.model.f
    
        right_side_mirror_position_z = dash_position_z + ( 3*(car_width / 4) + door_thickness + side_mirror_2_door + ( side_mirror_thickness / 2 ) )
        
        self.car_bottom = box(pos = vec(car_bottom_pos_x, car_bottom_pos_y, car_bottom_pos_z), length = car_length, height=car_bottom_thickness, width = car_width )
    
        self.car_ceil = box(pos = vec(car_ceil_pos_x, car_ceil_pos_y, car_ceil_pos_z), length = car_length, height = car_ceil_thickness, width = car_width, opacity = 0.5 )
    
        self.car_seat = box(pos = vec(car_seat_pos_x, car_seat_pos_y, car_seat_pos_z), length = car_seat_size, height = car_seat_height , width = car_seat_size )
    
        self.car_seat_back = box(pos = vec(car_seat_back_pos_x, car_seat_back_pos_y, car_seat_back_pos_z), length = car_seat_back_thickness , height=car_seat_back_size , width= car_seat_back_size)
    
        self.eye = box(pos = vec(eye_position_x, eye_position_y, eye_position_z), length = 5, height = 5, width = 5, color = color.red)
    
        self.padal = box(pos= vec(padal_postion_x, padal_postion_y, padal_postion_z), length = padal_length, height = padal_height, width = padal_width )
    
        self.dash = box(pos= vec(dash_position_x, dash_position_y, dash_position_z), length = dash_length, height = dash_height, width = dash_width  )
    
        self.left_door = box(pos = vec(left_door_position_x, left_door_position_y, left_door_position_z), length = car_length, height = inner_car_height ,width = door_thickness, opacity = 0.5)
    
        self.right_door = box(pos = vec(right_door_position_x, right_door_position_y, right_door_position_z), length = car_length, height = inner_car_height ,width = door_thickness, opacity = 0.5)
    
        self.left_side_mirror = box(pos = vec(left_side_mirror_position_x, left_side_mirror_position_y, left_side_mirror_position_z), length = side_mirror_length, height = side_mirror_height  , width =side_mirror_thickness)
    
        self.right_side_mirror = box(pos = vec(right_side_mirror_position_x, right_side_mirror_position_y, right_side_mirror_position_z), length = side_mirror_length, height = side_mirror_height  , width =side_mirror_thickness)
        
        self.left_side_mirror.rotate(angle = niked.lr_angle_left , axis = vec(0,1,0))
        self.left_side_mirror.rotate(angle = niked.ud_angle , axis = vec(1,0,0))
        
        self.right_side_mirror.rotate(angle = niked.lr_angle_right, axis = vec(0,1,0))
        self.right_side_mirror.rotate(angle = niked.ud_angle, axis = vec(1,0,0))
            
        
        
        
def MovSimul (nike, acg):
    delta = 0.1
    delta_sum = 0
    
    while (delta_sum < acg.a_u):
        rate(30)
        nike.car_seat.pos.x -= delta
        nike.car_seat_back.pos.x -= delta
        nike.eye.pos.x -= delta
        delta_sum += delta
    
    delta_sum = 0
    
    while (delta_sum < acg.b_u):
        rate(30)
        nike.car_seat.pos.y += delta
        nike.car_seat_back.pos.y += delta
        nike.eye.pos.y += delta
        delta_sum += delta
        
    delta_sum = 0
    delta = 1
    
    while (delta_sum < acg.lr_angle_left ):
        rate(30)
        nike.left_side_mirror.rotate(angle =radians(-delta), axis = vec(0,1,0))
        delta_sum += delta
    
    delta_sum = 0
    
    while (delta_sum < -(acg.ud_angle) ):
        rate(30)
        nike.left_side_mirror.rotate(angle = radians(delta), axis = vec(1,0,0) )
        delta_sum += delta
    
    delta_sum = 0
    
    while (delta_sum < acg.lr_angle_right) :
        rate(30)
        nike.right_side_mirror.rotate(angle = radians(delta), axis = vec(0,1,0) )
        delta_sum += delta
    
    delta_sum = 0
    
    while (delta_sum < -(acg.ud_angle) ):
        rate(30)
        nike.right_side_mirror.rotate(angle = radians(delta), axis = vec(1,0,0) )
        delta_sum += delta
        
    
    

def MakeCar( current , pos_x, pos_y, pos_z, driver_height):
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
    
    car_bottom_pos_x = pos_x

    car_bottom_pos_y = pos_y

    car_bottom_pos_z = pos_z
    
 
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

    eye_position_y = car_seat_pos_y + (driver_height * 0.44)

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
    
    


def Simulation(current, change, driver_height, current2):
        
    car1 = chachacha(current,0,0,0, driver_height)    
    
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
    
    returning = current
    
    while True:
        rate(30)
        k = keysdown() # a list of keys that are down
        if 'left'  in k:
            car1.car_seat.pos.x -= dv
            car1.car_seat_back.pos.x -=dv
            car1.eye.pos.x -= dv
            back_and_forth_sum += dv
            returning.a_u = back_and_forth_sum

            
        if 'right' in k: 
            car1.car_seat.pos.x += dv
            car1.car_seat_back.pos.x +=dv
            car1.eye.pos.x += dv
            back_and_forth_sum  -= dv
            returning.a_u = back_and_forth_sum
            
            
            
        if 'down' in k: 
            car1.car_seat.pos.y -= dv
            car1.car_seat_back.pos.y -=dv
            car1.eye.pos.y -= dv
            up_and_down_sum -= dv
            returning.b_u = up_and_down_sum
            
            
        if 'up' in k: 
            car1.car_seat.pos.y += dv
            car1.car_seat_back.pos.y +=dv
            car1.eye.pos.y += dv
            up_and_down_sum += dv
            returning.b_u = up_and_down_sum
            
        
        if 'a' in k : 
            car1.left_side_mirror.rotate(angle =  -dv2, axis = vec(0,1,0))
            theta1_sum += degrees(dv2)
            returning.lr_angle_left = theta1_sum

        if 'd' in k :
            car1.left_side_mirror.rotate(angle = dv2, axis = vec(0,1,0))
            theta1_sum -= degrees(dv2)
            returning.lr_angle_left = theta1_sum
           
        if 's' in k :
            car1.left_side_mirror.rotate(angle =  dv2, axis = vec(1,0,0))
            theta3_sum -= degrees(dv2)
            returning.ud_angle = theta3_sum
            
        if 'w' in k :
            car1.left_side_mirror.rotate(angle =  -dv2, axis = vec(1,0,0))
            theta3_sum += degrees(dv2)
            returning.ud_angle = theta3_sum
        
        
        if 'j' in k : 
            car1.right_side_mirror.rotate(angle = -dv2, axis = vec(0,1,0))
            theta2_sum -= degrees(dv2)
            returning.lr_angle_right = theta2_sum
          
        if 'l' in k :
            car1.right_side_mirror.rotate(angle = dv2, axis = vec(0,1,0))
            theta2_sum += degrees(dv2)
            returning.lr_angle_right = theta2_sum
          
        if 'k' in k : 
            car1.right_side_mirror.rotate(angle = -dv2, axis = vec(1,0,0))
            theta4_sum -= dv2
        
        if 'i' in k :
            car1.right_side_mirror.rotate(angle = dv2, axis = vec(1,0,0))
            theta4_sum += dv2

        if 'q' in k:
            car2 = chachacha(current2, 400,0,0, driver_height)     
            scene.camera.pos= vec(400, 0, 400 )# (car2.car_car_bottom)
            print(scene.camera.pos)
            MovSimul (car2, change)
            print("end")
            
        if 'y' in k:
            carmodel_setting()
            
        
            
            


# In[ ]:


from vpython import *

to_car = Avante
current2 = car_Model_setting[to_car.name]
change = move_change(setting_Model,current_Model_setting,User,ver)#->Drivepos
carmodel_setting()
Simulation(current_Model_setting, change, User.hip_to_eye,current2)


# In[ ]:




