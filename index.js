const os = require("os")
const linux = os.platform() === 'linux' ? true : false
const sysnames = ['helmet', 'server','turret'];
// process.env.sys="server"

if(linux) {
    const sysname = process.env.sys ? process.env.sys : os.hostname()
    const system = sysnames.indexOf(sysname) > -1 ? sysname : false;

    if(system) {
        console.log("initiating system: "+ system + ' on raspberrypi', '\x1b[32m%s\x1b[0m')

        require(`./startup/${system}/main`)(true, sysname)
    } else {
        console.error(new Error("hostname does not fit any subsystem description, cannot initiate..."))
    }
} else {
    const system = sysnames.indexOf(process.env.sys) > -1 ? process.env.sys : false;
    
    if(system) {
        console.log("initiating system: "+ system.toUpperCase() + ' on mock mode', '\x1b[32m%s\x1b[0m')
        require(`./startup/${system}/main`)(false, system)
    } else {
        console.error(new Error("process.env.sys requires a system name to start..."))
    }
}
