#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef const struct _CarModel{
    /* data */

    float a_d; // 페달 ~ 시트를 맨앞으로 당겼을때의 거리
    float b_d; // 차량내부 바닥 ~ 시트를 맨아래로 내렸을때의 거리
    float c; // 사이드미러 중앙 ~ 시트를 맨앞으로 당겼을때 눈위치(사람머리두께를 약 17 ~ 18cm 라고 가정, 차량 옆면과 수평이 되는 거리측정.)
    float d_left; // 좌측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
    float d_right; // 우측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
    float e; // 차량내부 바닥 ~ 대시보드
    float f; // 차량내부 바닥 ~ 사이드미러 중앙까지의 높이

    char name[20];
} CarModel;

typedef struct _Drivepos
{
    /* data */
    float a_u; // 사용자가 이동시킨 x값
    float b_u; // 사용자가 이동시킨 y값
    float lr_angle_left; // 사용자가 설정시킨 좌우 사이드미러 angle (차량 옆면 기준)
    float lr_angle_right; // 사용자가 설정시킨 좌우 사이드미러 angle (차량 옆면 기준)
    float ud_angle; // 사용자가 설정시킨 상하 사이드미러 angle (미러의 기울기)
    
    CarModel model;    
} Drivepos;

Drivepos transformModel(Drivepos setting, CarModel target, float hip_to_eye, int default_setting)
{
    /* 사용자의 성향 반영한 변수*/
    
    /* 좌석시트 */
    float A = setting.a_u + setting.model.a_d; // 사용자가 편안하다고 느끼는 공간
    float delta_a = A - target.a_d; // 바뀐차량에서 사용자가 움직여야하는 x값
    
    float B = - setting.b_u - setting.model.b_d + setting.model.e; // 조정된 시트에서 대쉬보드까지의 높이
    float delta_b = - B - target.b_d + target.e; // 바뀐차량에서 사용자가 움직여야하는 y값
    
    /* 사이드미러 */
    float setting_C = setting.a_u + setting.model.c; // 사이드미러 중앙 ~ 시트설정후 사용자의 눈위치 (차량 옆면과 수평이 되는 거리)
    float target_C = delta_a + target.c;
    
    float setting_D_left = setting.model.d_left;  // 좌측 사이드미러 중앙 ~ 차량시트 중앙까지의 거리
    float target_D_left = target.d_left;
    float setting_D_right = setting.model.d_right;  // 우측 사이드미러 중앙 ~ 차량시트 중앙까지의 거리
    float target_D_right = target.d_right;
    
    float setting_E = setting.b_u + setting.model.b_d + hip_to_eye - setting.model.f;  // 사이드미러 중앙 ~ 사용자의 눈높이 // (바닥 ~ 조정된시트의 높이) + (사람의 엉덩이 ~ 눈위치) - (바닥 ~ 미러)
    float target_E = delta_b + target.b_d + hip_to_eye - target.f;         
    
    float p_left; // 좌측사이드 좌우 시야각의 각도 (사이드미러에서 바라봤을때의 좌우시야 각) // 사용자 취향반영 (바깥쪽(>90), 중간(90), 안쪽(<90)..)
    float p_right; // 우측사이드 좌우 시야각의 각도 (사이드미러에서 바라봤을때의 좌우시야 각) // 사용자 취향반영 (바깥쪽(>90), 중간(90), 안쪽(<90)..)
    float q; // 상하 시야각의 각도 (사이드미러에서 바라봤을때의 상하시야 각) // 사용자 취향반영 (위(>90), 중간(90), 아래(<90)..)
    
    if(default_setting ==1){ // 표준값으로 세팅 (시야가 차체 방향과 나란하게 나감.)
    float p_left = 90;
    float p_right = 90;
    float q = 90;
    }
    else if(default_setting ==0){ // 사용자 취향고려
    float p_left = 2*setting.lr_angle_left - atan2(setting_C, setting_D_left); 
    float p_right = 2*setting.lr_angle_right - atan2(setting_C, setting_D_right); 
    float q = 2*setting.ud_angle + atan2(setting_C, setting_E); 
    }
    
    float delta_lr_angle_left = (p_left + atan2(target_C, target_D_left))/2; // 바뀐차량에서 사용자가 움직여야하는 사이드미러 좌우각도
    float delta_lr_angle_right = (p_right + atan2(target_C, target_D_right))/2; // 바뀐차량에서 사용자가 움직여야하는 사이드미러 좌우각도
    float delta_ud_angle = (q - atan2(target_C, target_E))/2; // 바뀐차량에서 사용자가 움직여야하는 사이드미러 상하각도
    
    return (Drivepos){delta_a, delta_b, delta_lr_angle_left, delta_lr_angle_right, delta_ud_angle, target};
}

