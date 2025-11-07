import asyncio
from typing import Optional

import typer

# Import the facade at command runtime from src.cli_app to avoid circular imports

app = typer.Typer(help="CLI for the backend application (tools)")


@app.command()
def list_tools():
    """List all tools."""
    from src.application.cli_app import cli_facade

    facade = cli_facade

    async def _inner():
        tools = await facade.list_tools()
        for t in tools:
            typer.echo(f"{t.id}: {t.name} - {t.description} ({t.link})")

    asyncio.run(_inner())


@app.command()
def get_tool(tool_id: int):
    """Get a single tool by id."""
    from src.application.cli_app import cli_facade

    facade = cli_facade

    async def _inner():
        t = await facade.get_tool(tool_id)
        if t is None:
            typer.secho("Tool not found", fg=typer.colors.RED)
        else:
            typer.echo(f"{t.id}: {t.name} - {t.description} ({t.link})")

    asyncio.run(_inner())


@app.command()
def create(name: str, description: Optional[str] = "", link: Optional[str] = ""):
    """Create a new tool."""
    from src.application.cli_app import cli_facade

    facade = cli_facade

    async def _inner():
        t = await facade.create_tool(
            name=name, description=description or "", link=link or ""
        )
        typer.secho(f"Created tool {t.id}", fg=typer.colors.GREEN)

    asyncio.run(_inner())


@app.command()
def delete(tool_id: int):
    """Delete a tool by id."""
    from src.application.cli_app import cli_facade

    facade = cli_facade

    async def _inner():
        ok = await facade.delete_tool(tool_id)
        if ok:
            typer.secho("Deleted", fg=typer.colors.GREEN)
        else:
            typer.secho("Tool not found", fg=typer.colors.RED)

    asyncio.run(_inner())


def main():
    app()


if __name__ == "__main__":
    main()
