class Drivepos
{
    
    private final class CarModel
    {
        float a_d; // 페달 ~ 시트를 맨앞으로 당겼을때의 거리
        float b_d; // 차량내부 바닥 ~ 시트를 맨아래로 내렸을때의 거리
        float c; // 사이드미러 중앙 ~ 시트를 맨앞으로 당겼을때 눈위치(사람머리두께를 약 17 ~ 18cm 라고 가정, 차량 옆면과 수평이 되는 거리측정.)
        float d_left; // 좌측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
        float d_right; // 우측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
        float e; // 차량내부 바닥 ~ 대시보드
        float f; // 차량내부 바닥 ~ 사이드미러 중앙까지의 높이
        float g; // 대시 ~ 천장
    
        String name;
    }

    public static void main(String args[])
    {
        System.out.println("Hello world~");
    }
}