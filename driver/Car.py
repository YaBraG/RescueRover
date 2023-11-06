import socketio
import time
import RPi.GPIO as GPIO

def remap(x, oMin, oMax, nMin, nMax):

    # range check
    if oMin == oMax:
        print("Warning: Zero input range")
        return None

    if nMin == nMax:
        print("Warning: Zero output range")
        return None

    # check reversed input range
    reverseInput = False
    oldMin = min(oMin, oMax)
    oldMax = max(oMin, oMax)
    if not oldMin == oMin:
        reverseInput = True

    # check reversed output range
    reverseOutput = False
    newMin = min(nMin, nMax)
    newMax = max(nMin, nMax)
    if not newMin == nMin:
        reverseOutput = True

    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

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

    def moveF(self, s):
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(s)

    def moveB(self, s):
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(s)


Motor1 = Motor(4, 17, 27)
Motor2 = Motor(24, 23, 22)
Motor3 = Motor(26, 16, 13)
Motor4 = Motor(12, 5, 6)

try:
    @sio.event
    def connect():
        print('connection established')
        sio.emit("ID", 'RescueRover')

    @sio.event
    def disconnect():
        print('disconnected from server')
        

    @sio.on('drive-orders')
    def on_message(angle, speed):
        asMultiplier = angle * speed

        # Speed Limiter
        if speed < 0.05:
            motor1Speed = 0
            motor2Speed = 0

        # First Quadrant
        elif angle >= 0 and angle < 90:
            motor1Speed = round(1023 * speed)
            motor2Speed = round(remap(asMultiplier, 0, 90, 0, 2047))

        # Second Quadrant
        elif angle > 90 and angle <= 180:
            motor1Speed = round(remap(asMultiplier, 90, 180, 1023, 0))
            motor2Speed = round(2047 * speed)

        # Third Quadrant
        elif angle < 0 and angle > -90:
            motor1Speed = round(remap(asMultiplier, -90, 0, 2047, 0))
            motor2Speed = round(1023 * speed)

        # Fourth Quadrant
        elif angle < -90 and angle >= -180:
            motor1Speed = round(2047 * speed)
            motor2Speed = round(remap(asMultiplier, -180, -90, 0, 1023))

        motor1.set_moving_speed(motor1Speed)
        motor2.set_moving_speed(motor2Speed)

    sio.connect('http://192.168.2.12:3000')
    sio.wait()

except KeyboardInterrupt:
    time.sleep(0.5)
    motor1.set_moving_speed(0)
    motor2.set_moving_speed(0)
    motor1.disable_torque()
    motor2.disable_torque()
