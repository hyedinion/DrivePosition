import math
from transform_base import *

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