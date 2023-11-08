"""PyScriptでライフゲームを実装するサンプルです。
"""
from js import document, window
from pyodide import create_proxy

class Universe:
    """ライフゲームの宇宙を表すクラスです。
    """
    def __init__(self, canvasId: str, width: int, height: int):
        """ライフゲームの宇宙を初期化します。
        """
        canvas = document.getElementById(canvasId)
        canvas.width = width
        canvas.height = height
        ctx = canvas.getContext("2d")
        self.canavs = canvas
        self.ctx = ctx
        self.width = width
        self.height = width
        self.cells = [False] * self.width * self.height
        for idx in range(len(self.cells)):
            if idx % 2 == 0 or idx % 7 == 0:
                self.cells[idx] = True

    def tick(self):
        """ライフゲームの世代を進めます。
        """
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

    def getIndex(self, row: int, column: int) -> int:
        """行番号と列番号からインデックスを計算します。

        Args:
            row (int): 行番号
            column (int): 列番号

        Returns:
            int: インデックス番号
        """
        return row * self.width + column

    def getCell(self, row: int, column: int) -> bool:
        """指定した行番号と列番号のセルの状態を取得します。

        Args:
            row (int): 行番号
            column (int): 列番号

        Returns:
            bool: セルの状態
        """
        idx = self.getIndex(row, column)
        return self.cells[idx]

    def liveNeighborCount(self, row: int, column: int) -> int:
        """指定した行番号と列番号のセルの周囲の生きたセルの数を取得します。
        """
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
        """ライフゲームの宇宙を描画します。
        """
        self.ctx.fillStyle = "white"
        self.ctx.fillRect(0, 0, self.width, self.height)

        for row in range(self.height):
            for col in range(self.width):
                idx = self.getIndex(row, col)
                cell = self.cells[idx]

                if cell:
                    self.ctx.fillStyle = "black"
                    self.ctx.fillRect(row, col, 1, 1)

universe = Universe("canvas", 64, 64)

def renderLoop():
    universe.render()
    universe.tick()
    window.requestAnimationFrame(proxiedRenderLoop)

proxiedRenderLoop = create_proxy(lambda _: renderLoop())
renderLoop()
