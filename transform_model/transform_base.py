class CarModel:
    def __init__(self, a_d, b_d, c, d_left, d_right, e, f, g, name:str):
        self.a_d = a_d          #페달 ~ 시트를 맨앞으로 당겼을때의 거리
        self.b_d = b_d          #차량내부 바닥 ~ 시트를 맨아래로 내렸을때의 거리
        self.c = c              #사이드미러 중앙 ~ 시트를 맨앞으로 당겼을때 눈위치(사람머리두께를 약 17 ~ 18cm 라고 가정, 차량 옆면과 수평이 되는 거리측정.)
        self.d_left = d_left    #좌측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
        self.d_right = d_right  #우측 사이드미러 중앙 ~ 시트 중앙까지의 거리 (차량 옆면과 수직되는 거리측정.)
        self.e = e              #차량내부 바닥 ~ 대시보드
        self.f = f              #차량내부 바닥 ~ 사이드미러 중앙까지의 높이
        self.g = g              #대시 ~ 천장
        self.name:str = name    #차량 모델명

class PersonalConst:
    def __init__(self, hip_to_eye, default_side):
        self.hip_to_eye = hip_to_eye        #엉덩이 ~ 눈
        self.default_side = default_side    #사용자 설정 사이드미러 각 활용 여부

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
