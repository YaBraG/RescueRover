let gAxis = {
    x:0,
    y:0,
    z:0
}
let gDelta = {
    x:0,
    y:0,
    z:0
}

function updateGyroDisplay({x,y,z}) {
    const dispX = document.getElementById("gx");
    const dispY = document.getElementById("gy");
    const dispZ = document.getElementById("gz");

    dispX.innerHTML = `x: ${x}`
    dispY.innerHTML = `y: ${y}`
    dispZ.innerHTML = `z: ${z}`
}