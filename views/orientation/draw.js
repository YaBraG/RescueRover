function setup() {
    createCanvas(windowWidth, windowHeight, WEBGL);
    textSize(width / 3);
    textAlign(CENTER, CENTER);
    rectMode(CENTER);
}

function draw() {
    background(255);
    normalMaterial();
    translate(-240, -100,0);
    angleMode(DEGREES)

    push()
    rotateX(gDelta.y)
    rotateY(gDelta.x)
    rotateX(gDelta.z)
    box( 180, 30, 180)
    pop()
}