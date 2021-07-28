from transform_base import *
from transform_utils import transformModel, getToMove

'''/*
****예시 상황****
   모닝에서 DrivePosition을 저장한 사용자가 그랜저를 운전하려는 상황
   이전에 한번 등록한 차량 세팅값을 이용하여 새로운 차량에서 사용자 맞춤 세팅값을 적용.
*/'''
'''/*
****IO Description****
   -input-
   
   <차량재원> : CarModel
    페달 ~ 시트를 맨앞으로 당겼을때의 거리
    차량내부 바닥 ~ 시트를 맨아래로 내렸을때의 거리
    사이드미러 중앙 ~ 시트를 맨앞으로 당겼을때 눈위치(사람머리두께를 약 17 ~ 18cm 라고 가정, 차량 옆면과 수평이 되는 거리측정.)
    좌측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
    우측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
    차량내부 바닥 ~ 대시보드
    차량내부 바닥 ~ 사이드미러 중앙까지의 높이
    대시 ~ 천장
   
   <사용자 특성값> : PersonalConst
    사용자가 앉았을때 엉덩이 ~ 눈높이 << 사용자의 키입력으로 부터 받아옴. => 이후 카메라 센서를 이용하여 측정을 자동화 하는 방법이 있음.
   
   <사용자 세팅값> : Drivepos
    초기 차량에서 조정한 시트와 사이드미러의 조정값.
    
   -process-
   1. input값을 토대로 사용자 특성을 추출
    시트x축 : 사용자의 편안한 공간 확보
    시트y축 : 
     / ver 1 : 바닥에서 편안한 공간을 확보한 값을 이용하여 시트조정
     / ver 2 : 대시보드에서 시선이 올라오는 고정값으로 시트조정 
     / ver 3: 대시보드에 사용자 시선이 위치하는 지점의 비율을 고려하여 시트조정.
    사이드미러 좌우,상하 : 
     / 사용자가 미러를 바라봤을때 보이는 시야의 방향을 고려하여 각도 조절. (즉, 사이드 미러에서 반사된 사용자의 시야각)
     / default : 시야각을 90도. 즉, 거울을 정면에서 바라봤을 때 보이는 장면을 볼 수 있게 설정.
   2. 추출된 사용자 특성을 토대로 새로운 차량에 적용.
   3. 새로운 차량에 적용되있던 포지션에서 1,2 에서 구한 포지션을 적용.
   
   -output-
   1. 새로운 차에서의 개인 포지션
   2. 움직일 값
*/'''
def main():
    #차종별 상수 세팅
    
    # setting(a~g)
    Morning = CarModel(34, 30, 63.5, 50.5, 103.5, 77, 77, 35, "Morning") # 가상의 값 (6, 7 ,8)
    Avante = CarModel(34, 30, 74, 55, 125, 77, 77, 38,"Avante") # 가상의 값 (2, 8)
    Genesis_G70 = CarModel(34, 29, 51, 57, 134, 77, 80, 40, "Genesis_G70") # 현재 제네시스만 정확.
    
    # test model
    TestModel = CarModel(0,0,0,0,0,0,0,0,"test") # 1. 테스트 데이터값 입력.

    ## 실측값 (a_u,b_u,lr_angle_left,lr_angle_right,ud_angle)
    setting_Model_Morning = [Drivepos(0, 5, 48, 35, 35, Morning),
                            Drivepos(15, 0, 48, 48, 35, Morning),
                            Drivepos(12.5, 2, 48, 48, 35, Morning),
                            Drivepos(13.5, 2, 48, 48, 35, Morning),
                            Drivepos(6, 0, 48, 48, 35, Morning)]
    setting_Model_Avante = [Drivepos(4,0,48,35,35,Avante),
                            Drivepos(12,0,48,35,35,Avante),
                            Drivepos(14,0,48,35,35,Avante),
                            Drivepos(13,0,48,48,48,Avante),
                            Drivepos(7,0,48,48,48,Avante)]
    setting_Model_Genesis_G70 = [Drivepos(1,0,48,35,35,Genesis_G70),
                                 Drivepos(16,0,48,35,35,Genesis_G70),
                                 Drivepos(9,0,48,35,35,Genesis_G70),
                                 Drivepos(12,0,48,35,35,Genesis_G70),
                                 Drivepos(6,0,48,35,35,Genesis_G70)]


    choose =int(input("1: Morning, 2:Avante, 3:Genesis : "))
    if choose ==1:
        setting_Model = setting_Model_Morning
    elif choose ==2:
        setting_Model = setting_Model_Avante
    elif choose ==3:
        setting_Model = setting_Model_Genesis_G70
    print("")
    hip_to_eye=0.0 # 엉덩이 ~ 시야까지의 거리.(키로 부터 일정한 비율로 받아옴)
    default_setting = 0 # 사용자취향x 표준값 적용.(선택사항)
    ver=0 # ver 2 : 대시보드에서 시선이 올라오는 고정값으로 시트조정 // ver 3: 대시보드에 사용자 시선이 위치하는 지점의 비율을 고려하여 시트조정.

    # 엉덩이에서 눈높이 까지의 길이
    hip_to_eye = [176,156,180,172,160] # 2. 키입력
    for i in range(0, len(hip_to_eye)):
        hip_to_eye[i] = hip_to_eye[i] * 0.438 + 5.0973 # 키와 엉덩이에서 눈높이까지의 길이에 대한 연관관계
        hip_to_eye[i] = round(hip_to_eye[i],4)

## 출력

    for i in range(0,len(setting_Model)):
        print("***** User",i+1," *****")
        #//입력 모델의 세팅 출력
        print("setting Model")
        print("x : {}".format(setting_Model[i].a_u))
        print("y : {}".format(setting_Model[i].b_u))
        print("lr_angle_left : {}".format(setting_Model[i].lr_angle_left))
        print("lr_angle_right : {}".format(setting_Model[i].lr_angle_right))
        print("ud_angle : {}".format(setting_Model[i].ud_angle))
        print("model name : {}".format(setting_Model[i].model.name))


        #//현재 차량 모델에 따라 변환된 세팅값 출력
        while(True):
            ver = int(input("choose height version (1 or 2 or 3): "))
            if ver==1 or ver==2 or ver==3:
                break
            else:
                print("plz check you had entered..")

        while(True):
            default_setting = int(input("Do you want default setting?? (YES:1 NO:0): "))
            if default_setting==0 or default_setting==1:
                break
            else:
                print("plz check you had entered..")
        print("\n")

         #// 여기에 새로운 자동차 모델 입력.
        get_transformed_setting = transformModel(setting_Model[i], TestModel, PersonalConst(hip_to_eye[i], default_setting), ver)
        print("User",i+1,"setting {} (transformed)".format(TestModel.name))
        print("x : {}".format(get_transformed_setting.a_u))
        print("y : {}".format(get_transformed_setting.b_u))
        print("lr_angle_left : {}".format(get_transformed_setting.lr_angle_left))
        print("lr_angle_left : {}".format(get_transformed_setting.lr_angle_right))
        print("ud_angle : {}".format(get_transformed_setting.ud_angle))
        print("model name : {}".format(get_transformed_setting.model.name))
        print("\n\n")

if __name__=='__main__':
    main()