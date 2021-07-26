GlowScript 3.1 VPython

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
    def __init__(self,a_u,b_u,lr_angle_left,lr_angle_right,ud_angle,model):
        self.a_u = a_u #사용자가 이동시킨 x값
        self.b_u = b_u #사용자가 이동시킨 y값
        self.lr_angle_left = lr_angle_left #사용자가 설정시킨 좌우 사이드미러 angle (차량 옆면 기준)
        self.lr_angle_right = lr_angle_right #사용자가 설정시킨 좌우 사이드미러 angle (차량 옆면 기준)
        self.ud_angle = ud_angle #사용자가 설정시킨 상하 사이드미러 angle (미러의 기울기)
        self.model = model #carmodel class 객체

def transformModel(setting,target,hip_to_eye,default_setting,ver):
    
    #사용자의 성향 반영한 변수
    
    #좌석시트
    A = 0.0
    delta_a = 0.0
    A = setting.a_u + setting.model.a_d #사용자가 편안하다고 느끼는 공간
    delta_a = A - target.a_d #바뀐차량에서 사용자가 움직여야하는 x값
    
    B = 0.0 # 시트의 높이를 결정할때 사용자의 취향이 반영된 변수
    delta_b=0.0 # 바뀐차량에서 사용자가 움직여야하는 y값
   
    if ver == 1 :
        #ver 1 : 바닥에서 편안한 공간을 확보한 값을 이용하여 시트조정
        B = setting.b_u + setting.model.b_d
        delta_b = B - target.b_d
        
    elif ver == 2:
        #ver 2 : 대시보드에서 시선이 올라오는 고정값으로 시트조정 
        B = - setting.b_u - setting.model.b_d + setting.model.e #조정된 시트에서 대쉬보드까지의 높이
        delta_b = - B - target.b_d + target.e

    elif ver == 3 :
        #ver 3: 대시보드에 사용자 시선이 위치하는 지점의 비율을 고려하여 시트조정.
        B = ( hip_to_eye + setting.b_u + setting.model.b_d - setting.model.e ) / setting.model.g  #사용자가 시트를 조정 했을때 대시보드에 사용자 시선이 위치하는 지점의 비율
        delta_b = B * target.g - hip_to_eye - target.b_d + target.e

    #/* 사이드미러 */
    setting_C = setting.a_u + setting.model.c # 사이드미러 중앙 ~ 시트설정후 사용자의 눈위치 (차량 옆면과 수평이 되는 거리)
    target_C = delta_a + target.c
    
    setting_D_left = setting.model.d_left  # 좌측 사이드미러 중앙 ~ 차량시트 중앙까지의 거리
    target_D_left = target.d_left
    setting_D_right = setting.model.d_right  # 우측 사이드미러 중앙 ~ 차량시트 중앙까지의 거리
    target_D_right = target.d_right
    
    setting_E = setting.b_u + setting.model.b_d + hip_to_eye - setting.model.f  # 사이드미러 중앙 ~ 사용자의 눈높이 // (바닥 ~ 조정된시트의 높이) + (사람의 엉덩이 ~ 눈위치) - (바닥 ~ 미러)
    target_E = delta_b + target.b_d + hip_to_eye - target.f
    
    p_left = 0.0 # 좌측사이드 좌우 시야각의 각도 (사이드미러에서 바라봤을때의 좌우시야 각) // 사용자 취향반영 (바깥쪽(>90), 중간(90), 안쪽(<90)..)
    p_right = 0.0 # 우측사이드 좌우 시야각의 각도 (사이드미러에서 바라봤을때의 좌우시야 각) // 사용자 취향반영 (바깥쪽(>90), 중간(90), 안쪽(<90)..)
    q=0.0 # 상하 시야각의 각도 (사이드미러에서 바라봤을때의 상하시야 각) // 사용자 취향반영 (위(>90), 중간(90), 아래(<90)..)
    
    if default_setting == 1:
        # 표준값으로 세팅 (시야가 차체 방향과 나란하게 나감.)
        p_left = 90
        p_right = 90
        q = 90
    elif default_setting == 0:
        #사용자 취향고려
        p_left = 2*setting.lr_angle_left - degrees(atan2(setting_C, setting_D_left))
        p_right = 2*setting.lr_angle_right - degrees(atan2(setting_C, setting_D_right))
        q = 2*setting.ud_angle + degrees(atan2(setting_C, setting_E))
    
    delta_lr_angle_left = (p_left + degrees(atan2(target_C, target_D_left)))/2 # 바뀐차량에서 사용자가 움직여야하는 사이드미러 좌우각도
    delta_lr_angle_right = (p_right + degrees(atan2(target_C, target_D_right)))/2 # 바뀐차량에서 사용자가 움직여야하는 사이드미러 좌우각도
    delta_ud_angle = (q - degrees(atan2(target_C, target_E)))/2 # 바뀐차량에서 사용자가 움직여야하는 사이드미러 상하각도
    
    return Drivepos(delta_a, delta_b, delta_lr_angle_left, delta_lr_angle_right, delta_ud_angle, target)


