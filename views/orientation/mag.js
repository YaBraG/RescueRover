let mAxis = {
    x:0,
    y:0,
    z:0
}
let mDelta = {
    x:0,
    y:0,
    z:0
}

function updateMagDisplay({x,y,z}) {
    const dispX = document.getElementById("mx");
    const dispY = document.getElementById("my");
    const dispZ = document.getElementById("mz");

    dispX.innerHTML = `x: ${x}`
    dispY.innerHTML = `y: ${y}`
    dispZ.innerHTML = `z: ${z}`
}