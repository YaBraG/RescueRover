let WIDTH =1000
let HEIGHT = 800

leftAngle = 0
leftSpeed = 0
rightAngle = 0
rightSpeed = 0

let dispAng 
let dispSpe

let multiAng = 1
let multiSpeed = 200

let sendValues = {}

function setup() {
    var d = document.getElementById("controller" + 0);
    var buttons = d.getElementsByClassName("button");
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
    let leftxAxis = controllers[0].axes[0]
    let leftyAxis = -controllers[0].axes[1]
    let rightxAxis = controllers[0].axes[2]
    let rightyAxis = -controllers[0].axes[3]
    
    // let bottonA = controllers[0].buttons[0]
    // let bottonX = controllers[0].buttons[2]
    // let bottonY = controllers[0].buttons[3]
    // let bottonB = controllers[0].buttons[1]
    sendValues.pwm = 0
    
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

    if(buttonA){
        sendValues.pwm=100
    }
    if(buttonX){
        sendValues.pwm=80
    }
    if(buttonB){
        sendValues.pwm=60
    }
    if(buttonX){
        sendValues.pwm=10
    }

    sendValues.leftSpeed = leftSpeed      
    dispSpe.innerText = leftSpeed

    sendValues.leftAngle = leftAngle*(180/Math.PI)
    dispAng.innerText = leftAngle*(180/Math.PI)

    socket.emit('drive-control', sendValues)
}