const domain = (new URL(window.location.href));
const socket = io(domain.host);
let tics = 0;
let startTime = Date.now();

socket.on("connect", () => {
    socket.emit("ID", "gyro-display");
    console.log("CONNECTION");
})

socket.on("raw-values", (gyro, accel, mag) => {
    updateGyroDisplay(gyro);
    updateAccelDisplay(accel);
    updateMagDisplay(mag);

    if(tics === 0) {
        gAxis.x = gyro.x;
        gAxis.y = gyro.y;
        gAxis.z = gyro.z;

        aAxis.x = accel.x;
        aAxis.y = accel.y;
        aAxis.z = accel.z;

        mAxis.x = mag.x;
        mAxis.y = mag.y;
        mAxis.z = mag.z;
    } else {
        gDelta.x = gAxis.x - gyro.x;
        gDelta.y = gAxis.y - gyro.y;
        gDelta.z = gAxis.z - gyro.z;

        aDelta.x = aAxis.x - accel.x;
        aDelta.y = aAxis.y - accel.y;
        aDelta.z = aAxis.z - accel.z;

        mDelta.x = mAxis.x - mag.x;
        mDelta.y = mAxis.y - mag.y;
        mDelta.z = mAxis.z - mag.z;
    }
    tics++
})