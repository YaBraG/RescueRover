let WIDTH =1000
let HEIGHT = 800

leftAngle = 0
leftSpeed = 0
rightAngle = 0
rightSpeed = 0
mode = 0

let dispAng 
let dispSpe

let multiAng = 1
let multiSpeed = 200

let sendValues = {}

function setup() {
    dispAng = document.getElementById("leftAngle")
    dispSpe = document.getElementById("leftSpeed")

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
    console.log("Button A Pressed")
    mode=1
    }
    if (pressedB) {
    console.log("Button B Pressed")
    mode=2
    }
    if (pressedX) {
    console.log("Button X Pressed")
    mode=3
    }
    if (pressedY) {
    console.log("Button Y Pressed")
    mode=4
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

    sendValues.leftSpeed = leftSpeed      
    dispSpe.innerText = leftSpeed

    sendValues.leftAngle = leftAngle*(180/Math.PI)
    dispAng.innerText = leftAngle*(180/Math.PI)

    sendValues.mode = mode

    socket.emit('drive-control', sendValues)
}