import time
import socketio
import RPi.GPIO as GPIO
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar


def remap(changingVariable, oldMin, oldMax, newMin, newMax):

    # range check
    # if oldMin == oldMax:
    #     print("Warning: Zero input range")
    #     return None

    # if newMin == newMax:
    #     print("Warning: Zero output range")
    #     return None

    # check reversed input range
    # reverseInput = False
    # oldMin = min(oldMin, oldMax)
    # oldMax = max(oldMin, oldMax)
    # if not oldMin == oldMin:
    #     reverseInput = True

    # # check reversed output range
    # reverseOutput = False
    # newMin = min(newMin, newMax)
    # newMax = max(newMin, newMax)
    div1 = oldMax-oldMin
    div2 = oldMax-oldMin
    # if div1==0:
    #     div1=+ 0.001
    # if div2==0:
    #     div2=+00.1
    # if not newMin == newMin:
    #     reverseOutput = True

    portion = (changingVariable-oldMin)*(newMax-newMin)/div1
    # if reverseInput:
    #     portion = (oldMax-changingVariable)*(newMax-newMin)/div2

    result = portion + newMin
    # if reverseOutput:
    #     result = newMax - portion
    # print(result)
    return result


sio = socketio.Client()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PORT_NAME = "/dev/ttyS0"
lidar = RPLidar(None, PORT_NAME)

max_distance = 0
scan_data = [0]*360


class Motor():
    def __init__(self, Ena, In1, In2):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(self.Ena, GPIO.OUT)
        GPIO.setup(self.In1, GPIO.OUT)
        GPIO.setup(self.In2, GPIO.OUT)
        self.pwm = GPIO.PWM(self.Ena, 100)
        self.pwm.start(0)

    def moveF(self):
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)

    def moveB(self):
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)

    def stop(self):
        GPIO.output(self.Ena, GPIO.LOW)

    def drive(self, s):
        self.pwm.ChangeDutyCycle(s)


Motor1 = Motor(4, 17, 27)
Motor2 = Motor(24, 23, 22)
Motor3 = Motor(26, 16, 13)
Motor4 = Motor(12, 6, 7)


def process_data(data):
    global max_distance
    d = []
    for angle in range(360):
        distance = data[angle]
        if distance > 0:
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119),
                     120 + int(y / max_distance * 119))
            d.append(point)
    return d


def lidar_scan(m1, m2, m3, m4):
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
    cart = process_data(scan_data)
    sio.emit("lidar", cart)
    carDrive(m1, m2, m3, m4)


def carStop():
    Motor1.stop()
    Motor2.stop()
    Motor3.stop()
    Motor4.stop()


def carDrive(m1Speed, m2Speed, m3Speed, m4Speed):
    Motor1.drive(m1Speed)
    Motor2.drive(m2Speed)
    Motor3.drive(m3Speed)
    Motor4.drive(m4Speed)


def moveLeftF():
    Motor1.moveF()
    Motor4.moveF()


def moveRightF():
    Motor2.moveF()
    Motor3.moveF()


def moveLeftB():
    Motor1.moveB()
    Motor4.moveB()


def moveRightB():
    Motor2.moveB()
    Motor3.moveB()


try:
    @sio.event
    def connect():
        print('connection established')
        sio.emit("ID", 'RescueRover')
        lidar_scan()

    @sio.on('drive-orders')
    def on_message(angle, speed, mode):

        asMultiplier = angle * speed
        sMultM1 = round(speed * mode['m1'])
        sMultM2 = round(speed * mode['m2'])
        sMultM3 = round(speed * mode['m3'])
        sMultM4 = round(speed * mode['m4'])
        motor1Speed = 0
        motor2Speed = 0
        motor3Speed = 0
        motor4Speed = 0

        # Speed Limiter
        if speed < 0.05:
            carStop()

        # First Quadrant
        elif angle > 0 and angle < 90:

            motor1Speed = sMultM1
            motor4Speed = sMultM4
            moveLeftF()
            motor2Speed = round(remap(asMultiplier, 0, 90, 0, mode['m2']))
            motor3Speed = round(remap(asMultiplier, 0, 90, 0, mode['m3']))
            moveRightB()

        # Second Quadrant
        elif angle > 90 and angle < 180:
            motor1Speed = round(remap(asMultiplier, 90, 180, mode['m1'], 0))
            motor4Speed = round(remap(asMultiplier, 90, 180, mode['m4'], 0))
            moveLeftF()
            motor2Speed = sMultM2
            motor3Speed = sMultM3
            moveRightB()

        # Third Quadrant
        elif angle < -90 and angle > -180:
            motor1Speed = round(remap(asMultiplier, -180, -90, 0, mode['m1']))
            motor4Speed = round(remap(asMultiplier, -180, -90, 0, mode['m4']))
            moveLeftB()
            motor2Speed = sMultM2
            motor3Speed = sMultM3
            moveRightF()

        # Fourth Quadrant
        elif angle < 0 and angle > -90:
            motor1Speed = sMultM1
            motor4Speed = sMultM4
            moveLeftB()
            motor2Speed = round(remap(asMultiplier, -90, 0, mode['m2'], 0))
            motor3Speed = round(remap(asMultiplier, -90, 0, mode['m3'], 0))
            moveRightF()
            # print(
            #     f"| 2 speed: {motor2Speed} | 3 speed: {motor3Speed} | Mult: {asMultiplier} | Mpwm {Mpwm[1]} |")

        # print(
            # f"1: {motor1Speed} | 2: {motor2Speed} | 3: {motor3Speed} | 4: {motor4Speed}")

        try:
            lidar_scan(motor1Speed, motor2Speed, motor3Speed, motor4Speed)
            # carDrive(motor1Speed, motor2Speed, motor3Speed, motor4Speed)

        except:
            print("Error")

    @sio.event
    def disconnect():
        print('disconnected from server')
        carStop()
        lidar.stop()
        lidar.disconnect()

    try:
        sio.connect('http://10.13.82.169:3000')

    except:
        sio.connect('http://192.168.250.11:3000')

    sio.wait()

except KeyboardInterrupt:
    print("Thank You For Comming :)")
    time.sleep(0.2)
    carStop()
    lidar.stop()
    lidar.disconnect()
