from typing import Optional

import typer

from bomsquad.vulndb.db.ingest import Ingest

app = typer.Typer()

nvd_app = typer.Typer(name="nvd")
app.add_typer(nvd_app)

osv_app = typer.Typer(name="osv")
app.add_typer(osv_app)


@nvd_app.command(name="ingest")
def _nvd_ingest(
    scope: Optional[str] = typer.Option(default=None, help="Ingest only cve or cpe "),
    offset: int = typer.Option(default=0, help="Offset into available entries to begin wtih"),
    limit: Optional[int] = typer.Option(default=None, help="Limit the number of entries to ingest"),
) -> None:
    if scope == "cve" or scope is None:
        Ingest.cve(offset, limit)
    if scope == "cpe" or scope is None:
        Ingest.cpe(offset, limit)


@osv_app.command(name="ingest")
def _osv_ingest(
    ecosystem: Optional[str] = typer.Option(default=None, help="Ingest only a single ecosystem"),
    offset: int = typer.Option(default=0, help="Offset into available entries to begin wtih"),
    limit: Optional[int] = typer.Option(default=None, help="Limit the number of entries to ingest"),
) -> None:
    if ecosystem:
        Ingest.osv(ecosystem, offset, limit)
    else:
        if offset != 0 or limit:
            raise ValueError("Offset and limit are only valid with a specific ecosystem")
        Ingest.all_osv()
