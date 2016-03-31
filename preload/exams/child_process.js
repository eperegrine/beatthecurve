var process = require("child_process")
var spawn = process.spawn
var execFile = process.execFile

var child = spawn("ls", ["-lF", "/rooot"])

//child.stdout.on("data", function (data) {
//  console.log("spawnSTDOUT:", JSON.stringify(data))
//})
//
//child.stderr.on("data", function (data) {
//  console.log("spawnSTDERR:", JSON.stringify(data))
//})
//
//child.on("exit", function (code) {
//  console.log("spawnEXIT:", code)
//})

//child.kill("SIGKILL")

execFile("python", ["download_images.py", "arg1"], null, function (err, stdout, stderr) {
  console.log("execFileSTDOUT:", JSON.stringify(stdout));
  console.log("execFileSTDERR:", JSON.stringify(stderr));
})