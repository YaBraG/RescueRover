let WIDTH =1000
let HEIGHT = 800

leftAngle = 0
leftSpeed = 0
rightAngle = 0
rightSpeed = 0

let dispAng 
let dispSpe
let powerMode 
mode = "Normal Mode (80%)"

let motorPWR = {
    m1:80,
    m2:80,
    m3:80,
    m4:80
}
let multiAng = 1
let multiSpeed = 200

let sendValues = {}

function setup() {
    dispAng = document.getElementById("leftAngle")
    dispSpe = document.getElementById("leftSpeed")
    powerMode = document.getElementById("power-mode")

    createCanvas(WIDTH, HEIGHT);
    stroke(51);
    strokeWeight(5);
}
  
function draw() {
    background(220);
    
    push()
        translate(WIDTH/2, HEIGHT/2)
        let x = (Math.cos(leftAngle)*leftSpeed)*multiSpeed
        let y = -(Math.sin(leftAngle)*leftSpeed)*multiSpeed

        line(0,0,x,y)
        circle(x,y, 10)

        if(controllers[0]){
            update();
        }
    pop()
}

function draw() {
    background(220);
    
    push()
    translate(WIDTH/2, HEIGHT/2)
    let x = (Math.cos(leftAngle)*leftSpeed)*multiSpeed
    let y = -(Math.sin(leftAngle)*leftSpeed)*multiSpeed
    
    line(0,0,x,y)
    circle(x,y, 10)
    
    if(controllers[0]){
        update();
    }
    pop()
}
let powerSet = true
const buton=document.getElementById("submit")

buton.addEventListener("click",(e)=>{
    motorPWR.m1=parseInt(document.getElementById("m1").value)
    motorPWR.m2=parseInt(document.getElementById("m2").value)
    motorPWR.m3=parseInt(document.getElementById("m3").value)
    motorPWR.m4=parseInt(document.getElementById("m4").value)
    powerSet=true
});
function update () {

    var controller = controllers[0];

    let leftxAxis = controllers[0].axes[0]
    let leftyAxis = -controllers[0].axes[1]
    let rightxAxis = controllers[0].axes[2]
    let rightyAxis = -controllers[0].axes[3]

    var buttonA = controller.buttons[0];
    var buttonB = controller.buttons[1];
    var buttonX = controller.buttons[2];
    var buttonY = controller.buttons[3];

    var pressed = buttonA == 1.0;
    var pressedB = buttonB == 1.0;
    var pressedX = buttonX == 1.0;
    var pressedY = buttonY == 1.0;


    if (typeof(buttonA) == "object") {
    pressed = buttonA.pressed;
    buttonA = buttonA.value;
    }
    if (typeof(buttonB) == "object") {
    pressedB = buttonB.pressed;
    buttonB = buttonB.value;
    }
    if (typeof(buttonX) == "object") {
    pressedX = buttonX.pressed;
    buttonX = buttonX.value;
    }
    if (typeof(buttonY) == "object") {
    pressedY = buttonY.pressed;
    buttonY = buttonY.value;
    }

    if (pressed) {
    mode = "Extreme Mode (100)%"
    motorPWR.m1 = 100
    motorPWR.m2 = 100
    motorPWR.m3 = 100
    motorPWR.m4 = 100
    }
    if (pressedB) {
    mode = "Normal Mode (80%)"
    motorPWR.m1 = 80
    motorPWR.m2 = 80
    motorPWR.m3 = 80
    motorPWR.m4 = 80
    }
    if (pressedX) {
    mode = "Power Saving Mode (60%)"
    motorPWR.m1 = 60
    motorPWR.m2 = 60
    motorPWR.m3 = 60
    motorPWR.m4 = 60
    }
    if (pressedY) {
    mode = "Custom Mode (0-100%)"
    powerSet=false
    }

    
    leftAngle = Math.atan2(leftyAxis,leftxAxis)
    leftSpeed = Math.hypot(leftxAxis,leftyAxis)
    rightAngle = Math.atan2(rightyAxis,rightxAxis)
    rightSpeed = Math.hypot(rightxAxis,rightyAxis)
    

    if (leftSpeed > 1){
        leftSpeed = 1 
    }
    if (leftSpeed < -1){
        leftSpeed = -1 
    }
    if (rightSpeed > 1){
        rightSpeed = 1 
    }
    if (rightSpeed < -1){
        rightSpeed = -1 
    }

    powerMode.innerText = mode
    sendValues.leftSpeed = leftSpeed      
    dispSpe.innerText = Math.round(leftSpeed*1000)/1000

    sendValues.leftAngle = leftAngle*(180/Math.PI)
    dispAng.innerText = Math.round(leftAngle*(180/Math.PI)*1000)/1000

    sendValues.mode = motorPWR

    if(powerSet){
        socket.emit('drive-control', sendValues)
    }

    socket.on("lidar-data", data=> {
        console.log(data)
    })
}