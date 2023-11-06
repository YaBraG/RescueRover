const express = require("express")
const orientation = express.Router();
const path = require("path")
const viewPath = '../../../../views'

module.exports = (app) => {
    app.get("/", (req, res)=> {
        res.sendFile(path.resolve(__dirname + viewPath + '/index/view.html'))
    })

    app.use('/orientation', orientation)

    app.get("/mouse-control", (req, res)=> {
        res.sendFile(path.resolve(__dirname + viewPath + '/mouse-control/view.html'))
    })
    app.get("/gyro-ref", (req, res)=> {
        res.sendFile(path.resolve(__dirname + viewPath + '/gyro-ref.html'))
    })

}

const orientationRoute = __dirname + viewPath + '/orientation'

orientation.get('/', (req, res) => res.sendFile(path.resolve(orientationRoute + '/view.html')))
orientation.get('/connection', (req, res) => res.sendFile(path.resolve(orientationRoute + '/connection.js')))
orientation.get('/accel', (req, res) => res.sendFile(path.resolve(orientationRoute + '/accel.js')))
orientation.get('/draw', (req, res) => res.sendFile(path.resolve(orientationRoute + '/draw.js')))
orientation.get('/gyro', (req, res) => res.sendFile(path.resolve(orientationRoute + '/gyro.js')))
orientation.get('/mag', (req, res) => res.sendFile(path.resolve(orientationRoute + '/mag.js')))