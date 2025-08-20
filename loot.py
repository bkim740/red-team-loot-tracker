#!/usr/bin/env python3
import json, os, csv
import typer
from tabulate import tabulate

app = typer.Typer(help="Red Team Loot Tracker (persistent)")

DATA_FILE = "loot.json"

def load_loot():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_loot(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.command()
def add(
    type: str = typer.Option(..., help="cred | file | note"),
    name: str = typer.Option(..., help="descriptive name"),
    tags: str = typer.Option("", help="comma-separated tags"),
    value: str = typer.Option(..., help="secret/path/text"),
):
    """Add a new loot item."""
    loot = load_loot()
    entry = {
        "type": type,
        "name": name,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "value": value,
    }
    loot.append(entry)
    save_loot(loot)
    typer.secho(f"Added: {name}", fg=typer.colors.GREEN)

@app.command()
def list():
    """List all loot items."""
    loot = load_loot()
    rows = [[i, x["type"], x["name"], ",".join(x["tags"])] for i, x in enumerate(loot)]
    print(tabulate(rows, headers=["ID", "Type", "Name", "Tags"], tablefmt="github"))

@app.command()
def search(keyword: str):
    """Search loot by keyword in name/tags."""
    loot = load_loot()
    results = [
        [i, x["type"], x["name"], ",".join(x["tags"])]
        for i, x in enumerate(loot)
        if keyword.lower() in x["name"].lower() or keyword.lower() in ",".join(x["tags"]).lower()
    ]
    if not results:
        typer.secho("No results.", fg=typer.colors.YELLOW)
        raise typer.Exit()
    print(tabulate(results, headers=["ID", "Type", "Name", "Tags"], tablefmt="github"))

@app.command()
def export(format: str = typer.Option(..., help="csv | json"), out: str = typer.Option(...)):
    """Export loot to CSV or JSON."""
    loot = load_loot()
    if format == "json":
        with open(out, "w") as f:
            json.dump(loot, f, indent=2)
        typer.secho(f"Wrote {out}", fg=typer.colors.GREEN)
    elif format == "csv":
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["type","name","tags","value"])
            w.writeheader()
            for x in loot:
                w.writerow({"type": x["type"], "name": x["name"], "tags": ",".join(x["tags"]), "value": x["value"]})
        typer.secho(f"Wrote {out}", fg=typer.colors.GREEN)
    else:
        typer.secho("Unsupported format (use csv or json)", fg=typer.colors.RED)

if __name__ == "__main__":
    app()
