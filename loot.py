import json, os, sys, csv
from typing import Optional, List
import typer
from cryptography.fernet import Fernet
import pandas as pd

app = typer.Typer()

VAULT_FILE = "vault.enc"
KEY_FILE = "vault.key"

def _load_key() -> bytes:
    if not os.path.exists(KEY_FILE):
        typer.secho("No vault.key found — run `python loot.py init`", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    return open(KEY_FILE, "rb").read()

def _fernet() -> Fernet:
    return Fernet(_load_key())

def _read_vault() -> list:
    if not os.path.exists(VAULT_FILE):
        return []
    f = _fernet()
    data = f.decrypt(open(VAULT_FILE, "rb").read())
    return json.loads(data.decode())

def _write_vault(items: list):
    f = _fernet()
    token = f.encrypt(json.dumps(items, indent=2).encode())
    open(VAULT_FILE, "wb").write(token)

@app.command()
def init():
    "Initialize a new vault (creates vault.key)"
    if os.path.exists(KEY_FILE):
        typer.echo("vault.key already exists")
        raise typer.Exit()
    key = Fernet.generate_key()
    open(KEY_FILE, "wb").write(key)
    typer.secho("Created vault.key — keep this safe!", fg=typer.colors.GREEN)

@app.command()
def add(type: str = typer.Option(..., help="cred/file/note"),
        name: str = typer.Option(...),
        value: str = typer.Option(..., help="secret, path, or text"),
        tags: str = typer.Option("", help="comma-separated tags")):
    items = _read_vault()
    item = {
        "type": type,
        "name": name,
        "value": value,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
    }
    items.append(item)
    _write_vault(items)
    typer.secho(f"Added: {name}", fg=typer.colors.GREEN)

@app.command()
def list():
    items = _read_vault()
    for i, it in enumerate(items):
        typer.echo(f"[{i}] {it['type']} | {it['name']} | tags={','.join(it['tags'])}")

@app.command()
def search(query: str):
    items = _read_vault()
    q = query.lower()
    for i, it in enumerate(items):
        if q in it["name"].lower() or q in " ".join(it["tags"]).lower():
            typer.echo(f"[{i}] {it['type']} | {it['name']} | tags={','.join(it['tags'])}")

@app.command()
def export(format: str = typer.Option("csv", help="csv or json"),
          out: str = typer.Option("loot.csv")):
    items = _read_vault()
    if format == "json":
        open(out, "w").write(json.dumps(items, indent=2))
        typer.echo(f"Wrote {out}")
    else:
        df = pd.DataFrame(items)
        df.to_csv(out, index=False)
        typer.echo(f"Wrote {out}")

if __name__ == "__main__":
    app()
