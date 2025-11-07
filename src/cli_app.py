"""CLI entrypoint shim.

The real CLI app and the cli_facade live in `src.application.cli_app`.
This module re-exports the Typer app so you can run `python -m src.cli_app`.
"""

from src.application.cli_app import app  # re-export the Typer app

if __name__ == "__main__":
    app()
