package com.example.driveposition2.Model;

import org.json.JSONException;
import org.json.JSONObject;

public class CarModel {
    public float a_d; // 페달 ~ 시트를 맨앞으로 당겼을때의 거리
    public float b_d; // 차량내부 바닥 ~ 시트를 맨아래로 내렸을때의 거리
    public float c; // 사이드미러 중앙 ~ 시트를 맨앞으로 당겼을때 눈위치(사람머리두께를 약 17 ~ 18cm 라고 가정, 차량 옆면과 수평이 되는 거리측정.)
    public float d_left; // 좌측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
    public float d_right; // 우측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
    public float e; // 차량내부 바닥 ~ 대시보드
    public float f; // 차량내부 바닥 ~ 사이드미러 중앙까지의 높이
    public float g; // 대시 ~ 천장
    public String name;

    public CarModel(JSONObject jo) throws JSONException {
        a_d = (float) jo.getInt("a_d");
        b_d = (float) jo.getInt("b_d");
        c = (float) jo.getInt("c");
        d_left = (float) jo.getInt("d_left");
        d_right = (float) jo.getInt("d_right");
        e = (float) jo.getInt("e");
        f = (float) jo.getInt("f");
        g = (float) jo.getInt("g");
        name = jo.getString("name");


    }
}
