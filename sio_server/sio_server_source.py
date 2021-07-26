import socketio
import eventlet
from ..transform_model.transformModel import CarModel, Drivepos, transformModel

ISVPYTHON = True

#create a Socket.IO server
sio = socketio.Server()
app = socketio.WSGIApp(sio)

#클라이언트(차 시트)와 통신을 통해 주고받아야 하는 경우.
#vpython 환경에서는 로컬 변수로 데이터를 주고받으므로, 불필요
if ISVPYTHON:
    Avante = CarModel(34, 30, 74, 55, 125, 77, 77, 38,"Avante")
    car_dummy = Drivepos(1, 2, 0, 0, 0, Avante)
else:
    sio_Car = socketio.Client()
    sio_Car.connect('')
    sio_Car.emit('my message', {'foo':'bar'})

@sio.event
def ev_connect(sid, environ):
    print('connect ', sid)

@sio.event
def ev_disconnect(sid):
    print('disconnect ', sid)

#####################

@sio.on('my message')
def on_test(sid,json):
    #print(sid)
    print(sid, json)

#App으로부터의 사용자 세팅 저장 요청
#현재 차량의 세팅 로드하여 반환
@sio.on('save_request')
def on_save_request(sid, json):
    sio.emit('save_send', dict(car_dummy) )
    print('save_request', sid, json)

#App으로부터의 사용자 세팅 적용 요청
#전달받은 세팅 기반으로 적용
@sio.on('apply')
def on_apply(sid, json):
    pass

@sio.on('connect')
def on_connect():
    sio.emit('connect_response', {})
    pass





#eventlet.wsgi.server(eventlet.listen(('0.0.0.0',5000)),app)