## link for simulation https://www.glowscript.org/#/user/wlals4629/folder/MyPrograms/program/practice02
GlowScript 3.1 VPython

side_mirror_left = box(pos = vec(0.3, 0.1, -(0.125+0.075/2)), length = 0.1, height=0.02 , width = 0.001,  color = color.magenta)

side_mirror_left.rotate(angle = pi/15, axis=vec(1,0,0))

side_mirror_left.rotate(angle = -pi/5, axis = vec(0,1,0))

side_mirror_right = box(pos = vec(0.3, 0.1, 0.4125), length = 0.1, height=0.02 , width = 0.001,  color = color.purple)

side_mirror_right.rotate(angle = -pi/15, axis=vec(1,0,0))

side_mirror_right.rotate(angle = +pi/5, axis = vec(0,1,0))



car_bottom = box(pos = vec(0,-0.075,0.125), length = 1, height=0.05, width = 0.5 )


check_origin = box(pos= vec(0,0,0), length = 0.01, height = 0.01, width = 0.01, color = color.green)


seat_bottom = box(pos = vec(-0.2, 0, 0), length = 0.2, height=0.05 , width = 0.15,  color = color.blue )
seat_back = box(pos = vec(-0.4, 0, 0), length = 0.2, height=0.05 , width = 0.15,  color = color.red)


theta22= 0
dtheta = pi/30
theta = 0
theta2 = 0
theta_sum=0
while (theta <10):
    rate(10)
    seat_bottom.pos.x = seat_bottom.pos.x + 0.01
    seat_back.pos.x = seat_back.pos.x + 0.01
    theta= theta+1




while (theta22 <10):
    rate(10)
    seat_bottom.pos.y = seat_bottom.pos.y + 0.01
    seat_back.pos.y = seat_back.pos.y + 0.01
    theta22 = theta22 + 1


temp3 = seat_back.pos
temp3 = temp3 + vec(0,0.1,0)

temp2 = seat_back.pos
temp2 = temp2 + vec(0.1,0.1,0)


while (theta_sum <= pi/25):
    rate(10)
    seat_back.rotate(angle = -theta_sum, axis = vec(0,0,1), origin = vec(-0.2, 0.1,0))
    theta_sum = (theta2 + dtheta)
    



box(pos = vec(1, 0, 0), length = 0.1, height=0.05/2 , width = 0.15/2,  color = color.magenta)