def getToMove(setting,current):
    return Drivepos(setting.a_u - current.a_u, setting.b_u - current.b_u, setting.lr_angle_left - current.lr_angle_left, setting.lr_angle_right - current.lr_angle_left , setting.ud_angle - current.ud_angle, setting.model)



def Simulation(current, change, driver_height):
    
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
    while True:
        rate(30)
        k = keysdown() # a list of keys that are down
        if 'left'  in k:
            car_seat.pos.x -= dv
            car_seat_back.pos.x -=dv
            eye.pos.x -= dv
            back_and_forth_sum += dv
            print(back_and_forth_sum)
        if 'right' in k: 
            car_seat.pos.x += dv
            car_seat_back.pos.x +=dv
            eye.pos.x += dv
            back_and_forth_sum  -= dv
            print(back_and_forth_sum)
            
        if 'down' in k: 
            car_seat.pos.y -= dv
            car_seat_back.pos.y -=dv
            eye.pos.y -= dv
            up_and_down_sum -= dv
            print(up_and_down_sum)
            
        if 'up' in k: 
            car_seat.pos.y += dv
            car_seat_back.pos.y +=dv
            eye.pos.y += dv
            up_and_down_sum += dv
            print(up_and_down_sum)
        
        if 'a' in k : 
            left_side_mirror.rotate(angle =  -dv2, axis = vec(0,1,0))
            theta1_sum -= dv2
            print(theta1_sum)
        if 'd' in k :
            left_side_mirror.rotate(angle = dv2, axis = vec(0,1,0))
            theta1_sum += dv2
            print(theta1_sum)
        if 's' in k :
            left_side_mirror.rotate(angle =  dv2, axis = vec(1,0,0))
            theta3_sum += dv2
            print(theta3_sum)
        if 'w' in k :
            left_side_mirror.rotate(angle =  -dv2, axis = vec(1,0,0))
            theta3_sum -= dv2
            print(theta3_sum)
        
        if 'j' in k : 
            right_side_mirror.rotate(angle = -dv2, axis = vec(0,1,0))
            theta2_sum -= dv2
            print(theta2_sum)
        if 'l' in k :
            right_side_mirror.rotate(angle = dv2, axis = vec(0,1,0))
            theta2_sum += dv2
            print(theta2_sum)
        if 'k' in k : 
            right_side_mirror.rotate(angle = -dv2, axis = vec(1,0,0))
            theta4_sum -= dv2
            print(theta4_sum)
        if 'i' in k :
            right_side_mirror.rotate(angle = dv2, axis = vec(1,0,0))
            theta4_sum += dv2
            print(theta4_sum)
    
#****예시 상황****
#    모닝에서 DrivePosition을 저장한 사용자가 그랜저를 운전하려는 상황
#    이전에 한번 등록한 차량 세팅값을 이용하여 새로운 차량에서 사용자 맞춤 세팅값을 적용.
#*/
#/*
#****IO Description****
#    -input-
#    
#    <차량재원>
#     페달 ~ 시트를 맨앞으로 당겼을때의 거리
#     차량내부 바닥 ~ 시트를 맨아래로 내렸을때의 거리
#     사이드미러 중앙 ~ 시트를 맨앞으로 당겼을때 눈위치(사람머리두께를 약 17 ~ 18cm 라고 가정, 차량 옆면과 수평이 되는 거리측정.)
#     좌측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
#     우측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
#     차량내부 바닥 ~ 대시보드
#     차량내부 바닥 ~ 사이드미러 중앙까지의 높이
#     대시 ~ 천장
#    
#    <사용자 특성값>
#     사용자가 앉았을때 엉덩이 ~ 눈높이 << 사용자의 키입력으로 부터 받아옴. => 이후 카메라 센서를 이용하여 측정을 자동화 하는 방법이 있음.
#    
#    <사용자 세팅값>
#     초기 차량에서 조정한 시트와 사이드미러의 조정값.
#     
#    -process-
#    1. input값을 토대로 사용자 특성을 추출
#     시트x축 : 사용자의 편안한 공간 확보
#     시트y축 : 
#      / ver 1 : 바닥에서 편안한 공간을 확보한 값을 이용하여 시트조정
#      / ver 2 : 대시보드에서 시선이 올라오는 고정값으로 시트조정 
#      / ver 3: 대시보드에 사용자 시선이 위치하는 지점의 비율을 고려하여 시트조정.
#     사이드미러 좌우,상하 : 
#      / 사용자가 미러를 바라봤을때 보이는 시야의 방향을 고려하여 각도 조절. (즉, 사이드 미러에서 반사된 사용자의 시야각)
#      / default : 시야각을 90도. 즉, 거울을 정면에서 바라봤을 때 보이는 장면을 볼 수 있게 설정.
#    2. 추출된 사용자 특성을 토대로 새로운 차량에 적용.
#    3. 새로운 차량에 적용되있던 포지션에서 1,2 에서 구한 포지션을 적용.
#    
#    -output-
#    1. 새로운 차에서의 개인 포지션
#    2. 움직일 값
#*/



