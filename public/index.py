from js import document, window
from pyodide import create_proxy

class Universe:
    def __init__(self):
        self.width = 64
        self.height = 64
        self.cells = [False] * self.width * self.height
        for idx in range(len(self.cells)):
            if idx % 2 == 0 or idx % 7 == 0:
                self.cells[idx] = True

    def tick(self):
        next = [False] * self.width * self.height

        for row in range(self.height):
            for col in range(self.width):
                idx = self.getIndex(row, col)
                cell = self.cells[idx]
                liveNeighbors = self.liveNeighborCount(row, col)

                nextCell = None
                if cell and liveNeighbors < 2:
                    nextCell = False
                elif cell and (liveNeighbors == 2 or liveNeighbors == 3):
                    nextCell = True
                elif cell and liveNeighbors > 3:
                    nextCell = False
                elif not cell and liveNeighbors == 3:
                    nextCell = True
                else:
                    nextCell = cell

                next[idx] = nextCell

        self.cells = next

    def getIndex(self, row, column):
        return row * self.width + column

    def getCell(self, row, column):
        idx = self.getIndex(row, column)
        return self.cells[idx]

    def liveNeighborCount(self, row, column):
        count = 0
        for deltaRow in [self.height - 1, 0, 1]:
            for deltaCol in [self.width - 1, 0, 1]:
                if deltaRow == 0 and deltaCol == 0:
                    continue

                neighborRow = (row + deltaRow) % self.height
                neighborCol = (column + deltaCol) % self.width
                idx = self.getIndex(
                neighborRow,
                neighborCol
                )
                if self.cells[idx]:
                    count += 1
        return count

    def render(self):
        canvas = document.getElementById("canvas")
        canvas.width = self.width
        canvas.height = self.height

        ctx = canvas.getContext("2d")
        ctx.fillStyle = "white"
        ctx.fillRect(0, 0, self.width, self.height)

        for row in range(self.height):
            for col in range(self.width):
                idx = self.getIndex(row, col)
                cell = self.cells[idx]

                if cell:
                    ctx.fillStyle = "black"
                    ctx.fillRect(row, col, 1, 1)

universe = Universe()

def renderLoop():
    universe.render()
    universe.tick()
    window.requestAnimationFrame(proxiedRenderLoop)

proxiedRenderLoop = create_proxy(lambda _: renderLoop())
renderLoop()
