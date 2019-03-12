import click
import json
import os
from pathlib import Path

from cupper.logic import update_project_template_branch


@click.command()
@click.option('--context-file', '-c', type=click.Path(file_okay=True, readable=True, allow_dash=True),
              default="docs/cookiecutter_input.json")
@click.option('--branch', '-b', default="cookiecutter-template")
def main(context_file: str, branch: str):
    """Cupper - Cookie-cutter Upper - Upgrades projects created from a template"""
    context = _load_context(context_file)
    project_directory = os.getcwd()
    update_project_template_branch(context, project_directory, branch)


def _load_context(context_file: str):
    context_str = Path(context_file).read_text(encoding="utf-8")
    context = json.loads(context_str)
    return context
