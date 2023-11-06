const domain = (new URL(window.location.href));
const socket = io(domain.host);
let startTime = Date.now();

socket.on("connect", ()=> {
    socket.emit("ID", "js-controller");
    console.log("CONNECTION");
})