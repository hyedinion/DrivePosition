package com.example.driveposition2.Model;

public class Drivepos {
    public float a_u; // 사용자가 이동시킨 x값
    public float b_u; // 사용자가 이동시킨 y값
    public float lr_angle_left; // 사용자가 설정시킨 좌우 사이드미러 angle (차량 옆면 기준)
    public float lr_angle_right; // 사용자가 설정시킨 좌우 사이드미러 angle (차량 옆면 기준)
    public float ud_angle; // 사용자가 설정시킨 상하 사이드미러 angle (미러의 기울기)
    public CarModel model;
}
