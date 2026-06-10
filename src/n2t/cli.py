"""Console script for n2t."""

import typer
from rich.console import Console

from n2t import utils

app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for n2t."""
    console.print("Replace this message by putting your code into n2t.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
