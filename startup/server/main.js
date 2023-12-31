const { createServer } = require("http");
const { Server } = require("socket.io");
const express = require("express");

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, { /* options */ });
const PORT = 3000;

function exec () {
  io.on("connection", (socket) => {
    socket.on("ID", id => {
      console.log("CONNECTION: ", id)
    })

    socket.on("drive-control", data=>{
      io.emit("drive-orders", data.leftAngle, data.leftSpeed,data.mode,data.motor)
      // console.log(data.motor)
      
      
    })
    socket.on("lidar", (cart_data)=> {
      io.emit("lidar-data", cart_data)
    })

  });
  
  require("./routes/router")(app);

  httpServer.listen(PORT, ()=>{
    const ip = require("../helper").getHostIp();
    console.log(`http://${ip}:${PORT}`)
  });
}

module.exports = exec;