#차종별 상수 세팅
Morning = CarModel(34, 30, 63.5, 50.5, 103.5, 77, 77, 35, "Morning") # 가상의 값 (6, 7 ,8)
Avante = CarModel(34, 30, 74, 55, 125, 77, 77, 38,"Avante") # 가상의 값 (2, 8)
Genesis_G70 = CarModel(34, 29, 51, 57, 134, 77, 80, 40, "Genesis_G70") # 현재 제네시스만 정확.



setting_Model= Drivepos(4, 5, 50, 48, 35, Morning)
current_Model_setting = Drivepos(1, 2, 0, 0, 0, Avante)
#{ x축 조정값, y축조정값, 사이드미러 좌측 조정값, 사이드미러 우측 조정값, 사이드미러 상하 조정값, 차량모델 }*/

hip_to_eye=0.0 # 엉덩이 ~ 시야까지의 거리.(키로 부터 일정한 비율로 받아옴)
default_setting = 0 # 사용자취향x 표준값 적용.(선택사항)
ver=0 # ver 2 : 대시보드에서 시선이 올라오는 고정값으로 시트조정 // ver 3: 대시보드에 사용자 시선이 위치하는 지점의 비율을 고려하여 시트조정.

# 엉덩이에서 눈높이 까지의 길이
hip_to_eye = float(input("Enter your height : "))# 키입력
hip_to_eye *= 0.44 # 키와 엉덩이에서 눈높이까지의 길이에 대한 연관관계

#//입력 모델의 세팅 출력
print("setting Model");
print("x : {}".format(setting_Model.a_u))
print("y : {}".format(setting_Model.b_u))
print("lr_angle_left : {}".format(setting_Model.lr_angle_left))
print("lr_angle_right : {}".format(setting_Model.lr_angle_right))
print("ud_angle : {}".format(setting_Model.ud_angle))
print("model name : {}".format(setting_Model.model.name))

print("\n\n");

#//현재 차량 모델에 따라 변환된 세팅값 출력
while(True):
      default_setting = int(input("Do you want default setting?? (YES:1 NO:0): "))
      if default_setting==0 or default_setting==1:
          break
      else:
          print("plz check you had entered..")


while(True):
      ver = int(input("choose height version (1 or 2 or 3): "))
      if ver==1 or ver==2 or ver==3:
          break
      else:
          print("plz check you had entered..")

get_transformed_setting = transformModel(setting_Model, Avante, hip_to_eye, default_setting, ver)

print("setting Avante(transformed)")
print("x : {}".format(get_transformed_setting.a_u))
print("y : {}".format(get_transformed_setting.b_u))
print("lr_angle_left : {}".format(get_transformed_setting.lr_angle_left))
print("lr_angle_left : {}".format(get_transformed_setting.lr_angle_right))
print("ud_angle : {}".format(get_transformed_setting.ud_angle))
print("model name : {}".format(get_transformed_setting.model.name))

print("\n\n")

#얼마나 움직여야 하는지 출력`
toMove = getToMove(get_transformed_setting, current_Model_setting)
print("to move\nx {}\ny {}\nlr_angle_left {}\nlr_angle_right {}\nud_angle {}\n".format(toMove.a_u, toMove.b_u, toMove.lr_angle_left, toMove.lr_angle_right, toMove.ud_angle))


Simulation(current_Model_setting, toMove, hip_to_eye/0.44)

    
    

