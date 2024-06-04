from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable
import requests
import json

COLUMNS = [("Code", "Name", "Sports")]

def load_data() -> []:
    # REST call
    url = "https://data.paris2024.org/api/explore/v2.1/catalog/datasets/paris-2024-sites-de-competition/records?limit=60"
    response = requests.get(url, verify=True)
    payload = json.loads(response.text)

    print("Dataset size :", payload["total_count"])

    rows = [("Code", "Name", "Sports")]
    sites = payload["results"]

    for site in sites:
        # if site["category_id"] == "venue-olympic":
        rows.append((site["code_site"],
                     site["nom_site"],
                     site["sports"]))
        # print(f"{rows}\n")

    return rows


class MyApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("c", "sort_by_code", "Sort By Code"),
                ("n", "sort_by_name", "Sort By Name"),
                ("q, Q", "quit", "Quit"),
                ]

    CSS_PATH = "styles.tcss"

    def __init__(self):
        super().__init__()
        self.rows = load_data()

    current_sorts: set = set()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield DataTable()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def sort_reverse(self, sort_type: str):
        """Determine if `sort_type` is ascending or descending."""
        reverse = sort_type in self.current_sorts
        if reverse:
            self.current_sorts.remove(sort_type)
        else:
            self.current_sorts.add(sort_type)
        return reverse

    def action_sort_by_name(self) -> None:
        """Sort DataTable by name (via a lambda)."""
        table = self.query_one(DataTable)
        table.sort(
            "Name",
            key=lambda name: name,
            reverse=self.sort_reverse("Name"),
        )

    def action_sort_by_code(self) -> None:
        """Sort DataTable by country which is a `Rich.Text` object."""
        table = self.query_one(DataTable)
        table.sort(
            "Code",
            key=lambda code: code,
            reverse=self.sort_reverse("Code"),
        )

    def on_mount(self) -> None:
        self.title = "Olympics sites"
        self.sub_title = "TUI"
        table = self.query_one(DataTable)
        for col in self.rows[0]:
            table.add_column(col, key=col)
        # table.add_columns(*self.rows[0])
        table.add_rows(self.rows[1:])
        table.cursor_type = "row"


if __name__ == "__main__":
    app = MyApp()
    app.run()
