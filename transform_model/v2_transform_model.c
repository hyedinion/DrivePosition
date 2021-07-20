#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef const struct _CarModel{
    /* data */

    float a_d; // 페달 ~ 시트를 맨앞으로 당겼을때의 거리
    float b_d; // 차량내부 바닥 ~ 시트를 맨아래로 내렸을때의 거리
    float c; // 사이드미러 중앙 ~ 시트를 맨앞으로 당겼을때 눈위치(사람머리두께를 약 17 ~ 18cm 라고 가정, 차량 옆면과 수평이 되는 거리측정.)
    float d; // 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
    float e; // 차량내부 바닥 ~ 대시보드
    float f; // 차량내부 바닥 ~ 사이드미러 중앙까지의 높이

    char name[20];
} CarModel;

typedef struct _Drivepos
{
    /* data */
    float a_u; // 사용자가 이동시킨 x값
    float b_u; // 사용자가 이동시킨 y값
    float lr_angle; // 사용자가 설정시킨 좌우 사이드미러 angle (차량 옆면 기준)
    float ud_angle; // 사용자가 설정시킨 상하 사이드미러 angle (미러의 기울기)
    
    CarModel model;    
} Drivepos;

Drivepos transformModel(Drivepos setting, CarModel target, float hip_to_eye)
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
    
    float setting_D = setting.d;  // 사이드미러 중앙 ~ 차량시트 중앙까지의 거리
    float target_D = target.d;
    
    float setting_E = setting.b_u + setting.model.b_d + hip_to_eye - setting.model.f;  // 사이드미러 중앙 ~ 사용자의 눈높이 // (바닥 ~ 조정된시트의 높이) + (사람의 엉덩이 ~ 눈위치) - (바닥 ~ 미러)
    float target_E = delta_b + target.b_d + hip_to_eye - target.f;         
             
    float p = 2*setting.lr_angle - atan2(setting_C, setting_D); // 좌우 시야각의 각도 (사이드미러에서 바라봤을때의 좌우시야 각) // 사용자 취향반영 (바깥쪽(>90), 중간(90), 안쪽(<90)..)
    float q = 2*setting.ud_angle + atan2(setting_C, setting_E); // 상하 시야각의 각도 (사이드미러에서 바라봤을때의 상하시야 각) // 사용자 취향반영 (위(>90), 중간(90), 아래(<90)..)
    
    float delta_lr_angle = (p + atan2(target_C, target_D))/2; // 바뀐차량에서 사용자가 움직여야하는 사이드미러 좌우각도
    float delta_ud_angle = (q - atan2(target_C, target_E))/2; // 바뀐차량에서 사용자가 움직여야하는 사이드미러 상하각도
    
    return (Drivepos){delta_a, delta_b, delta_lr_angle, delta_ud_angle, target};
}

Drivepos getToMove(Drivepos setting, Drivepos current)
{
    return (Drivepos){setting.a_u - current.a_u, setting.b_u - current.b_u, setting.lr_angle - current.lr_angle, setting.ud_angle - current.ud_angle, setting.model};
}

/*
****IO Description****
    -input-
    1. 각 차종별 최대한 앞으로 시트를 위치했을 때의 위치(상수값)
    2. 개인이 편하다고 저장한 포지션(단, 어느 차종에서 저장했는지 알아야 함)
    3. 현재 의자의 위치(이전 운전자가 설정한 값)
    -output-
    1. 새로운 차에서의 개인 포지션
    2. 움직일 값(음수면 왼쪽으로)
*/

/*
****예시 상황****
    모닝에서 DrivePosition을 저장한 사용자가 그랜저를 운전하려는 상황
    각종 상수 및 변수값은 임의로 지정한 값임.
    모닝 상수(1, 1) / 그랜저 상수(3, 3)
    모닝에서 사용자가 저장한 값(15, 15)
    현재 의자의 위치(8, 20)
*/

//차종별 상수 세팅
CarModel Grandeur = {3, 3, "Grandeur"}, Morning = {1, 1, "Morning"};

int main()
{   
    float hip_to_eye; // 엉덩이 ~ 시야까지의 거리.(키로 부터 일정한 비율로 받아옴)
    Drivepos setting_Morning= {15, 15, Morning}, current_Grandeur = {8, 20, Grandeur};
    
    // 엉덩이에서 눈높이 까지의 길이
    printf("Enter your height : "); // 키입력
    scanf("%f",&hip_to_eye);
    hip_to_eye *= 0.44 // 키와 엉덩이에서 눈높이까지의 길이에 대한 연관관계
    
    //모닝의 세팅 출력
    printf("setting Morning\n");
    printf("x : %f\n", setting_Morning.a_u);
    printf("y : %f\n", setting_Morning.b_u);
    printf("lr_angle : %f\n", setting_Morning.lr_angle);
    printf("ud_angle : %f\n", setting_Morning.ud_angle);
    printf("model name : %s\n", setting_Morning.model.name);
    /*
    setting Morning
    x : 15
    y : 15
    lr_angle :
    ud_angle :
    model name : Morning
    */
    printf("\n\n\n");

    //모닝의 세팅을 그랜저 세팅으로 변환 후 출력
    Drivepos setting_Grandeur = transformModel(setting_Morning, Grandeur, hip_to_eye);
    printf("setting Grandeur(transformed)\n");
    printf("x : %f\n", setting_Grandeur.a_u);
    printf("y : %f\n", setting_Grandeur.b_u);
    printf("lr_angle : %f\n", setting_Grandeur.lr_angle);
    printf("ud_angle : %f\n", setting_Grandeur.ud_angle);
    printf("model name : %s\n", setting_Grandeur.model.name);
    /*
    setting Grandeur(transformed)
    x : 13
    y : 13
    lr_angle :
    ud_angle :
    model name : Grandeur
    */
    printf("\n\n\n");

    //얼마나 움직여야 하는지 출력
    Drivepos toMove = getToMove(setting_Grandeur, current_Grandeur);
    printf("to move\nx %f\ny %f\nlr_angle %f\nud_angle %f\n", toMove.a_u, toMove.b_u, toMove.lr_angle, toMove.ud_angle);
    /*
    to move
    x 5
    y -7
    */


    return 0;
}
