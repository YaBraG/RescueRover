const socket = io("http://10.13.82.169:3000")

socket.on("connection", ()=> {
    console.log("c")
    socket.emit("ID", "js-controller")
})