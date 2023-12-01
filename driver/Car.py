import socketio
import time
import RPi.GPIO as GPIO


def remap(changingVariable, oldMin, oldMax, newMin, newMax):

    # range check
    if oldMin == oldMax:
        print("Warning: Zero input range")
        return None

    if newMin == newMax:
        print("Warning: Zero output range")
        return None

    # check reversed input range
    reverseInput = False
    oldMin = min(oldMin, oldMax)
    oldMax = max(oldMin, oldMax)
    if not oldMin == oldMin:
        reverseInput = True

    # check reversed output range
    reverseOutput = False
    newMin = min(newMin, newMax)
    newMax = max(newMin, newMax)
    if not newMin == newMin:
        reverseOutput = True

    portion = (changingVariable-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-changingVariable)*(newMax-newMin)/(oldMax-oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result


sio = socketio.Client()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


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
Motor4 = Motor(12, 5, 6)


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


try:
    @sio.event
    def connect():
        print('connection established')
        sio.emit("ID", 'RescueRover')

    @sio.event
    def disconnect():
        print('disconnected from server')
        carStop()

    @sio.on('drive-orders')
    def on_message(angle, speed):
        asMultiplier = angle * speed
        maxPWM = 100
        # Speed Limiter
        if speed < 0.05:
            carStop

        # First Quadrant
        elif angle >= 0 and angle < 90:

            motor1Speed = round(maxPWM * speed)
            Motor1.moveF()
            Motor4.moveF()
            motor2Speed = round(remap(asMultiplier, 0, 90, 0, maxPWM))
            Motor2.moveF()
            Motor3.moveF()

        # Second Quadrant
        elif angle > 90 and angle <= 180:
            motor1Speed = round(remap(asMultiplier, 90, 180, maxPWM, 0))
            Motor1.moveF()
            Motor4.moveF()
            motor2Speed = round(maxPWM * speed)
            Motor2.moveB()
            Motor3.moveB()

        # Third Quadrant
        elif angle < 0 and angle > -90:
            motor1Speed = round(remap(asMultiplier, -90, 0, maxPWM, 0))
            Motor1.moveB()
            Motor4.moveB()
            motor2Speed = round(maxPWM * speed)
            Motor2.moveF()
            Motor3.moveF()

        # Fourth Quadrant
        elif angle < -90 and angle >= -180:
            motor1Speed = round(maxPWM * speed)
            Motor1.moveB()
            Motor4.moveB()
            motor2Speed = round(remap(asMultiplier, -180, -90, 0, maxPWM))
            Motor2.moveF()
            Motor3.moveF()

        motor4Speed = motor1Speed
        motor3Speed = motor2Speed

        print("1: " + motor1Speed + "2: " + motor2Speed +
              "3: " + motor3Speed + "4: " + motor4Speed)

        try:
            carDrive(motor1Speed, motor2Speed, motor3Speed, motor4Speed)

        except:
            print("e")

    try:
        sio.connect('http://10.13.82.169:3000')

    except:
        sio.connect('http://192.168.24.11:3000')

    sio.wait()

except KeyboardInterrupt:
    time.sleep(0.5)
    carStop()