Drivepos getToMove(Drivepos setting, Drivepos current)
{
    return (Drivepos){setting.a_u - current.a_u, setting.b_u - current.b_u, setting.lr_angle_left - current.lr_angle_left, setting.lr_angle_right - current.lr_angle_left , setting.ud_angle - current.ud_angle, setting.model};
}
/*
****예시 상황****
    모닝에서 DrivePosition을 저장한 사용자가 그랜저를 운전하려는 상황
    이전에 한번 등록한 차량 세팅값을 이용하여 새로운 차량에서 사용자 맞춤 세팅값을 적용.
*/
/*
****IO Description****
    -input-
    
    <차량재원>
     페달 ~ 시트를 맨앞으로 당겼을때의 거리
     차량내부 바닥 ~ 시트를 맨아래로 내렸을때의 거리
     사이드미러 중앙 ~ 시트를 맨앞으로 당겼을때 눈위치(사람머리두께를 약 17 ~ 18cm 라고 가정, 차량 옆면과 수평이 되는 거리측정.)
     좌측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
     우측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
     차량내부 바닥 ~ 대시보드
     차량내부 바닥 ~ 사이드미러 중앙까지의 높이
    
    <사용자 특성값>
     사용자가 앉았을때 엉덩이 ~ 눈높이 << 사용자의 키입력으로 부터 받아옴. => 이후 카메라 센서를 이용하여 측정을 자동화 하는 방법이 있음.
    
    <사용자 세팅값>
     초기 차량에서 조정한 시트와 사이드미러의 조정값.
     
    -process-
    1. input값을 토대로 사용자 특성을 추출
     시트x축 : 사용자의 편안한 공간 확보
     시트y축 : 차량의 대시보드에서 부터 올라온 눈높이
     사이드미러 좌우,상하 : 사용자가 미러를 바라봤을때 보이는 시야의 방향 (즉, 사이드 미러에서 반사된 사용자의 시야각)
    2. 추출된 사용자 특성을 토대로 새로운 차량에 적용.
    3. 새로운 차량에 적용되있던 포지션에서 1,2 에서 구한 포지션을 적용.
    
    -output-
    1. 새로운 차에서의 개인 포지션
    2. 움직일 값
*/



//차종별 상수 세팅
CarModel Morning = {34, 30, 63.5, 50.5, 103.5, 70, 70, "Morning"}, // 가상의 값 (6, 7)
         Avante = {34, 30, 74, 55, 125, 77, 77, "Avante"},        // 가상의 값 (2)

         Genesis_G70 = {34, 29, 51, 57, 134, 77, 80, "Genesis_G70"} // 현재 제네시스만 정확.
         ;

int main()
{   
    Drivepos setting_Model= {4, 5, 50, 48, 15, Morning}, current_Model_setting = {1, 2, 0, 0, 0, Avante};
    /*{ x축 조정값, y축조정값, 사이드미러 좌측 조정값, 사이드미러 우측 조정값, 사이드미러 상하 조정값, 차량모델 }*/
    
    float hip_to_eye; // 엉덩이 ~ 시야까지의 거리.(키로 부터 일정한 비율로 받아옴)
    int default_setting = 0; // 사용자취향x 표준값 적용.(선택사항)
    
    // 엉덩이에서 눈높이 까지의 길이
    printf("Enter your height : "); // 키입력
    scanf("%f",&hip_to_eye);
    hip_to_eye *= 0.44; // 키와 엉덩이에서 눈높이까지의 길이에 대한 연관관계
    
    //입력 모델의 세팅 출력
    printf("setting Model\n");
    printf("x : %f\n", setting_Model.a_u);
    printf("y : %f\n", setting_Model.b_u);
    printf("lr_angle_left : %f\n", setting_Model.lr_angle_left);
    printf("lr_angle_right : %f\n", setting_Model.lr_angle_right);
    printf("ud_angle : %f\n", setting_Model.ud_angle);
    printf("model name : %s\n", setting_Model.model.name);

    printf("\n\n\n");

    //현재 차량 모델에 따라 변환된 세팅값 출력
    while(1)
    {  
      printf("Do you want default setting?? (YES:1 NO:0):");
      scanf("%d",&default_setting);
       if(default_setting==0 || default_setting==1)
          break;
       else
           printf("plz check you had entered..");
    }
    Drivepos get_transformed_setting = transformModel(setting_Model, Avante, hip_to_eye, default_setting);
    
    printf("setting Avante(transformed)\n");
    printf("x : %f\n", get_transformed_setting.a_u);
    printf("y : %f\n", get_transformed_setting.b_u);
    printf("lr_angle_left : %f\n", get_transformed_setting.lr_angle_left);
    printf("lr_angle_left : %f\n", get_transformed_setting.lr_angle_right);
    printf("ud_angle : %f\n", get_transformed_setting.ud_angle);
    printf("model name : %s\n", get_transformed_setting.model.name);

    printf("\n\n\n");

    //얼마나 움직여야 하는지 출력
    Drivepos toMove = getToMove(get_transformed_setting, current_Model_setting);
    printf("to move\nx %f\ny %f\nlr_angle_left %f\nlr_angle_right %f\nud_angle %f\n", toMove.a_u, toMove.b_u, toMove.lr_angle_left, toMove.lr_angle_right, toMove.ud_angle);

    return 0;
}
