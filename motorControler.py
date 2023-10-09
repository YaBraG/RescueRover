import RPi.GPIO as GPIO
import time
import socketio

sio = socketio.Client()
GPIO.satmode(GPIO.BCM)
GPIO.setwarnings(False)


class MotionMode():
    def __init__(self, Ena, In1, In2):
        self.Ena = Ena
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(self.Ena, GPIO.OUT)  # motor A
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


Motor1 = MotionMode(4, 17, 27)
Motor2 = MotionMode(24, 23, 22)
Motor3 = MotionMode(26, 16, 13)
Motor4 = MotionMode(12, 5, 6)
Motor1.pwm()

def FullPowerDrivingMode():
    # FORWARD MOVEMENT
    Motor1.moveF(100)
    Motor2.moveF(100)
    Motor3.moveF(100)
    Motor4.moveF(100)
    # BACKWARD MOVEMENT
    Motor1.moveB(100)
    Motor2.moveB(100)
    Motor3.moveB(100)
    Motor4.moveB(100)
    # RIGHT MOVEMENT
    Motor1.moveF(100)
    Motor2.moveB(100)
    Motor3.moveF(100)
    Motor4.moveB(100)
    # LEFT MOVEMENT
    Motor1.moveB(100)
    Motor2.moveF(100)
    Motor3.moveB(100)
    Motor4.moveF(100)


def NormalDrivingMode():

    # FORWARD MOVEMENT
    Motor1.moveF(80)
    Motor2.moveF(80)
    Motor3.moveF(80)
    Motor4.moveF(80)
    # BACKWARD MOVEMENT
    Motor1.moveB(80)
    Motor2.moveB(80)
    Motor3.moveB(80)
    Motor4.moveB(80)
    # RIGHT MOVEMENT
    Motor1.moveF(80)
    Motor2.moveB(80)
    Motor3.moveF(80)
    Motor4.moveB(80)
    # LEFT MOVEMENT
    Motor1.moveB(80)
    Motor2.moveF(80)
    Motor3.moveB(80)
    Motor4.moveF(80)


def LowPowerDrivingMode():
    # FORWARD MOVEMENT
    Motor1.moveF(60)
    Motor2.moveF(60)
    Motor3.moveF(60)
    Motor4.moveF(60)
    # BACKWARD MOVEMENT
    Motor1.moveB(60)
    Motor2.moveB(60)
    Motor3.moveB(60)
    Motor4.moveB(60)
    # RIGHT MOVEMENT
    Motor1.moveF(60)
    Motor2.moveB(60)
    Motor3.moveF(60)
    Motor4.moveB(60)
    # LEFT MOVEMENT
    Motor1.moveB(60)
    Motor2.moveF(60)
    Motor3.moveB(60)
    Motor4.moveF(60)


def CustumizedDrivingMode():
    # Forward 2 Front wheels
    Motor1.moveF(100)
    Motor2.moveF(100)
    # Backward 2 Front wheels
    Motor1.moveB(100)
    Motor2.moveB(100)
    # Forward 2 rear wheels
    Motor3.moveF(100)
    Motor4.moveF(100)
    # Backward 2 rear wheels
    Motor3.moveB(100)
    Motor4.moveB(100)
    # Forward 2 Right wheels
    Motor1.moveF(100)
    Motor3.moveF(100)
    # Backward 2 Right wheels
    Motor1.moveB(100)
    Motor3.moveB(100)
    # Forward 2 Left wheels
    Motor2.moveF(100)
    Motor4.moveF(100)
    # Backward 2 Left wheels
    Motor2.moveB(100)
    Motor4.moveB(100)

try:
    @sio.event
    def connect():
        print('connection established')
        sio.emit("ID", 'RescueRober-client')

    @sio.event
    def disconnect():
        print('disconnected from server')
        time.sleep(0.5)
        

    @sio.on('inertial-order')
    def on_message(yaw, pitch):
        m1Yaw = round(remap(yaw, 180, -180, 0, 1023))
        m2Pitch = round(remap(pitch, -180, 180, 150, 1023))
        motor1.set_goal_position(m1Yaw)
        motor2.set_goal_position(m2Pitch)

    sio.connect('http://192.168.2.13:3000')
    sio.wait()

except KeyboardInterrupt:
    time.sleep(0.5)
    motor1.set_moving_speed(0)
    motor2.set_moving_speed(0)
    motor1.disable_torque()
    motor2.disable_torque()