#include <stdio.h>
#include <stdlib.h>

typedef const struct _Model{
    /* data */
    float x;
    float y;
    char name[20];
} CarModel;

typedef struct _Drivepos
{
    /* data */
    float x;
    float y;
    CarModel model;
} Drivepos;


Drivepos transformModel(Drivepos setting, CarModel target)
{
    float real_x = setting.x + setting.model.x;
    float real_y = setting.y + setting.model.y;

    return (Drivepos){real_x - target.x, real_y - target.y, target};
}

Drivepos getToMove(Drivepos setting, Drivepos current)
{
    return (Drivepos){setting.x - current.x, setting.y - current.y, setting.model};
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
    Drivepos setting_Moring= {15, 15, Morning}, current_Grandeur = {8, 20, Grandeur};
    
    printf("setting Morning\n");
    printf("x : %f\n", setting_Moring.x);
    printf("y : %f\n", setting_Moring.y);
    printf("model name : %s\n", setting_Moring.model.name);

    printf("\n\n\n");

    Drivepos setting_Grandeur = transformModel(setting_Moring, Grandeur);
    printf("setting Grandeur(transformed)\n");
    printf("x : %f\n", setting_Grandeur.x);
    printf("y : %f\n", setting_Grandeur.y);
    printf("model name : %s\n", setting_Grandeur.model.name);

    printf("\n\n\n");

    Drivepos toMove = getToMove(setting_Grandeur, current_Grandeur);
    printf("to move\nx %f\ny %f\n", toMove.x, toMove.y);
    return 0;
}