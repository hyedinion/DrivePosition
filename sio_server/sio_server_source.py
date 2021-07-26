from typing import Dict
from transform_model.transformModel import transformModel
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
    Morning = CarModel(34, 30, 63.5, 50.5, 103.5, 77, 77, 35, "Morning")
    car_dummy = Drivepos(4, 5, 50, 48, 35, Morning)
else:
    sio_Car = socketio.Client()
    sio_Car.connect('')
    sio.emit('my message', {'foo':'bar'})

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

@sio.on('save_request')
def on_save_request(sid, json):
    sio.emit('save_send', dict(car_dummy) )
    print(sid, json)

@sio.on('apply')
def on_apply(sid, json):
    pass

@sio.on('connect')
def on_connect():
    sio.emit('connect_response', {})
    pass





#eventlet.wsgi.server(eventlet.listen(('0.0.0.0',5000)),app)