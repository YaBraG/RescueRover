let aAxis = {
    x:0,
    y:0,
    z:0
}
let aDelta = {
    x:0,
    y:0,
    z:0
}

function updateAccelDisplay({x,y,z}) {
    const dispX = document.getElementById("ax");
    const dispY = document.getElementById("ay");
    const dispZ = document.getElementById("az");

    dispX.innerHTML = `x: ${x}`
    dispY.innerHTML = `y: ${y}`
    dispZ.innerHTML = `z: ${z}`
}