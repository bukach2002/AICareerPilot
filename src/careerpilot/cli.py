"""careerpilot [your resume]: one command, the rest happens on the screen it opens."""

from __future__ import annotations

import io
import sys
from pathlib import Path

import click

from careerpilot import __version__
from careerpilot.config import ConfigError, default_home
from careerpilot.database import DatabaseError
from careerpilot.plugins import PluginError


@click.command()
@click.version_option(__version__)
@click.argument("resume", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path))
def main(resume: Path | None) -> None:
    """Give it your resume, get the jobs that fit, select them and apply."""
    # Imported here: the interface takes a moment to load, and --help should not wait for it.
    from careerpilot.tui import CareerPilot

    CareerPilot(default_home().resolve(), resume.resolve() if resume else None).run()


def run() -> None:
    # A Windows console's code page cannot print every company's name.
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except (ConfigError, DatabaseError, PluginError) as error:
        raise SystemExit(f"careerpilot: {error}") from error
