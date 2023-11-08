from js import document

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")

ctx.fillStyle = "red"
ctx.fillRect(0, 0, 100, 100)

