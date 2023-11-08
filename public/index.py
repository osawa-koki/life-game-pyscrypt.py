"""PyScriptでライフゲームを実装するサンプルです。
"""
# pylint: disable=no-name-in-module, import-error
from js import document, window
from pyodide import create_proxy
# pylint: enable=import-error


class Universe:
    """ライフゲームの宇宙を表すクラスです。
    """

    def __init__(self, canvas_id: str, width: int, height: int):
        """ライフゲームの宇宙を初期化します。
        """
        canvas = document.getElementById(canvas_id)
        canvas.width = width
        canvas.height = height
        ctx = canvas.getContext("2d")
        self.canavs = canvas
        self.ctx = ctx
        self.width = width
        self.height = width
        self.cells = [False] * self.width * self.height
        for idx, _cell in enumerate(self.cells):
            if idx % 2 == 0 or idx % 7 == 0:
                self.cells[idx] = True

    def tick(self):
        """ライフゲームの世代を進めます。
        """
        next_state = [False] * self.width * self.height

        for row in range(self.height):
            for col in range(self.width):
                idx = self.get_index(row, col)
                cell = self.cells[idx]
                live_neighbors = self.live_neighbor_count(row, col)

                next_cell = None
                if cell and live_neighbors < 2:
                    next_cell = False
                elif cell and live_neighbors in (2, 3):
                    next_cell = True
                elif cell and live_neighbors > 3:
                    next_cell = False
                elif not cell and live_neighbors == 3:
                    next_cell = True
                else:
                    next_cell = cell

                next_state[idx] = next_cell

        self.cells = next_state

    def get_index(self, row: int, column: int) -> int:
        """行番号と列番号からインデックスを計算します。

        Args:
            row (int): 行番号
            column (int): 列番号

        Returns:
            int: インデックス番号
        """
        return row * self.width + column

    def get_cell(self, row: int, column: int) -> bool:
        """指定した行番号と列番号のセルの状態を取得します。

        Args:
            row (int): 行番号
            column (int): 列番号

        Returns:
            bool: セルの状態
        """
        idx = self.get_index(row, column)
        return self.cells[idx]

    def live_neighbor_count(self, row: int, column: int) -> int:
        """指定した行番号と列番号のセルの周囲の生きたセルの数を取得します。
        """
        count = 0
        for delta_row in [self.height - 1, 0, 1]:
            for delta_col in [self.width - 1, 0, 1]:
                if delta_row == 0 and delta_col == 0:
                    continue

                neighbor_row = (row + delta_row) % self.height
                neighbor_col = (column + delta_col) % self.width
                idx = self.get_index(
                    neighbor_row,
                    neighbor_col
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
                idx = self.get_index(row, col)
                cell = self.cells[idx]

                if cell:
                    self.ctx.fillStyle = "black"
                    self.ctx.fillRect(row, col, 1, 1)


universe = Universe("canvas", 64, 64)


def render_loop():
    """ライフゲームの宇宙を描画するループです。
    """
    universe.render()
    universe.tick()
    window.requestAnimationFrame(proxiedRenderLoop)


proxiedRenderLoop = create_proxy(lambda _: render_loop())
render_loop()
