let piblaster;
const { io } = require("socket.io-client");

if(process.platform === 'linux'){
    console.log("LINUX platform");
    piblaster = require("pi-blaster.js");
}

const ipAddresses = [
    "http://192.168.2.15:3000",
    "http://192.168.2.14:3000",
    "http://192.168.0.100:3000",
    "http://192.168.0.109:3000",
    "http://192.168.2.19:3000",
    "http://192.168.2.16:3000"
]
const sockets = []
let socket;

function exec () {
    console.log("connecting to server...")

    for(let i = 0; i < ipAddresses.length; i++) {

        sockets[i] = io(ipAddresses[i])

        sockets[i].on("connect", ()=> {
            socket = sockets[i];
            console.log("CONNECTION");
            socket.emit("ID", "turret-"+i);
            flushSockets(i);
            initReciever();
        })
    }
}


function flushSockets(exception) {
    console.log("FLUSHING SOCKETS")
    for(let i = 0; i < ipAddresses.length; i++) {
        if(i !== exception){
            sockets[i].close();
            sockets[i] = null;
        }
    }
}

function initReciever() {
    console.log("INITIALIZING RECIEVER")
    // piblaster 180 degree for servo is 0.06 - 0.24
    socket.on("gyro-output", (pitch, roll, yaw)=>{
        console.log(pitch, yaw)
        // console.log(`pitch: ${pitch} yaw: ${yaw}`)
        // pin 4 is pitch
        piblaster.setPwm(4, pitch)
        
        // piblaster.setPwm(4, 0.08)
        // pin 17 is yaw 
        piblaster.setPwm(17, yaw)
        // piblaster.setPwm(17, 0.14)
    })

    
}

module.exports = exec;
