from textual.app import App, ComposeResult
from textual.coordinate import Coordinate
from textual.widgets import Header, Footer, DataTable, Tree, Static, Input
import string
_decode_table = {_: '.' for _ in range(256)}
_decode_table.update({ord(_): _ for _ in string.printable[:-5]})

cols = ("Base", "Hex", "String")

fn = "F"

class HexNavigator(Static):

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Position", id = "position")
        yield Tree(label = "Structure", id = "kaitai_tree")

    def on_mount(self) -> None:
        tree: Tree[dict] = self.query_one(Tree)
        tree.root.expand()
        base = tree.root.add("Something", expand=True)
        base.add_leaf("Thing")
        base.add_leaf("Other Thing")
        base.add_leaf("Final Thing")

class HexViewer(Static):

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield HexNavigator()
        yield DataTable(id = "HexTable")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns(*cols)
        with open(fn, "rb") as f:
            rows = []
            while True:
                loc = f.tell()
                chunk = f.read(0x10)
                if not chunk: break
                rows.append( ("{0:010x}".format(loc), 
                              " ".join("{0:02x}".format(_) for _ in chunk),
                              "".join(_decode_table[_] for _ in chunk)))
        table.add_rows(rows)

    def on_input_submitted(self, event: Input.Submitted):
        table = self.query_one(DataTable)
        table.cursor_coordinate = Coordinate(row = int(event.value) // 16, column = 0)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted):
        position = self.query_one(Input)
        position.value = str(event.cursor_row * 16)
        

class HexViewerApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "hexviewer.css"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield HexViewer()
        yield Footer()

if __name__ == "__main__":
    app = HexViewerApp()
    app.run()
